#!/bin/bash

# Setup script for StannaHeater by Armin Koefler, 25.08.2017
# Script shall be run as super user

#1 Install HTTP server 
apt-get -y install lighttpd

#2 Install PHP
apt-get -y install php5-common php5-cgi php5

#3 Configure HTTP server
mv /etc/lighttpd/lighttpd.conf /etc/lighttpd/lighttpd.conf.original
cp lighttpd.conf /etc/lighttpd/lighttpd.conf 

#4 Setup server group and user
groupadd www-regulator
useradd -g www-regulator www-regulator

#5 create log folders
mkdir /var/log/StannaHeater
mkdir /var/log/StannaHeater
chown -R www-regulator:www-regulator /var/log/StannaHeater

#6 Deploy website
mkdir /var/www/regulator
cp -r ../www/* /var/www/regulator/
chown -R www-regulator:www-regulator /var/www/regulator

#7 Register HTTP server to auto-start  !TODO!