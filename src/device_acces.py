#!/usr/bin/env python

# Armin Koefler, file created at 19.08.2017
# Helper code for regulator<i>.pi
# The present code allows checking for other processes that are currently interacting 
#  with the stepper motor to ensure mutually exclusive hardware access

import fcntl

# lock file definition
mDeviceLock = "/var/lock/regulator.lock"

# Tries to lock the device. Boolean return value describes result.
def tryLockDevice():
    lockfile = open(mDeviceLock, 'w')       
    try:
        fcntl.lockf(lockfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
        print("Acquired device lock successfully")
        return True
    except:
        print("Acquired device lock successfully")
        return False

# Unlocks the device that previously has been locked by the current process. 
# No error check upon previous lock acquisition.
def unlockDevice():
        lockfile = open(mDeviceLock, 'w')
        fcntl.lockf(lockfile, fcntl.LOCK_UN)
        print("Unlocked device")
        