Name:      qmail
Summary:   qmail Mail Transfer Agent
Version:   1.03
Release:   1%{?dist}
License:   Public Domain / GNU
Group:     System/Servers
URL:       http://www.qmail.org/
Vendor:    QmailToaster
Packager:  Eric Shubert <qmt-build@datamatters.us>
Source:    http://cr.yp.to/software/%{name}-%{version}.tar.gz
Source1:   qmail.dh_key
Source2:   qmail.rc
Source3:   qmail.init
Source4:   badmimetypes
Source5:   badloadertypes
Source6:   badmailfrom
Source7:   badmailto
Source8:   concurrencyincoming
Source9:   concurrencyremote
Source10:  databytes
Source11:  defaultdelivery
Source12:  locals
Source13:  logcount
Source14:  logsize
Source15:  queuelifetime
Source16:  spfbehavior
Source17:  smtpgreeting
#Source18:  qmail.run.send
#Source19:  qmail.run.send.log
Source20:  qmail.run.smtp
Source21:  qmail.run.smtp.log
Source22:  qmail.run.submission
Source23:  qmail.run.submission.log
Source24:  qmail.tcp.smtp
Source25:  makecert.sh
Patch0:    qmailtoaster-1.3.2.patch
Patch1:    qmailtoaster-chkuser.patch
Patch2:    qmail-require_auth.patch
Patch3:    qmail-dk-0.6.beta.2.patch
Patch4:    qmail-smtpd-spf-qq-reject-logging.patch
Patch5:    qmail-srs-qt-0.5.patch
Patch6:    qmailtoaster-big-dns.patch
Patch7:    qmail-smtpd-linefeed.patch
Patch8:    qmail-empf.patch
Patch9:    qmail-vpopmail-devel.patch
Patch10:   qmail-uids.patch
Patch11:   qmail-nocram.patch
Patch12:   splogger-nostamp.patch
BuildRequires: krb5-devel >= 1.5
BuildRequires: libdomainkeys-static
BuildRequires: libsrs2-static
BuildRequires: libvpopmail-static
BuildRequires: openssl-devel >= 0.9.8
Requires:  daemontools
Requires:  openssl >= 0.9.8
Requires:  sh-utils
Requires:  spamdyke
Requires:  ucspi-tcp
Requires:  vpopmail
Provides:  MTA
Provides:  smtpdaemon
Provides:  sendmail
Obsoletes: exim
Obsoletes: postfix
Obsoletes: qmail-toaster
Obsoletes: qmail-toaster-doc
BuildRoot: %{_topdir}/BUILDROOT/%{name}-%{version}-%{release}.%{_arch}

%define ccflags       %{optflags} -DTLS=20060104 -I/usr/include/libvpopmail
%define crontab       %{_sysconfdir}/crontab
%define _initpath     %{_sysconfdir}/rc.d/init.d
%define debug_package %{nil}
%define qdir          /var/%{name}
%define qbin          %{qdir}/bin
%define qcon          %{qdir}/control
%define qdoc          %{qdir}/doc
%define qman          %{qdir}/man
%define qque          %{qdir}/queue
%define qsup          %{qdir}/supervise
%define qlog          /var/log/%{name}

#-------------------------------------------------------------------------------
%description
#-------------------------------------------------------------------------------
qmail is a small, fast, secure replacement for the sendmail package, which is
the program that actually receives, routes, and delivers electronic mail.

qmailtoaster-1.3.2.patch            Thu Feb 24, 2011

~~~~~~~~~~~~~ Patches Applied ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

qmail-1.03 patched to netqmail-1.05
-----------------------------------
QMAILQUEUE patch
qmail-local patch
local IP 0.0.0.0 patch
sendmail -f patch

Andrew St. Jean - qregex-starttls-2way-auth-20060305
http://www.arda.homeunix.net/store/qmail/

Frederik Vermeulen - qmail-tls 20060104
http://inoa.net/qmail-tls/

Erwin Hoffman - SMTP-AUTH Version 0.57
http://www.fehcom.de/qmail/

Robert Sander - qmail-remote-auth
http://www.ornl.gov/lists/mailing-lists/qmail/2002/03/msg00091.html

Antonio Nati - chkuser-2.0.9
http://opensource.interazioni.it/qmail/chkuser.html

Chris christophe@saout.de - qmail-spf.rc5 
http://www.saout.de/misc/spf/

Russ Nelson - qmail-1.03-dk-0.54 domainkeys patch
http://www.qmail.org/qmail-1.03-dk-0.54.patch

Jeremy Kister - qmail-dk-0.54-auth patch
http://jeremy.kister.net/code/qmail-dk-0.54-auth.patch

Erwin Hoffmann - warlord-1.3.11  
http://www.fehcom.de/qmail/

Bill Shupp - netqmail-maildir++.patch
http://shupp.org/patches/netqmail-maildir++.patch

Bill Shupp - custom-smtp-reject
http://www.shupp.org/patches/custom.patch

Johannes Erdfelt - big-concurrency patch
http://qmail.org/big-concurrency.patch

Inter7 - qmailtap-1.1 tap
http://www.inter7.com/qmailtap/qmail-tap-1.1.diff

Alexey Loukianov - Log Enhancement Patch

Jean-Paul van de Plasse - REQUIRE_AUTH Patch

Marcelo Coelho - qmail-srs-0.4.patch
http://opensource.mco2.net/qmail/srs/

SMTP Linefeed Patch

Big DNS Patch

Inter7 - eMPF 1.0
http://www.inter7.com/?page=empf-install

#-------------------------------------------------------------------------------
%prep
#-------------------------------------------------------------------------------

%setup -q

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p0
%patch5 -p1
%patch6 -p0
%patch7 -p0
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1

#-------------------------------------------------------------------------------
%build
#-------------------------------------------------------------------------------
echo "gcc %{ccflags}"     >conf-cc
echo "gcc -s %{optflags}" >conf-ld

# shubes 11/18/2013 - this is a hack
# TODO: get qmail-dk to pick up libdomainkeys.a in a more normal way
%ifarch x86_64
  sed -i 's|LIB_DK=/usr/lib/|LIB_DK=/usr/lib64/|' Makefile
%endif

make clean
make compile makelib
make it man

#-------------------------------------------------------------------------------
%install
#-------------------------------------------------------------------------------
rm -rf %{buildroot}
install -d %{buildroot}%{qdir}
install -d %{buildroot}%{qdir}/alias
install -d %{buildroot}%{qbin}
install -d %{buildroot}%{qcon}
install -d %{buildroot}%{qcon}/domainkeys
install -d %{buildroot}%{qdir}/owners
install -d %{buildroot}%{qdir}/users
install -d %{buildroot}%{qman}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sbindir}

for i in bin boot control doc man users; do
  install -d -m755 %{buildroot}%{qdir}/$i
done

for i in man1 man5 man7 man8; do
  install -d -m755 %{buildroot}%{qman}/$i
done

