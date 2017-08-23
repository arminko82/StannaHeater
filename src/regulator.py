#!/usr/bin/env python

# Armin Koefler, file created at 19.08.2017
# Helper code for regulator<i>.pi
# Main entry point for application. In the end shall interpret cmd line arguments in order to move
# the rotor by a certain amount (degree would be nice).
# Current finding: 512 steps equal a full rotation so that one degree is actually 0.703 degrees

from device import *
from device_acces import tryLockDevice, unlockDevice
from Carbon.AppleEvents import kAEAutoDown

# Block of response codes for external callers
RESULT_OK = 0
ERROR_COMMON = 1
ERROR_DEVICE_IN_USE = 2

def shutdown(ignore1, ignore2):
    resetGpioState()
    sys.exit(0)

def printDescription(error):
    print("""{0}
             Call this using one of the following arguments:
               -calibrate:    Reset the device by rotating counterclockwise till the clipper button is pushed 
               -getAngle:     Returns the current angle to std out.
               -turn <angle>: Rotates the rotor by an given angle that is interpreted 
                              as floating point. A positive angle is interpreted 
                              as clockwise.
              Return values:
                {1} - Success
                {2} - Some error that is not specified exactly
                {3} - Device is currently in use.
                f.f - In case of success in mode -getAngle the current angle is returned as floating point.
              Example: python regulator -calibrate""".format(error, RESULT_OK, ERROR_COMMON, ERROR_DEVICE_IN_USE))
    
# Parses command and executes. Returns error code or success or an angle if in command mode -getAngle
def main():
    if sys.argv == 0:
        printDescription("Error: No command line arguments")
        cmd = sys.argv[0]
    elif sys.argv == 1:
        if cmd == "-calibrate":
            return doCalibrate()
        elif cmd == "-getAngle":
            return doGetAngle()
        else:
            printDescription("Command '{0}' not known".format(cmd))
    elif sys.argv == 2:
        if cmd == "-turn":
            return doTurn(argv[1])
        else:
            printDescription("Command '{0}' not known".format(cmd))
    else:
            printDescription("Command '{0}' not known or invalid number of arguments".format(cmd))
    return ERROR_COMMON
        
def doCalibrate():
    print("todo")
    
def doGetAngle():
    print("todo")
    
def doTurn(angleString):
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

