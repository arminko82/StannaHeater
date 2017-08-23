#!/usr/bin/env python

# Armin Koefler, file created at 19.08.2017
# Helper code for regulator<i>.pi
# Main entry point for application. In the end shall interpret cmd line arguments in order to move
# the rotor by a certain amount (degree would be nice).
# Current finding: 512 steps equal a full rotation so that one degree is actually 0.703 degrees

from device_access import *
from device import *
from device_acces import tryLockDevice, unlockDevice

# Block of response codes for external callers
RESULT_OK = 0
ERROR_COMMON = 1
ERROR_DEVICE_IN_USE = 2

def shutdown(ignore1, ignore2):
    resetGpioState()
    sys.exit(0)

def main():
    if sys.argv == 0:
        print("No command line arguments")
TODO TODO TODO TODO TODO TODO print list of arguements TODO TODO TODO TODO TODO 
Modes:
 - turn clockwise by angle
 - turn counterclockwise by angle
 - get current angle
 - calibrate hardware by going counterclockwise will a button is pressed by the contraption 
   (there is no button at the moment, would need another GPIO pin set to input mode)
        return ERROR_COMMON
    
    if tryLockDevice() == False:
        print("Another process is accessing the device at the moment.")
        return ERROR_DEVICE_IN_USE

    try:
        setup()
        signal.signal(signal.SIGINT, shutdown)
        print("Waiting for a second ...")
        resetGpioState()
        time.sleep(1)
        GPIO.output(enable_pin, 1)
        print("Setting up ...")

        while True:
            delay = raw_input("Zeitverzoegerung (ms)?")
            steps = raw_input("Wie viele Schritte vorwaerts? ")
            forward(int(delay) / 1000.0, int(steps))
            steps = raw_input("Wie viele Schritte rueckwaerts? ")
            backwards(int(delay) / 1000.0, int(steps))
        return RESULT_OK
    finally:
        unlockDevice()

if __name__ == "__main__":
    main()

