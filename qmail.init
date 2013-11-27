#!/bin/sh
#
# qmail	Startup script for QmailToaster MTA
#
# chkconfig: 345 55 45
# description: Qmailtoaster MTA
#
# Udated May 19, 2006
# Nick Hemmesch <nick@ndhsoft.com>
#

# Source function library.
if [ -f /etc/init.d/functions ]; then
  . /etc/init.d/functions
elif [ -f /etc/rc.d/init.d/functions ]; then
  . /etc/rc.d/init.d/functions
fi

PATH=/var/qmail/bin:/usr/local/bin:/usr/bin:/bin
export PATH

case "$1" in
  start)
    # have a silent kill in case someone tries to start the service when it
    # is already running
    $0 stop >/dev/null 2>&1
    echo -n "Starting qmail-toaster: svscan"
    cd /var/qmail/supervise
    env - PATH="$PATH" svscan &
    echo $! > /var/run/qmail-svscan.pid
    touch /var/lock/subsys/qmail
    echo "."
    ;;
  stop)
    echo -n "Stopping qmail-toaster: svscan"
    kill `cat /var/run/qmail-svscan.pid`
    echo -n " qmail"
    svc -dx /var/qmail/supervise/*
    echo -n " logging"
    svc -dx /var/qmail/supervise/*/log
    echo "."
    rm -rf /var/run/qmail-svscan.pid
    rm -rf /var/lock/subsys/qmail
    ;;
  stat)
    cd /var/qmail/supervise
    svstat * */log
    ;;
  doqueue|alrm)
    echo "Sending ALRM signal to qmail-send."
    svc -a /var/qmail/supervise/send
    ;;
  queue)
    /var/qmail/bin/qmail-qstat
    /var/qmail/bin/qmail-qread
    ;;
  reload|hup)
    echo "Sending HUP signal to qmail-send."
    svc -h /var/qmail/supervise/send
    ;;
  pause)
    echo "Pausing qmail-send"
    svc -p /var/qmail/supervise/send
    echo "Pausing qmail-smtpd"
    svc -p /var/qmail/supervise/smtp
    ;;
  cont)
    echo "Continuing qmail-send"
    svc -c /var/qmail/supervise/send
    echo "Continuing qmail-smtpd"
    svc -c /var/qmail/supervise/smtp
    ;;
  restart)
    echo "Restarting qmail:"
    echo "* Stopping qmail-smtpd."
    svc -d /var/qmail/supervise/smtp
    echo "* Sending qmail-send SIGTERM and restarting."
    svc -t /var/qmail/supervise/send
    echo "* Restarting qmail-smtpd."
    svc -u /var/qmail/supervise/smtp
    ;;
  cdb)
    tcprules /etc/tcprules.d/tcp.smtp.cdb /etc/tcprules.d/tcp.smtp.tmp < /etc/tcprules.d/tcp.smtp
    chmod 644 /etc/tcprules.d/tcp.smtp*
    echo "Reloaded /etc/tcprules.d/tcp.smtp"
    if [ -f /var/qmail/bin/qmail-badmimetypes ] ; then
	/var/qmail/bin/qmail-badmimetypes;
	echo "Reloaded /var/qmail/control/badmimetypes.cdb";
    fi
    if [ -f /var/qmail/bin/qmail-badloadertypes ] ; then
	/var/qmail/bin/qmail-badloadertypes;
	echo "Reloaded /var/qmail/control/badloadertypes.cdb";
    fi
    if [ -f /var/qmail/bin/simscanmk ] ; then
        /var/qmail/bin/simscanmk -g >/dev/null 2>&1;
	echo "Reloaded /var/qmail/control/simversions.cdb";
	if [ -f /var/qmail/control/simcontrol ] ; then
           /var/qmail/bin/simscanmk >/dev/null 2>&1;
	   echo "Reloaded /var/qmail/control/simcontrol.cdb";
        fi
    fi
    ;;
  help)
    cat <<HELP 
   stop -- stops mail service (smtp connections refused, nothing goes out)
  start -- starts mail service (smtp connection accepted, mail can go out)
  pause -- temporarily stops mail service (connections accepted, nothing leaves)
   cont -- continues paused mail service
   stat -- displays status of mail service
    cdb -- rebuild the tcpserver cdb file for smtp
restart -- stops and restarts smtp, sends qmail-send a TERM & restarts it
doqueue -- sends qmail-send ALRM, scheduling queued messages for delivery
 reload -- sends qmail-send HUP, rereading locals and virtualdomains
  queue -- shows status of queue
   alrm -- same as doqueue
    hup -- same as reload
HELP
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|doqueue|reload|stat|pause|cont|cdb|queue|help}"
    exit 1
    ;;
esac
 
exit 0
