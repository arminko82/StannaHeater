#!/usr/bin/env python

# Armin Koefler, file created at 24.08.2017
# This file contains the higher level functions that are invoked by the main method

import sys
from device import *
from const_vars import *
from custom_exceptions import NoDeviceLibraryFoundException

# The file holds the currently known angle. It is reset to 0 when doCalibrate is called which
# moves the rotor to the left-most location and rewrites this file. Any call to doTurn updates the 
# file's value.
ANGLE_FILE = "./current_angle.dat"
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
        print(ex)
        return ERROR_COMMON
        
# Reads the current rotor angle from the angle file.
# Returns ERROR_COMMON if the file is not present, else to file content.
# If the files content equals ERROR_COMMON exactly something bad has happened.
# doTurn()  should ensure that no matter what angle is the current on
# ERROR_COMMON is never written
# but at least differs the smallest epsilon possible from it.    
def doGetAngle():
    try:
        with open(ANGLE_FILE) as file:
            return float(file.readline()) # culture invariant?
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
        currentAngle = doGetAngle()
        if currentAngle == ERROR_COMMON:
            print("No calibration found, try to calibrate.")
            doCalibrate()
        currentAngle = doGetAngle()
        if currentAngle == ERROR_COMMON:
            print("Could not perform initial calibration.")
            return ERROR_COMMON
        else:
            print("Calibration successful")
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
    except:
        printDescription("Angle was not a floating point number")
        return ERROR_COMMON