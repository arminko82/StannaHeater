#!/usr/bin/env python

# Armin Koefler, 19.08.2017
# This device code controls the interaction with the stepper motor driver board.

import sys
import logging
import signal
import RPi.GPIO as GPIO
import time
from custom_exceptions import NoDeviceLibraryFoundException

FULL_ROTATION_STEPS = 512 # the number of steps for a full rotation of the motor

coil_A_1_pin = 4 # brown wire
coil_A_2_pin = 17 # green wire
coil_B_1_pin = 23 # yellow wire
coil_B_2_pin = 24 # orange wire
enable_pin   = 7 # main switch

StepCount = 8
Seq = list(range(0, StepCount))

# Prepares all definitions and sets up the GPIO ports.
# On powerOn set the main switch is turned on at the end of setup
def setup(powerOn=False):
    try:
        logging.debug("Setup: Setting GPIO modes ...")
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
    except Exception as x:
        raise NoDeviceLibraryFoundException()
    
    Seq[0] = [1,0,0,0]
    Seq[1] = [1,1,0,0]
    Seq[2] = [0,1,0,0]
    Seq[3] = [0,1,1,0]
    Seq[4] = [0,0,1,0]
    Seq[5] = [0,0,1,1]
    Seq[6] = [0,0,0,1]
    Seq[7] = [1,0,0,1]

    GPIO.setup(enable_pin, GPIO.OUT)
    GPIO.setup(coil_A_1_pin, GPIO.OUT)
    GPIO.setup(coil_A_2_pin, GPIO.OUT)
    GPIO.setup(coil_B_1_pin, GPIO.OUT)
    GPIO.setup(coil_B_2_pin, GPIO.OUT)
    
    logging.debug("Setup: Resetting state and enabling power for driver ...")
    
    resetGpioState()
    time.sleep(1)
    if powerOn:
        GPIO.output(enable_pin, 1)
    logging.debug("Device setup complete")

def resetGpioState():
    setStep(0,0,0,0)
    GPIO.output(enable_pin, 0)
    logging.debug("GPIO state reset")
    
def forward(delay, steps):
    logging.info("Turning {0} steps clockwise using a delay of {1}ms".format(steps, delay)) # untested!
    for i in range(steps):
        for j in range(StepCount):
            setStep(getItem(j)[0], getItem(j)[1], getItem(j)[2], getItem(j)[3])
            time.sleep(delay)

def backwards(delay, steps):
    logging.info("Turning {0} steps counterclockwise using a delay of {1}ms".format(steps, delay)) # untested
    for i in range(steps):
        for j in reversed(range(StepCount)):
            setStep(getItem(j)[0], getItem(j)[1], getItem(j)[2], getItem(j)[3])
            time.sleep(delay)

def getItem(index) :
    return Seq[index % StepCount]

def setStep(w1, w2, w3, w4):
    GPIO.output(coil_A_1_pin, w1)
    GPIO.output(coil_A_2_pin, w2)
    GPIO.output(coil_B_1_pin, w3)
    GPIO.output(coil_B_2_pin, w4)