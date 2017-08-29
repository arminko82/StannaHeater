#!/usr/bin/env python

# Armin Koefler, file created at 24.08.2017
# Collects constants used at various places


# Block of response codes for external callers
RESULT_OK = 0
ERROR_COMMON = 1
ERROR_DEVICE_IN_USE = 2
# Full collection of error response codes
RESPONSES = [RESULT_OK, ERROR_COMMON, ERROR_DEVICE_IN_USE]
#common state
# Ensures that setup is only performed once.
mSetupDone = False