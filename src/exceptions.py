#!/usr/bin/env python

# Armin Koefler, file created at 24.08.2017
# This file collects exceptions used in this project

# The app is run either on a non-raspi device of GPIO libraries are not installed
class NoDeviceLibraryFoundException(Exception):
    #ctor passes to base
    def __init__(self, message):
        super(NoDeviceLibraryFoundException, self).__init__(message)