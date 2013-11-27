#!/bin/sh

umask 0077 || exit 0

export PATH="/sbin:/usr/sbin:/bin:/usr/bin:/usr/local/bin/ssl"

openssl genrsa -out /var/qmail/control/rsa512.new 512 2>&1 > /dev/null
chmod 644 /var/qmail/control/rsa512.new 2>&1 > /dev/null
chown root:qmail /var/qmail/control/rsa512.new 2>&1 > /dev/null
mv -f /var/qmail/control/rsa512.new /var/qmail/control/rsa512.pem 2>&1 > /dev/null

openssl dhparam -2 -out /var/qmail/control/dh512.new 512 2>&1 > /dev/null
chmod 644 /var/qmail/control/dh512.new 2>&1 > /dev/null
chown root:qmail /var/qmail/control/dh512.new 2>&1 > /dev/null
mv -f /var/qmail/control/dh512.new /var/qmail/control/dh512.pem 2>&1 > /dev/null

openssl dhparam -2 -out /var/qmail/control/dh1024.new 1024 2>&1 > /dev/null
chmod 644 /var/qmail/control/dh1024.new 2>&1 > /dev/null
chown root:qmail /var/qmail/control/dh1024.new 2>&1 > /dev/null
mv -f /var/qmail/control/dh1024.new /var/qmail/control/dh1024.pem 2>&1 > /dev/null