for i in cat1 cat5 cat7 cat8; do
  install -d -m755 %{buildroot}%{qman}/$i
done

#-------------------------------------------------------------------------------
install -d -m700 %{buildroot}%{qsup}

#for i in send smtp submission; do
for i in smtp submission; do
  install -d -m1751 %{buildroot}%{qsup}/$i
  install -d -m751  %{buildroot}%{qsup}/$i/log
  install -d -m751  %{buildroot}%{qsup}/$i/supervise
done

#-------------------------------------------------------------------------------
install -d -m750  %{buildroot}%{qque}
install -d -m2755 %{buildroot}%{qdir}/alias

install -d -m755  %{buildroot}%{qlog}
#install -d -m755  %{buildroot}%{qlog}/send
install -d -m755  %{buildroot}%{qlog}/smtp
install -d -m755  %{buildroot}%{qlog}/submission

mkdir -p %{buildroot}%{_initpath}

#-------------------------------------------------------------------------------
for i in bouncesaying condredirect datemail elq except forward instcheck \
         maildir2mbox maildirmake maildirwatch mailsubj \
         pinq predate preline qail qbiff
do
  install -m755 %{_builddir}/%{name}-%{version}/$i %{buildroot}%{qbin}
done

for i in qmail-clean qmail-getpw qmail-local qmail-pw2u \
         qmail-remote qmail-rspawn qmail-send splogger
do
  install -m711 %{_builddir}/%{name}-%{version}/$i %{buildroot}%{qbin}
done

for i in qmail-lspawn qmail-newmrh qmail-newu qmail-start
do
  install -m700 %{_builddir}/%{name}-%{version}/$i %{buildroot}%{qbin}
done

for i in qmail-dk qmail-queue
do
  install -m4711 %{_builddir}/%{name}-%{version}/$i %{buildroot}%{qbin}
done

for i in qmail-badmimetypes qmail-badloadertypes qmail-inject \
         qmail-qmqpc qmail-qmqpd qmail-qmtpd qmail-qread qmail-qstat \
         qmail-showctl qmail-smtpd qmail-tcpok qmail-tcpto qreceipt \
         qsmhook sendmail spfquery tcp-env srsfilter
do
  install -m755 %{_builddir}/%{name}-%{version}/$i %{buildroot}%{qbin}
done

# install docs
#-------------------------------------------------------------------------------
for i in BIN.README BLURB BLURB2 BLURB3 BLURB4 CHANGES CHKUSER.changelog \
         CHKUSER.copyright CHKUSER.log_format CHKUSER.readme CHKUSER.running \
         chkuser_settings.h FAQ FILES FILES.warlord HISTORY.warlord \
         INSTALL INSTALL.alias INSTALL.ctl INSTALL.ids INSTALL.maildir \
         INSTALL.mbox INSTALL.vsm INSTALL.warlord INTERNALS PIC.local2alias \
         PIC.local2ext PIC.local2local PIC.local2rem PIC.local2virt \
         PIC.nullclient PIC.relaybad PIC.relaygood PIC.rem2local \
         README README.srs README.auth README.domainkeys README.qregex \
         README.remote-auth README.starttls README.tap README.warlord \
         REMOVE.binmail REMOVE.sendmail SECURITY SYSDEPS THANKS THOUGHTS \
         TODO UPGRADE VERSION ChangeLog.empf README.empf
do
  install -m644 %{_builddir}/%{name}-%{version}/$i %{buildroot}%{qdoc}
done

for i in qreceipt condredirect mailsubj except maildirmake preline tcp-env \
         bouncesaying maildir2mbox qbiff forward maildirwatch
do
  install -m644 %{_builddir}/%{name}-%{version}/$i.1 %{buildroot}%{qman}/man1
  install -m644 %{_builddir}/%{name}-%{version}/$i.0 %{buildroot}%{qman}/cat1
done

for i in qmail-users maildir qmail-header envelopes mbox tcp-environ \
         qmail-control qmail-log addresses dot-qmail
do
  install -m644 %{_builddir}/%{name}-%{version}/$i.5 %{buildroot}%{qman}/man5
  install -m644 %{_builddir}/%{name}-%{version}/$i.0 %{buildroot}%{qman}/cat5
done

for i in qmail-limits forgeries qmail
do
  install -m644 %{_builddir}/%{name}-%{version}/$i.7 %{buildroot}%{qman}/man7
  install -m644 %{_builddir}/%{name}-%{version}/$i.0 %{buildroot}%{qman}/cat7
done

for i in qmail-badmimetypes qmail-badloadertypes qmail-tcpto qmail-qread \
         splogger qmail-start qmail-qmqpc qmail-newu qmail-tcpok \
         qmail-inject qmail-clean qmail-getpw qmail-command qmail-showctl \
         qmail-rspawn qmail-smtpd qmail-qmqpd qmail-qstat qmail-pw2u \
         qmail-qmtpd qmail-queue qmail-lspawn qmail-newmrh \
         qmail-local qmail-send qmail-remote
do
  install -m644 %{_builddir}/%{name}-%{version}/$i.8 %{buildroot}%{qman}/man8
  install -m644 %{_builddir}/%{name}-%{version}/$i.0 %{buildroot}%{qman}/cat8
done

install %{_builddir}/%{name}-%{version}/qmail-dk.8 %{buildroot}%{qman}/man8

# install boot
#-------------------------------------------------------------------------------
for i in home home+df binm1 binm2+df proc+df \
         binm2 binm3 proc binm3+df binm1+df
do
  install -m755 %{_builddir}/%{name}-%{version}/$i %{buildroot}%{qdir}/boot
done

# build the queue
#-------------------------------------------------------------------------------
for i in bounce info intd local lock mess pid remote todo
do
  install -d %{buildroot}%{qque}/$i
done

for d in info local mess remote
do
  for i in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22; do
    install -d %{buildroot}%{qque}/$d/$i
  done
done

# the rest
#-------------------------------------------------------------------------------
touch %{buildroot}%{qque}/lock/sendmutex
touch %{buildroot}%{qque}/lock/tcpto

# trigger will be changed to a named pipe in the %post section
# this is because fuse-unionfs doesn't handle named pipes (yet)
#mkfifo -m 0622 %{buildroot}%{qque}/lock/trigger
touch %{buildroot}%{qque}/lock/trigger

install -m755 instcheck   %{buildroot}%{qbin}
install -m755 config-fast %{buildroot}%{qbin}

#-------------------------------------------------------------------------------
install %{SOURCE1}  %{buildroot}%{qbin}/dh_key
install %{SOURCE2}  %{buildroot}%{qdir}/rc
install %{SOURCE3}  %{buildroot}%{_initpath}/qmail

# configure qmail /var/qmail/control/*
#-------------------------------------------------------------------------------

install %{SOURCE4}  \
        %{SOURCE5}  \
        %{SOURCE6}  \
        %{SOURCE7}  \
        %{SOURCE8}  \
        %{SOURCE9}  \
        %{SOURCE10} \
        %{SOURCE11} \
        %{SOURCE12} \
        %{SOURCE13} \
        %{SOURCE14} \
        %{SOURCE15} \
        %{SOURCE16} \
        %{SOURCE17} \
      %{buildroot}%{qcon}

