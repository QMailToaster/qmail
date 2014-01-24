#!/bin/sh
QMAILDUID=`id -u vpopmail`
NOFILESGID=`id -g vpopmail`
MAXSMTPD=`cat /var/qmail/control/concurrencyincoming`
SPAMDYKE="/usr/bin/spamdyke"
SPAMDYKE_CONF="/etc/spamdyke/spamdyke.conf"
SMTPD="/var/qmail/bin/qmail-smtpd"
TCP_CDB="/etc/tcprules.d/tcp.smtp.cdb"
HOSTNAME=`hostname`
VCHKPW="/home/vpopmail/bin/vchkpw"
REQUIRE_AUTH=0

exec /usr/bin/softlimit -m 20000000 \
     /usr/bin/tcpserver -v -R -H -l $HOSTNAME -x $TCP_CDB -c "$MAXSMTPD" \
     -u "$QMAILDUID" -g "$NOFILESGID" 0 smtp \
     $SPAMDYKE --config-file $SPAMDYKE_CONF \
     $SMTPD $VCHKPW /bin/true 2>&1
