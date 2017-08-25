#!/bin/bash

# Uninstall script for StannaHeater by Armin Köfler, 25.08.2017
# Script shall be run as super user


userdel www-regulator
groupdel www-regulator


#n-0 Uninstall HTTP server 
apt-get remove lighttpd