pushd %{buildroot}%{qcon}
  touch defaultdomain \
        defaulthost \
        me \
        plusdomain \
        policy \
        rcpthosts \
        smtproutes
popd

# Make users dir and files
#-------------------------------------------------------------------------------
pushd %{buildroot}%{qdir}/users
  touch cdb
  echo "." > assign
  chmod 644 *
popd

# sendmail compatability and qmailctl links
#-------------------------------------------------------------------------------
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_libdir}
pushd %{buildroot}%{_sbindir}
  ln -s ../..%{qbin}/sendmail sendmail
popd
pushd %{buildroot}%{_libdir}
  ln -s ../..%{qbin}/sendmail sendmail
popd
pushd %{buildroot}%{_bindir}
  ln -s ../..%{_initpath}/qmail qmailctl
popd

# Install supervise
#-------------------------------------------------------------------------------
#mkdir -p %{buildroot}%{qsup}/send/log
mkdir -p %{buildroot}%{qsup}/smtp/log
mkdir -p %{buildroot}%{qsup}/submission/log

#install %{SOURCE18}  %{buildroot}%{qsup}/send/run
#install %{SOURCE19}  %{buildroot}%{qsup}/send/log/run
install %{SOURCE20}  %{buildroot}%{qsup}/smtp/run
install %{SOURCE21}  %{buildroot}%{qsup}/smtp/log/run
install %{SOURCE22}  %{buildroot}%{qsup}/submission/run
install %{SOURCE23}  %{buildroot}%{qsup}/submission/log/run

# TODO: this can be done w/out perl
%ifarch x86_64
   %define spath %{buildroot}%{qsup}
   %{__perl} -pi -e "s|20000000|64000000|g" %{spath}/smtp/run
   %{__perl} -pi -e "s|12000000|50000000|g" %{spath}/submission/run
%endif

install -Dp %{SOURCE24} %{buildroot}%{_sysconfdir}/tcprules.d/tcp.smtp

# Make skel dirs
#-------------------------------------------------------------------------------
mkdir -p %{buildroot}%{_sysconfdir}/skel/Maildir/{cur,new,tmp}
echo "./Maildir/" > %{buildroot}%{_sysconfdir}/skel/.qmail

find %{buildroot}%{qman} -type f -exec bzip2 -9f {} \;

install %{SOURCE25}  %{buildroot}%{qbin}/.

# this is a %ghost file, which is generated in %post
touch %{buildroot}%{qcon}/servercert.pem
 
pushd %{buildroot}%{qcon}
  ln -s servercert.pem clientcert.pem
popd

#-------------------------------------------------------------------------------
%clean
#-------------------------------------------------------------------------------
rm -rf %{buildroot}

#-------------------------------------------------------------------------------
%pre
#-------------------------------------------------------------------------------

# Add users and groups as per Life With Qmail
#-------------------------------------------------------------------------------
echo " Adding qmailtoaster users and groups."
if [ -z "`/usr/bin/id -g nofiles 2>/dev/null`" ]; then
	/usr/sbin/groupadd -g 2107 -r nofiles 2>&1 || :
fi
if [ -z "`/usr/bin/id -g qmail 2>/dev/null`" ]; then	
	/usr/sbin/groupadd -g 2108 -r qmail 2>&1 || :
fi

if [ -z "`/usr/bin/id -u alias 2>/dev/null`" ]; then
	/usr/sbin/useradd -u 7790 -r -M -d %{qdir}/alias -s /sbin/nologin -c "qmail alias" -g qmail alias  2>&1 || :
fi
if [ -z "`/usr/bin/id -u qmaild 2>/dev/null`" ]; then
	/usr/sbin/useradd -u 7791 -r -M -d %{qdir} -s /sbin/nologin -c "qmail daemon" -g qmail qmaild  2>&1 || :
fi
if [ -z "`/usr/bin/id -u qmaill 2>/dev/null`" ]; then
	/usr/sbin/useradd -u 7792 -r -M -d %{qdir} -s /sbin/nologin -c "qmail logger" -g qmail qmaill  2>&1 || :
fi
if [ -z "`/usr/bin/id -u qmailp 2>/dev/null`" ]; then
	/usr/sbin/useradd -u 7793 -r -M -d %{qdir} -s /sbin/nologin -c "qmail passwd" -g qmail qmailp  2>&1 || :
fi
if [ -z "`/usr/bin/id -u qmailq 2>/dev/null`" ]; then
	/usr/sbin/useradd -u 7794 -r -M -d %{qdir} -s /sbin/nologin -c "qmail queue" -g qmail qmailq  2>&1 || :
fi
if [ -z "`/usr/bin/id -u qmailr 2>/dev/null`" ]; then
	/usr/sbin/useradd -u 7795 -r -M -d %{qdir} -s /sbin/nologin -c "qmail remote" -g qmail qmailr  2>&1 || :
fi
if [ -z "`/usr/bin/id -u qmails 2>/dev/null`" ]; then
	/usr/sbin/useradd -u 7796 -r -M -d %{qdir} -s /sbin/nologin -c "qmail send" -g qmail qmails  2>&1 || :
fi


#-------------------------------------------------------------------------------
%preun
#-------------------------------------------------------------------------------

if [ "$1" = 0 ]; then

# stop qmail from automatically starting
chkconfig --del qmail

# Remove users and groups
userdel alias 2> /dev/null
userdel qmaild 2> /dev/null
userdel qmaill 2> /dev/null
userdel qmailp 2> /dev/null
userdel qmailq 2> /dev/null
userdel qmailr 2> /dev/null
userdel qmails 2> /dev/null
groupdel nofiles 2> /dev/null
groupdel qmail 2> /dev/null	
echo " Removed qmail-toaster users and groups."

# Remove cron job
grep -v ' * * * root %{qbin}/dh_key' %{crontab} > %{crontab}.new
mv -f %{crontab}.new %{crontab}
echo " Removed TLS key cron job."

# Remove qmail man path
if [ -f /etc/man.config ]; then
  grep -v 'MANPATH  /var/qmail/man' /etc/man.config > /etc/man.config.new
  mv -f /etc/man.config.new /etc/man.config
  echo " Removed qmail-toaster from MANPATH."
fi

fi

#-------------------------------------------------------------------------------
%post
#-------------------------------------------------------------------------------

# stop qmail send and move supervise scripts if present
#oldsenddir=/var/qmail/supervise/send
#if [ ! -z "$(which svc 2>/dev/null)" ] \
#      && [ -d "$oldsenddir" ]; then
#  svc -d $oldsenddir
#  mv $oldsenddir /root/send.supervise
#fi

mv -f %{qbin}/qmail-queue %{qbin}/qmail-queue.orig
ln -s %{qbin}/qmail-dk %{qbin}/qmail-queue
chmod 4711 %{qbin}/qmail-queue.orig

