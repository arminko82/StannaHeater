#!/usr/bin/env python

# Armin Koefler, file created at 19.08.2017
# Helper code for regulator<i>.pi
# Main entry point for application. Cmd line arguments are interpreted in order control the heaters state or
# to get the current state.
# Current finding: 512 steps equal a full rotation so that one degree is actually 0.703 degrees

import sys
import signal
import logging
from const_vars import mSetupDone, ERROR_DEVICE_IN_USE, ERROR_COMMON, RESULT_OK
from device_access import tryLockDevice, unlockDevice
from logic import doCalibrate, doGetAngle, doTurn
from custom_exceptions import NoDeviceLibraryFoundException

LOG_FILE = "/var/log/StannaHeater/backend.log"

# Event handler which is run when the current process ends based on a SIGINT.
# Cleans up.
def shutdown(ignore1, ignore2):
    resetGpioState()

# Prints the how to use text to console. Optionally shows an error information in the first line.
def printDescription(error):
    print("""{0}
             Call this using one of the following arguments:
               -calibrate:    Reset the device by rotating counterclockwise till 
                              the clipper button is pushed 
               -getAngle:     Returns the current angle to std out.
               -turn <angle>: Rotates the rotor by an given angle that is interpreted 
                              as floating point. A positive angle is interpreted 
                              as clockwise.
              Return values:
                {1} - Success
                {2} - Some error that is not specified exactly
                {3} - Device is currently in use.
                f.f - In case of success in mode -getAngle the current 
                      angle is returned as floating point.
              Example: python regulator -calibrate""".format(error, RESULT_OK, ERROR_COMMON, ERROR_DEVICE_IN_USE))
    
# Parses command and executes. Returns error code or success or an angle if in command mode -getAngle
# In order to get the return value back to the php layer each return value is
# printed to stdout before the value is actually returned.
def main():
    logging.basicConfig(filename=LOG_FILE,level=logging.DEBUG,format='%(asctime)s %(message)s')
    global mSetupDone
    mSetupDone = False
    if tryLockDevice() == False:
        logging.error("Another process is accessing the device at the moment. Rejecting new request.")
        print ERROR_DEVICE_IN_USE
        return ERROR_DEVICE_IN_USE
    try:
        signal.signal(signal.SIGINT, shutdown)
        cmd = ""
        argc = len(sys.argv)
        if argc == 1:
            printDescription("Error: No command line arguments")
        elif argc == 2:
            cmd = sys.argv[1]
            if cmd == "-calibrate":
                result = doCalibrate()
                print result
                return result
            elif cmd == "-getAngle":
                result = doGetAngle()
                print result
                return result
            else:
                printDescription("Command '{0}' not known".format(cmd))
        elif argc == 3:
            cmd = sys.argv[1]
            if cmd == "-turn":
                result = doTurn(argv[2])
                print result 
                return result
            else:
                printDescription("Command '{0}' not known".format(cmd))
        else:
                printDescription("Command '{0}' not known or invalid number of arguments".format(cmd))
        print ERROR_COMMON
        return ERROR_COMMON
    except NoDeviceLibraryFoundException:
        logging.error("Error: Current computer is either not a raspberry pi or no RPi.GPIO libraries are installed.")
        print ERROR_COMMON
    except Exception as x:
        logging.error("Unhandled error: " + x)
        print ERROR_COMMON
    finally:
        if mSetupDone:
            resetGpioState()
        unlockDevice()
        
# Some strange entry point found in this language
if __name__ == "__main__":
    main()