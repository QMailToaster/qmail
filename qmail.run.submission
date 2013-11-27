#!/bin/sh
QMAILDUID=`id -u vpopmail`
NOFILESGID=`id -g vpopmail`
MAXSMTPD=`cat /var/qmail/control/concurrencyincoming`
SMTPD="/var/qmail/bin/qmail-smtpd"
TCP_CDB="/etc/tcprules.d/tcp.smtp.cdb"
HOSTNAME=`hostname`
VCHKPW="/home/vpopmail/bin/vchkpw"
export REQUIRE_AUTH=1

exec /usr/bin/softlimit -m 12000000 \
    /usr/bin/tcpserver -v -R -H -l $HOSTNAME -x $TCP_CDB -c "$MAXSMTPD" \
    -u "$QMAILDUID" -g "$NOFILESGID" 0 587 \
    $SMTPD $VCHKPW /bin/true 2>&1