if [ $1 = "1" ]; then

# Get hostname and parse it for following operations
#-------------------------------------------------------------------------------
defaultHost=`hostname -s`
defaultHostname=`hostname -f`
defaultDomain=`hostname -f | perl -ne "s/.*\.([a-z0-9-]+\.[a-z]+)$/\1/i;" -e "print lc"`

echo $defaultHostname  > %{qcon}/me
echo $defaultDomain    > %{qcon}/defaultdomain
echo $defaultDomain    > %{qcon}/defaulthost
echo $defaultDomain    > %{qcon}/plusdomain
echo $defaultHostname >> %{qcon}/rcpthosts
echo $defaultHostname >> %{qcon}/locals
echo "$defaultHostname - Welcome to Qmail Toaster Ver. %{version}-%{release} SMTP Server"              > %{qcon}/smtpgreeting

# Make postmaster the default address for aliases
#-------------------------------------------------------------------------------
echo "&postmaster@$defaultDomain"	> %{qdir}/alias/.qmail-postmaster
echo "&postmaster@$defaultDomain"	> %{qdir}/alias/.qmail-mailer-daemon
echo "&postmaster@$defaultDomain"	> %{qdir}/alias/.qmail-root
chown alias:nofiles %{qdir}/alias/.qmail*
chmod 644 %{qdir}/alias/.qmail*

# Compile default tcp.smtp
#-------------------------------------------------------------------------------
if [ -f /usr/bin/tcprules ]; then
  echo "Compiling default cdb files in %{_sysconfdir}/tcprules.d..."
  %{_sysconfdir}/rc.d/init.d/qmail cdb
fi

fi
# done with initial install

# Add qmail man dir to man path
#-------------------------------------------------------------------------------
if [ -f /etc/man.config ]; then
   if ! grep 'MANPATH  /var/qmail/man' /etc/man.config > /dev/null; then
     echo " Adding qmail-toaster to MANPATH."
     echo "MANPATH  /var/qmail/man" >> /etc/man.config
   fi
fi

# Install cron-job to keep temp keys current
#-------------------------------------------------------------------------------
if ! grep ' * * * root %{qbin}/dh_key' %{crontab} > /dev/null; then
  echo " Adding cron job for TLS keys."
  echo "" >> %{crontab}
  echo "01 01 * * * root %{qbin}/dh_key 2>&1 > /dev/null" >> %{crontab}
fi

# Create queue/lock/trigger, but only if not installing in a sandbox
# This is necessary because fuse-unionfs does not (yet) support fifo files.
#-------------------------------------------------------------------------------
if [ ! -f /boot/.qtp-sandbox ]; then
  echo " Creating queue/lock/trigger named pipe."
  rm -f %{qque}/lock/trigger
  mkfifo -m 0622 %{qque}/lock/trigger
  chown qmails:qmail %{qque}/lock/trigger
else
  echo " NOT Creating queue/lock/trigger named pipe."
fi

./%{qbin}/qmail-badmimetypes
echo " Compiling badmimetypes."
./%{qbin}/qmail-badloadertypes
echo " Compiling badloadertypes."

touch  %{qcon}/tlsserverciphers
rm -fr %{qcon}/tlsclientciphers 2>&1 > /dev/null
echo " Making tlsserverciphers."
./%{_bindir}/openssl ciphers 'MEDIUM:HIGH:!SSLv2:!MD5:!RC4:!3DES' \
               > %{qcon}/tlsserverciphers
chown root:qmail %{qcon}/tlsserverciphers
chmod 644        %{qcon}/tlsserverciphers

echo " Linking tlsserverciphers to tlsclientciphers."
ln -s %{qcon}/tlsserverciphers %{qcon}/tlsclientciphers

echo " Making SSL certs."
yes "" | ./%{qbin}/makecert.sh

echo " Making dh_keys."
./%{qbin}/dh_key

# Make start
chkconfig --add qmail
chkconfig qmail on

#-------------------------------------------------------------------------------
%postun
#-------------------------------------------------------------------------------

