#!/bin/sh
LOGSIZE=`cat /var/qmail/control/logsize`
LOGCOUNT=`cat /var/qmail/control/logcount`
exec /usr/bin/setuidgid qmaill \
     /usr/bin/multilog t s$LOGSIZE n$LOGCOUNT \
     /var/log/qmail/submission 2>&1
