#!/usr/bin/env python

# Armin Koefler, file created at 24.08.2017
# This file contains the higher level functions that are invoked by the main method

import sys
import logging
from device import *
from const_vars import *
from custom_exceptions import NoDeviceLibraryFoundException, BoundaryException

# The file holds the currently known angle. It is reset to 0 when doCalibrate is called which
# moves the rotor to the left-most location and rewrites this file. Any call to doTurn updates the 
# file's value.
ANGLE_FILE = "./current_angle.dat"
#Specifes the minimal and the maximal angle the rotor may not surpass.
# Line 0 contains min angle, line 1 max angle
BORDER_ANGLE_FILE = "./border_angles.cfg"
STEP_DELAY = 5 # ms

# Executes the device's setup if not done before.
def doSetup():
    global mSetupDone
    if mSetupDone:
        return
    mSetupDone = True
    setup()
    
# Performs a calibration by turning the rotor counterclockwise till the limiter button
# is hit. After achieving this position the content on the angle file is reset to contain 0.
def doCalibrate():
    try:
        doSetup()
        raise Exception("No handling for implemented yet, no hardware created.")
        writeAngleFile(0)
        return RESULT_OK
    except NoDeviceLibraryFoundException as e:
        raise # rethrow GPIO error
    except Exception as ex:
        logging.error(ex)
        return ERROR_COMMON
        
# Reads the current rotor angle from the angle file.
# Returns ERROR_COMMON if the file is not present, else to file content.
# If the files content equals ERROR_COMMON exactly something bad has happened.
# doTurn()  should ensure that no matter what angle is the current on
# ERROR_COMMON is never written
# but at least differs the smallest epsilon possible from it.    
def doGetAngle():
    try:
        min, max = readBorders()
        with open(ANGLE_FILE) as f:
            return "{0}|{1}|{2}".format(min,
                                        max,
                                        f.readline().strip())  # current
    except:
        return ERROR_COMMON

#Reads the content of the corger
def readBorders():
    try:
        with open(BORDER_ANGLE_FILE) as b:
                return (b.readline().strip(),  # min
                        b.readline().strip())  # max
    except:
        return ERROR_COMMON
        
# Creates and opens the angle file, then writes angle into it.
def writeAngleFile(angle):
    if any(angle == x for x in RESPONSES):
        angle = angle + sys.float_info.epsilon
    with open(ANGLE_FILE, "w") as file:
        file.write(str(angle))
        
# Turns the amount defined by angleString and writes the result to the file.
# The result written to angle file always differs at least by the smallest floating point
# epsilon possible from ERROR_COMMON
def doTurn(angleString):
    try:
        angle = float(angleString)
        min, max = readBorders()
        if float(min) > angle or float(max) < angle:
            raise BoundaryException()
        currentAngle = doGetAngle()
        if currentAngle == ERROR_COMMON:
            logging.info("No calibration found, try to calibrate.")
            doCalibrate()
        currentAngle = doGetAngle()
        if currentAngle == ERROR_COMMON:
            logging.error("Could not perform initial calibration.")
            return ERROR_COMMON
        else:
            logging.info("Calibration successful")
        doSetup()
        if angle > 0:
            forward(STEP_DELAY, angleToSteps(angle))
        elif angle < 0:
            backwards(STEP_DELAY, angleToSteps(angle))
        newAngle = currentAngle + angle
        writeAngleFile(newAngle)
        return RESULT_OK
    except NoDeviceLibraryFoundException as e:
        raise # rethrow GPIO error
    except BoundaryException:
        logging.error("Requested angle outside bounds.")
        return ERROR_COMMON
    except:
        printDescription("Angle was not a floating point number")
        return ERROR_COMMON