if [ "$1" = 0 ]; then
 rm -f  /var/qmail/control/*.cdb
 rm -fR %{qsup}/send/
 rm -fR %{qsup}/smtp/
 rm -fR %{qsup}/submission/
 rm -fR %{qlog}/send/
 rm -fR %{qlog}/smtp/
 rm -fR %{qlog}/submission/
fi

#-------------------------------------------------------------------------------
%files
#-------------------------------------------------------------------------------

%defattr(-,-,qmail)

# config (system)
#-------------------------------------------------------------------------------
%attr(0755,root,root) %config(noreplace) %{_initpath}/qmail
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/tcprules.d/tcp.smtp
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/skel/.qmail

# directories
#-------------------------------------------------------------------------------
%attr(0755,root,qmail) %dir %{qdir}
%attr(2755,alias,qmail) %dir %{qdir}/alias
%attr(0755,root,qmail) %dir %{qbin}
%attr(0755,root,qmail) %dir %{qdir}/boot
%attr(0755,root,qmail) %dir %{qcon}
%attr(0755,root,qmail) %dir %{qcon}/domainkeys
%attr(0755,root,qmail) %dir %{qdoc}
%attr(0755,root,qmail) %dir %{qman}
%attr(0755,root,qmail) %dir %{qman}/cat1
%attr(0755,root,qmail) %dir %{qman}/cat5
%attr(0755,root,qmail) %dir %{qman}/cat7
%attr(0755,root,qmail) %dir %{qman}/cat8
%attr(0755,root,qmail) %dir %{qman}/man1
%attr(0755,root,qmail) %dir %{qman}/man5
%attr(0755,root,qmail) %dir %{qman}/man7
%attr(0755,root,qmail) %dir %{qman}/man8
%attr(0750,qmailq,qmail) %dir %{qque}
%attr(0700,qmaill,qmail) %dir %{qsup}
%attr(1700,qmaill,qmail) %dir %{qsup}/send
%attr(0700,qmaill,qmail) %dir %{qsup}/send/log
%attr(0700,qmaill,qmail) %dir %{qsup}/send/supervise
%attr(1700,qmaill,qmail) %dir %{qsup}/smtp
%attr(0700,qmaill,qmail) %dir %{qsup}/smtp/log
%attr(0700,qmaill,qmail) %dir %{qsup}/smtp/supervise
%attr(1700,qmaill,qmail) %dir %{qsup}/submission
%attr(0700,qmaill,qmail) %dir %{qsup}/submission/log
%attr(0700,qmaill,qmail) %dir %{qsup}/submission/supervise
%attr(0755,root,qmail)   %dir %{qdir}/users
%attr(0750,qmaill,qmail) %dir %{qlog}
%attr(0750,qmaill,qmail) %dir %{qlog}/send
%attr(0750,qmaill,qmail) %dir %{qlog}/smtp
%attr(0750,qmaill,qmail) %dir %{qlog}/submission
%attr(0755,root,root) %dir %{_sysconfdir}/skel/Maildir
%attr(0755,root,root) %dir %{_sysconfdir}/skel/Maildir/cur
%attr(0755,root,root) %dir %{_sysconfdir}/skel/Maildir/new
%attr(0755,root,root) %dir %{_sysconfdir}/skel/Maildir/tmp

# config (qmail)
#-------------------------------------------------------------------------------
%attr(0644,root,qmail) %config(noreplace) %{qcon}/badloadertypes
%attr(0644,root,qmail) %config(noreplace) %{qcon}/badmimetypes
%attr(0644,root,qmail) %config(noreplace) %{qcon}/badmailfrom
%attr(0644,root,qmail) %config(noreplace) %{qcon}/badmailto
%attr(0644,root,qmail) %config(noreplace) %{qcon}/concurrencyincoming
%attr(0644,root,qmail) %config(noreplace) %{qcon}/concurrencyremote
%attr(0644,root,qmail) %config(noreplace) %{qcon}/databytes
%attr(0644,root,qmail) %config(noreplace) %{qcon}/defaultdelivery
%attr(0644,root,qmail) %config(noreplace) %{qcon}/defaultdomain
%attr(0644,root,qmail) %config(noreplace) %{qcon}/defaulthost
%attr(0644,root,qmail) %config(noreplace) %{qcon}/locals
%attr(0644,root,qmail) %config(noreplace) %{qcon}/logcount
%attr(0644,root,qmail) %config(noreplace) %{qcon}/logsize
%attr(0644,root,qmail) %config(noreplace) %{qcon}/plusdomain
%attr(0644,root,qmail) %config(noreplace) %{qcon}/queuelifetime
%attr(0644,root,qmail) %config(noreplace) %{qcon}/rcpthosts
%attr(0644,root,qmail) %config(noreplace) %{qcon}/servercert.pem
%attr(0644,root,qmail) %config(noreplace) %{qcon}/smtpgreeting
%attr(0644,root,qmail) %config(noreplace) %{qcon}/smtproutes
%attr(0644,root,qmail) %config(noreplace) %{qcon}/spfbehavior
%attr(0644,root,qmail) %config(noreplace) %{qcon}/me
%attr(0644,root,qmail) %config(noreplace) %{qcon}/policy
%attr(0644,root,qmail) %config(noreplace) %{qdir}/users/assign
%attr(0644,root,qmail) %config(noreplace) %{qdir}/users/cdb
%attr(0755,root,qmail) %{qdir}/rc

# symlinks (sendmail & domainkeys)
#-------------------------------------------------------------------------------
%attr(-,root,qmail) %{_libdir}/sendmail
%attr(-,root,qmail) %{_sbindir}/sendmail
%attr(-,root,qmail) %{_bindir}/qmailctl
%attr(-,root,qmail) %{qcon}/clientcert.pem
#%attr(-,root,qmail) %{qbin}/qmail-queue

# supervise
#-------------------------------------------------------------------------------
%attr(0751,qmaill,qmail) %{qsup}/send/run
%attr(0751,qmaill,qmail) %{qsup}/send/log/run
%attr(0751,qmaill,qmail) %{qsup}/smtp/run
%attr(0751,qmaill,qmail) %{qsup}/smtp/log/run
%attr(0751,qmaill,qmail) %{qsup}/submission/run
%attr(0751,qmaill,qmail) %{qsup}/submission/log/run

# cat pages
#-------------------------------------------------------------------------------
%attr(0644,root,qmail) %{qman}/cat1/*
%attr(0644,root,qmail) %{qman}/cat5/*
%attr(0644,root,qmail) %{qman}/cat7/*
%attr(0644,root,qmail) %{qman}/cat8/*

# qmail queue
#-------------------------------------------------------------------------------
%attr(0700,qmails,qmail) %dir %{qque}/bounce
%attr(0700,qmails,qmail) %dir %{qque}/info
%attr(0700,qmails,qmail)      %{qque}/info/*
%attr(0700,qmailq,qmail) %dir %{qque}/intd
%attr(0700,qmails,qmail) %dir %{qque}/local
%attr(0700,qmails,qmail)      %{qque}/local/*
%attr(0750,qmailq,qmail) %dir %{qque}/lock
%attr(0600,qmails,qmail)      %{qque}/lock/sendmutex
%attr(0644,qmailr,qmail)      %{qque}/lock/tcpto
%attr(-,qmails,qmail)         %{qque}/lock/trigger
%attr(0750,qmailq,qmail) %dir %{qque}/mess
%attr(0750,qmailq,qmail)      %{qque}/mess/*
%attr(0700,qmailq,qmail) %dir %{qque}/pid
%attr(0700,qmails,qmail) %dir %{qque}/remote
%attr(0700,qmails,qmail)      %{qque}/remote/*
%attr(0750,qmailq,qmail) %dir %{qque}/todo

# boot files
#-------------------------------------------------------------------------------
%attr(0755,root,qmail) %{qdir}/boot/home
%attr(0755,root,qmail) %{qdir}/boot/home+df
%attr(0755,root,qmail) %{qdir}/boot/binm1
%attr(0755,root,qmail) %{qdir}/boot/binm2+df
%attr(0755,root,qmail) %{qdir}/boot/proc+df
%attr(0755,root,qmail) %{qdir}/boot/binm2
%attr(0755,root,qmail) %{qdir}/boot/binm3
%attr(0755,root,qmail) %{qdir}/boot/proc
%attr(0755,root,qmail) %{qdir}/boot/binm3+df
%attr(0755,root,qmail) %{qdir}/boot/binm1+df

# binaries/bin
#-------------------------------------------------------------------------------
%attr(0755,root,qmail) %{qbin}/bouncesaying
%attr(0755,root,qmail) %{qbin}/condredirect
%attr(0755,root,qmail) %{qbin}/config-fast
%attr(0755,root,qmail) %{qbin}/datemail
%attr(0755,root,qmail) %{qbin}/dh_key
%attr(0755,root,qmail) %{qbin}/elq
%attr(0755,root,qmail) %{qbin}/except
%attr(0755,root,qmail) %{qbin}/forward
%attr(0755,root,qmail) %{qbin}/instcheck
%attr(0755,root,qmail) %{qbin}/maildir2mbox
%attr(0755,root,qmail) %{qbin}/maildirmake
%attr(0755,root,qmail) %{qbin}/maildirwatch
%attr(0755,root,qmail) %{qbin}/mailsubj
%attr(0755,root,qmail) %{qbin}/makecert.sh
%attr(0755,root,qmail) %{qbin}/pinq
%attr(0755,root,qmail) %{qbin}/predate
%attr(0755,root,qmail) %{qbin}/preline
%attr(0755,root,qmail) %{qbin}/qail
%attr(0755,root,qmail) %{qbin}/qbiff
%attr(0755,root,qmail) %{qbin}/qmail-badloadertypes
%attr(0755,root,qmail) %{qbin}/qmail-badmimetypes
%attr(0711,root,qmail) %{qbin}/qmail-clean
%attr(04711,qmailq,qmail) %{qbin}/qmail-dk
%attr(0711,root,qmail) %{qbin}/qmail-getpw
%attr(0755,root,qmail) %{qbin}/qmail-inject
%attr(0711,root,qmail) %{qbin}/qmail-local
%attr(0700,root,qmail) %{qbin}/qmail-lspawn
%attr(0700,root,qmail) %{qbin}/qmail-newmrh
%attr(0700,root,qmail) %{qbin}/qmail-newu
%attr(0711,root,qmail) %{qbin}/qmail-pw2u
%attr(0755,root,qmail) %{qbin}/qmail-qread
%attr(0755,root,qmail) %{qbin}/qmail-qstat
%attr(04711,qmailq,qmail) %{qbin}/qmail-queue
%attr(0711,root,qmail) %{qbin}/qmail-remote
%attr(0711,root,qmail) %{qbin}/qmail-rspawn
%attr(0711,root,qmail) %{qbin}/qmail-send
%attr(0755,root,qmail) %{qbin}/qmail-showctl
%attr(0755,root,qmail) %{qbin}/qmail-smtpd
%attr(0755,root,qmail) %{qbin}/qmail-qmqpc
%attr(0755,root,qmail) %{qbin}/qmail-qmqpd
%attr(0755,root,qmail) %{qbin}/qmail-qmtpd
%attr(0700,root,qmail) %{qbin}/qmail-start
%attr(0755,root,qmail) %{qbin}/qmail-tcpok
%attr(0755,root,qmail) %{qbin}/qmail-tcpto
%attr(0755,root,qmail) %{qbin}/qreceipt
%attr(0755,root,qmail) %{qbin}/qsmhook
%attr(0755,root,qmail) %{qbin}/sendmail
%attr(0755,root,qmail) %{qbin}/spfquery
%attr(0755,root,qmail) %{qbin}/srsfilter
%attr(0711,root,qmail) %{qbin}/splogger
%attr(0755,root,qmail) %{qbin}/tcp-env

# man pages
#-------------------------------------------------------------------------------
%attr(0644,root,qmail) %{qman}/man1/qreceipt.1*
%attr(0644,root,qmail) %{qman}/man1/condredirect.1*
%attr(0644,root,qmail) %{qman}/man1/mailsubj.1*
%attr(0644,root,qmail) %{qman}/man1/except.1*
%attr(0644,root,qmail) %{qman}/man1/maildirmake.1*
%attr(0644,root,qmail) %{qman}/man1/preline.1*
%attr(0644,root,qmail) %{qman}/man1/tcp-env.1*
%attr(0644,root,qmail) %{qman}/man1/bouncesaying.1*
%attr(0644,root,qmail) %{qman}/man1/maildir2mbox.1*
%attr(0644,root,qmail) %{qman}/man1/qbiff.1*
%attr(0644,root,qmail) %{qman}/man1/forward.1*
%attr(0644,root,qmail) %{qman}/man1/maildirwatch.1*
%attr(0644,root,qmail) %{qman}/man5/qmail-users.5*
%attr(0644,root,qmail) %{qman}/man5/maildir.5*
%attr(0644,root,qmail) %{qman}/man5/qmail-header.5*
%attr(0644,root,qmail) %{qman}/man5/envelopes.5*
%attr(0644,root,qmail) %{qman}/man5/mbox.5*
%attr(0644,root,qmail) %{qman}/man5/tcp-environ.5*
%attr(0644,root,qmail) %{qman}/man5/qmail-control.5*
%attr(0644,root,qmail) %{qman}/man5/qmail-log.5*
%attr(0644,root,qmail) %{qman}/man5/addresses.5*
%attr(0644,root,qmail) %{qman}/man5/dot-qmail.5*
%attr(0644,root,qmail) %{qman}/man7/qmail-limits.7*
%attr(0644,root,qmail) %{qman}/man7/forgeries.7*
%attr(0644,root,qmail) %{qman}/man7/qmail.7*
%attr(0644,root,qmail) %{qman}/man8/qmail-badloadertypes.8*
%attr(0644,root,qmail) %{qman}/man8/qmail-badmimetypes.8*
%attr(0644,root,qmail) %{qman}/man8/qmail-dk.8*
%attr(0644,root,qmail) %{qman}/man8/qmail-tcpto.8*
%attr(0644,root,qmail) %{qman}/man8/qmail-qread.8*
%attr(0644,root,qmail) %{qman}/man8/splogger.8*
%attr(0644,root,qmail) %{qman}/man8/qmail-start.8*
%attr(0644,root,qmail) %{qman}/man8/qmail-qmqpc.8*
%attr(0644,root,qmail) %{qman}/man8/qmail-qmqpd.8*
%attr(0644,root,qmail) %{qman}/man8/qmail-qmtpd.8*
%attr(0644,root,qmail) %{qman}/man8/qmail-newu.8*
%attr(0644,root,qmail) %{qman}/man8/qmail-tcpok.8*
%attr(0644,root,qmail) %{qman}/man8/qmail-inject.8*
%attr(0644,root,qmail) %{qman}/man8/qmail-clean.8*
%attr(0644,root,qmail) %{qman}/man8/qmail-getpw.8*
%attr(0644,root,qmail) %{qman}/man8/qmail-command.8*
%attr(0644,root,qmail) %{qman}/man8/qmail-showctl.8*
%attr(0644,root,qmail) %{qman}/man8/qmail-rspawn.8*
%attr(0644,root,qmail) %{qman}/man8/qmail-smtpd.8*
%attr(0644,root,qmail) %{qman}/man8/qmail-qstat.8*
%attr(0644,root,qmail) %{qman}/man8/qmail-pw2u.8*
%attr(0644,root,qmail) %{qman}/man8/qmail-queue.8*
%attr(0644,root,qmail) %{qman}/man8/qmail-lspawn.8*
%attr(0644,root,qmail) %{qman}/man8/qmail-newmrh.8*
%attr(0644,root,qmail) %{qman}/man8/qmail-local.8*
%attr(0644,root,qmail) %{qman}/man8/qmail-send.8*
%attr(0644,root,qmail) %{qman}/man8/qmail-remote.8*

# qmail docs
#-------------------------------------------------------------------------------
%attr(0644,root,qmail) %{qdoc}/*

#-------------------------------------------------------------------------------
%changelog
#-------------------------------------------------------------------------------
* Tue Jul 29 2014 Eric Shubert <eric@datamatters.us> 1.03-1.qt
- Patched splogger to remove superfluous timestamp
- Modified rc file to use splogger for qmail-send log messages
- qmail-send log messages now go to /var/log/maillog
- removed CRAM_MD5 authentication method
* Sun Oct 20 2013 Eric Shubert <eric@datamatters.us> 1.03-0.qt
- Migrated to github
- Removed -toaster designation
- Added CentOS 6 support
- Removed qmail-pop3d, unsupported cruft
- Added spamdyke
- Added uid/gid patch so package can be built as non-root user.
- Thanks to Justin H for coding the uid/gid patch.
- Created permanent makecert.sh script, to build TLS certs in %post.
* Thu Mar 08 2012 Eric Shubert <ejs@shubes.net> 1.03-1.3.22
- Reverted chkuser to enable user extensions
- Modified chkuser to enable mailman extensions
* Thu Feb 24 2011 Jake Vickers <jake@qmailtoaster.com> 1.03-1.3.21
- Updated chkuser to 2.0.9
- Re-diff'ed the patch file
- enabled ALL extra allow chars in addresses
- Disabled rcpt MX address checking
* Wed Sep 30 2009 Eric Shubert <ejs@shubes.net> 1.03-1.3.20
- Fixed problem with named pipe not being contained in package list
* Mon Aug 17 2009 Eric Shubert <ejs@shubes.net> 1.03-1.3.19
- Modified to not create named pipe when installed in a sandbox
* Fri Jun 12 2009 Jake Vickers <jake@qmailtoaster.com> 1.03-1.3.18
- Added Fedora 11 support
- Added Fedora 11 x86_64 support
* Tue Jun 02 2009 Jake Vickers <jake@qmailtoaster.com> 1.03-1.3.18
- Added Mandriva 2009 support
* Wed Apr 22 2009 Jake Vickers <jake@qmailtoaster.com> 1.03-1.3.17
- Added Fedora 9 x86_64 and Fedora 10 x86_64 support
- Increased softlimits for x86_64 distros
- Added eMPF patch to the package
* Fri Feb 13 2009 Jake Vickers <jake@qmailtoaster.com> 1.03-1.3.16
- Added Suse 11.1 support
* Sun Feb 08 2009 Jake Vickers <jake@qmailtoaster.com> 1.03-1.3.16
- Added Fedora 9 and 10 support
* Sat Apr 14 2007 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.3.15
- Add CentOS 5 i386 support
- Add CentOS 5 x86_64 support
* Fri Feb 23 2007 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.3.14
- Adapt qmail-103 big dns patch for qmailtoaster - qmailtoaster-big-dns.patch
- Added qmail-smtpd-linefeed.patch thanks to Jean-Paul van de Plasse
* Wed Jan 31 2007 Jean-Paul van de Plasse <jeanpaul@i-serve.nl> 1.03-1.3.13
- Fixed an error in the supervise submission run script
* Fri Jan 12 2007 Erik A. Espinoza <espinoza@kabewm.com> 1.03-1.3.12
- Upgraded to SRS Patch 0.5. Fixed for gcc 4.x and above
* Thu Jan 11 2007 Erik A. Espinoza <espinoza@kabewm.com> 1.03-1.3.11
- Upgraded to SRS Patch 0.4. No longer optional.
- Changed default blacklist to zen.spamhaus.org from sbl.spamhaus.org
* Mon Jan 08 2007 Erik A. Espinoza <espinoza@kabewm.com> 1.03-1.3.10
- Added SRS Patch, must --define 'srs 1' during compile
* Tue Jan 02 2007 Erik A. Espinoza <espinoza@kabewm.com> 1.03-1.3.9
- Added various logging patches from Alexey Loukianov
* Wed Nov 08 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 1.03-1.3.8
- Added REQUIRE_AUTH patch, thanks to Jean-Paul van de Plasse
- Enabled Submission port 587.
* Wed Nov 01 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 1.03-1.3.7
- Added Fedora Core 6 support
* Sat Sep 09 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 1.03-1.3.6
- Commented out everything in badmimetypes/badloadertypes
- Fixed bug in qmailctl (cont had smtpd instead of smtp)
* Sat Jul 08 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 1.03-1.3.5
- Enabled "*" and "$" in chkuser for mailing list support
* Sun Jul 01 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 1.03-1.3.4
- Enabled SRS support in chkuser_settings.h
- Disabled MyDoom sig in badmimetypes
* Mon Jun 05 2006 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.3.3
- Correct badmailfrom patterns - Thanks to Paul Oehler
- Add SuSE 10.1 support
* Sat May 13 2006 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.3.2
- Testing complete and found to be stable
- Add Fedora Core 5 support
* Sun Apr 30 2006 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.3.1
- Totally new test project
- Build-01
- This build is patched only to net-qmail-1.05 with
- TLS, smtp-auth, qmail-remote-auth and qmregex 
- Build-02
- Add chkuser 2.0.8b
- Build-03
- Add netqmail-maildir++
- Build-04
- fix chkuser-2.0 to tarpit and check for valid sender MX record
- Build-05
- Add custom-smtp-reject, oversize-dns, big-concurrency 
- Build-06
- Add warlock-1.3.11
- Build-07
- Add qmail-spf-rc5
- Build-08
- Add qmail-dk-0.54 domainkeys and qmail-dk-0.54-auth
- Build-09
- Add qmail-tap-1.1
- Build-10
- Move qmail-queue to qmail-queue.orig
- Configure qmail-dk link to qmail-queue
* Wed Apr 28 2006 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.2.11
- Add qmailtoaster-1.2.1.patch
- See description for a list of applied patches
- Fixed MTA provides for distros
* Sun Nov 20 2005 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.2.10
- Add SuSE 10.0 and Mandriva 2006.0 support
- Add chkconfig support
* Fri Oct 14 2005 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.2.9
- Add Fedora Core 4 x86_64 support
* Sat Oct 01 2005 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.2.8
- Add CentOS 4 x86_64 support
* Wed Jun 29 2005 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.2.7
- Add Fedora Core 4 support
* Sun Jun 19 2005 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.2.6
- Update patches - add qmail-tap ver 2
* Fri Jun 03 2005 Torbjorn Turpeinen <tobbe@nyvalls.se> 1.03-1.2.5
- Gnu/Linux Mandrake 10.0,10.1,10.2 support
- Add Obsoletes:	qmail-toaster-doc 
* Thu May 25 2005 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.2.4
- Update patches - add SPF, chkuser 2.0, spamthrottle, Warlord
- filtering
* Sun Feb 27 2005 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.2.3
- Add Fedora Core 3 support
- Add CentOS 4 support
* Wed Jun 02 2004 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.2.2
- Add Fedora Core 2 support
* Mon Apr 19 2004 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.2.1
- patch to netqmail-1.05
- Update patches - add qmail-smtpd-virusscan
- Change methods for creating groups and users
- Cleanup runlevel s-links
- Remove cron job with preun
* Sun Feb 22 2004 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.0.15
- Make dh and rsa temp key cron job silent
- Set default mfcheck = 1
* Sun Feb 15 2004 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.0.14
- Add dh and rsa temp keys
- Add cron job for temp keys
* Fri Jan 23 2004 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.0.13
- Fix qmail-remote for TLS and add patch list to description
- Set softlimits
* Thu Jan 08 2004 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.0.12
- Add Trustix 2.0 support
- Add Fedora Core 1 support
- New TLS and SMTP-AUTH patch that works with RedHat and Fedora
* Sat Nov 29 2003 Nick Hemmesch <nick@ndhsoft.com. 1.03-1.0.11
- Fixed overmaildirquota.c - will work on new patches later aaarg :(
* Fri Nov 28 2003 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.0.10
- Bad build with big patch and chkuser - revertet back with fixes
* Wed May 27 2003 Miguel Beccari <miguel.beccari@clikka.com> 1.03-1.0.9
- Build self-signed certificate for TLS
* Sat Apr 26 2003 Miguel Beccari <miguel.beccari@clikka.com> 1.03-1.0.8
- Clean-ups on SPEC file: compilation banner, better gcc detects
- Detect gcc-3.2.3
- Fixed permission on supervise dirs (rare bug with high msec security)
- Revisited spamcontrol patch (http://www.ltn.net/enrique)
- Red Hat Linux 9.0 support (nick@ndhsoft.com)
- Gnu/Linux Mandrake 9.2 support
* Wed Apr 02 2003 Miguel Beccari <miguel.beccari@clikka.com> 1.03-1.0.7
- Clean-ups
* Mon Mar 31 2003 Miguel Beccari <miguel.beccari@clikka.com> 1.03-1.0.6
- Conectiva Linux 7.0 support
- Big DNS patch (was missing???)
* Sun Feb 15 2003 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.0.5
- Support for Red Hat 8.0
* Sun Feb 09 2003 Miguel Beccari <miguel.beccari@clikka.com> 1.03-1.0.4
- Fixed SMTP-AUTH (smtp run script call vpopmail user)
* Sat Feb 01 2003 Miguel Beccari <miguel.beccari@clikka.com> 1.03-1.0.3
- Redo Macros to prepare supporting larger RPM OS.
  We could be able to compile (and use) packages under every RPM based
  distribution: we just need to write right requirements.
* Fri Jan 31 2003 Miguel Beccari <miguel.beccari@clikka.com> 1.03-1.0.2
- Fixed bugs in RPM macros, but we need to improve them to support a large
  number of RPM based OS.
* Sat Jan 25 2003 Miguel Beccari <miguel.beccari@clikka.com> 1.03-1.0.1
- Added new daemons qmail-qmqpc, qmail-qmqpd, qmail-qmtpd. Maybe in future we
  will use it.
- Added MDK 9.1 support
- Try to use gcc-3.2.1
- Added very little patch to compile with newest GLIBC
- Support dor new RPM-4.0.4
* Sat Oct 05 2002 Miguel Beccari <miguel.beccari@clikka.com> 1.03-0.9.2
- TLS patch
- qmail-queue patch
- qmail-pop3d maildir++ quota support
* Sun Sep 29 2002 Miguel Beccari <miguel.beccari@clikka.com> 1.03-0.9.1
- RPM macros to detect Mandrake, RedHat, Trustix are OK again. They are
  very basic but they should work.
- Packages are named with their proper releases and bversion is from now
  part of the rpm release: we will continue upgrading safely.
- Better macros in post unistall
* Fri Sep 27 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.8.1.03-2
- New set of patches
* Mon Sep 23 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.8.1.03-1
- Rebuilded under 0.8 tree.
- Important comments translated from Italian to English.
- Written rpm rebuilds instruction at the top of the file (in english).
- Clean-ups
* Sun Sep 22 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.1.03-5
- In supervise script now using tcpserver with -R flag: Do not attempt
  to obtain $TCPREMOTEINFO from  the  remote  host.
  This speeds up connections from hosts behind misconfigured firewalls
  with port 113 (identd) closed - that are really really a lot -.
- Full support for smtp over SSL.
* Wed Sep 04 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.1.03-4
- Fixed hostname in pop3 tcpserver script
* Thu Aug 29 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.1.03-3
- Deleted Mandrake Release Autodetection (creates problems)
* Wed Aug 28 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.1.03-2
- Fixed init.d restart option
* Fri Aug 16 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.1.03-1
- New version: 0.7 toaster.
- All sources are now bz2 compressed.
- Auth working 100%
- Better macros to detect Mandrake Release
- Minor clean-ups.
* Thu Aug 13 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.6.1.03-1
- New version: 0.6 toaster./bin/qmail-newu
* Mon Aug 12 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.5.1.03-1
- Doc package is standalone (someone does not ask for man pages)
- Checks for gcc-3.2 (default compiler from now)
- New version: 0.5 toaster.
* Tue Aug 08 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.4.1.03-1
- Rebuild against 0.4 toaster
- Revisited instructions after installed the rpm
* Tue Jul 30 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.3.1.03-3
- Now packages have got 'no sex': you can rebuild them with command line
  flags for specifics targets that are: RedHat, Trustix, and of course
  Mandrake (that is default)
* Mon Jul 29 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.3.1.03.2mdk
- Added bettere controls in supervise/smtp/run
* Sun Jul 28 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.3.1.03.1mdk
- toaster v. 0.3: now it is possible upgrading safely because of 'pversion'
  that is package version and 'version' that is toaster version
* Thu Jul 25 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.2-1.03.1mdk
- toaster v. 0.2 (rebuild against ucspi-tcp-toaster v. 0.2)
- More controls on users creation/deletion
- Added /var/qmail/control/blacklists to add anti UCE
- Added controls in supervise/smtp/run to accept mail ONLY from hosts
  with reverse IP (anti-spam rule)
- Added some instructions in post installation
* Mon Jul 22 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.1-1.03.5mdk
- Tested the part that creates qmail users (for RedHat users): we use
  useradd -r flag to create systems account. That is, an user with an
  UID  lower  than  value  of UID_MIN defined in /etc/login.defs
- Some clean-ups
* Thu Jul 18 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.1-1.03.4mdk
- Added tests for gcc-3.1.1
- Added toaster version (we will need to mantain it too): is vtoaster 0.1
- Deleted all Mandrake dependencies as mandrake-release and so on...
- Deleted chkconfig work (some people told me on RedHat failed) and added
  soft links.
- Added SMTP greatings with toaster banner.
* Wed Jul 10 2002 Miguel Beccari <miguel.beccari@clikka.com> 1.03-3mdk
- Corrected /var/qmail/assign file (had to have a "." in it)
- Added stuff to create qmail users and groups (people seems not
  to like Mandrake: so we need to be able to create users and groups).
- Better tuning on supervise (adjusted softlimit to 3200000)
- Complete integration (and dependecing) from qmail-pop3d and vpopmail
* Tue Jul 02 2002 Miguel Beccari <miguel.beccari@clikka.com> 1.03-2mdk
- Tuned supervise to work as better as possible.
- Changed the package names in toaster (we will build toaster packages)
- Added more /var/qmail/control files (but I know I can do more...)
* Tue Jun 25 2002 Miguel Beccari <miguel.beccari@clikka.com> 1.03-1mdk
- First RPM package (it is based on the great Vincent Danen's SRPM).
  I hope to do a good job too.
