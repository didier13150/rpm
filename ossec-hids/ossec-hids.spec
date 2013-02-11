%define asl 1
%define _default_patch_fuzz 2

%define prg  ossec
%define cvs  101203
Distribution:	%{_distribution}
Packager:	%{_packager}
Summary:	An Open Source Host-based Intrusion Detection System
Name:		ossec-hids
Version:	2.6
Release:	1%{?dist}
License:	GPL
Group:		Applications/System
#Source0:	http://www.ossec.net/files/%{name}-%{version}.tar.gz
Source0:	http://www.ossec.net/files/ossec-hids-%{cvs}.tar.gz
Source2:	%{name}.init
Source3:	asl_rules.xml
Source4:	authpsa_rules.xml
Source5:	asl-shun.pl
Source6:	ossec-hids.logrotate
Source7:	zabbix-alert.sh
Source8:	ossec-configure
Source9:	exclusion_rules.xml

#Patch1:	ossec-server-config.patch
Patch2:		asl-decoder-rules.patch
Patch3:		syslog_rules.patch
Patch4:		ossec-client-conf.patch
Patch5:		firewall-drop-update.patch
Patch6:		disable-psql.patch
#Patch7:	ossec-hids-system_audit_rcl-php.patch
#Patch8:	ossec-hids-mysql-schema.patch
Patch9:		ossec-client-init.patch
#Patch10:	smtp_auth-decoder.patch
Patch11:	courier-imap-rules.patch
#Patch12:	denyhosts-decoder.patch
Patch13:	ossec-hids-server-reload.patch
#Patch14:	ossec-hids-inotify-build.patch
#Patch15:	decoder-minicon.patch
#Patch16:	os_dbd-list-fix.patch
#Patch17:	ar-option.patch
# ossec dbd fixes
Patch18:	analysisd_alerts_log.c.patch
Patch19:	headers_read-alert.h.patch
Patch20:	os_dbd_alert.c.patch
Patch21:	shared_read-alert.c.patch
# These add in alertid
Patch22:	headers_read-alert.h-2.patch
Patch23:	os_dbd_alert.c-2.patch
Patch24:	shared_read-alert.c-2.patch
Patch25:	os_dbd_mysql.schema.patch


URL:		http://www.%{prg}.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Vendor:		http://www.ossec.net
Requires(pre):	/usr/sbin/groupadd /usr/sbin/useradd


BuildRequires:	coreutils glibc-devel httpd-devel openssl-devel
BuildRequires:	mysql-devel
%if 0%{?rhel} >= 6
BuildRequires:	inotify-tools-devel
%endif
BuildRequires:	libprelude-devel
BuildRequires:	zlib-devel


Provides:	ossec
Requires:	inotify-tools

#ExclusiveOS:	linux


%description
OSSEC is a scalable, multi-platform, open source Host-based Intrusion Detection
System (HIDS). It has a powerful correlation and analysis engine, integrating
log analysis, file integrity checking, Windows registry monitoring, centralized
policy enforcement, rootkit detection, real-time alerting and active response.
It runs on most operating systems, including Linux, OpenBSD, FreeBSD, MacOS,
Solaris and Windows.

This package contains common files required for all packages.



%package client
Summary:	The OSSEC HIDS Client
Group:		System Environment/Daemons
Provides:	ossec-client
Requires:	%{name} = %{version}-%{release}
Requires(post):	/sbin/chkconfig
Requires(preun):	/sbin/chkconfig /sbin/service
Requires(postun):	/sbin/service
Conflicts:	%{name}-server
%if %{asl}
Requires:	perl-DBD-SQLite
%endif

%description client
The %{name}-client package contains the client part of the
OSSEC HIDS. Install this package on every client to be
monitored.

%package server
Summary:	The OSSEC HIDS Server
Group:		System Environment/Daemons
Provides:	ossec-server
Requires:	%{name} = %{version}-%{release}
Conflicts:	%{name}-client
Requires(pre):	/usr/sbin/groupadd /usr/sbin/useradd
Requires(post):	/sbin/chkconfig
Requires(preun):	/sbin/chkconfig /sbin/service
Requires(postun):	/sbin/service
%if %{asl}
Requires:	perl-DBD-SQLite
%endif

%description server
The %{name}-server package contains the server part of the
OSSEC HIDS. Install this package on a central machine for
log collection and alerting.


%prep
%setup -q -n %{name}-%{cvs}
#%setup -q
%if %{asl}
#%patch1 -p1
%patch2 -p1
%patch3 -p0
%patch4 -p0
%patch5 -p0
%patch6 -p0
#%patch7 -p0
#%patch8 -p0
#%patch10 -p1
%patch11 -p1
#%patch12 -p1
%patch13 -p1
#%patch14 -p1
#%patch15 -p1
#%patch16 -p1
#%patch17 -p1
#%patch18 -p0
#%patch19 -p0
#%patch20 -p0
#%patch21 -p0
#%patch22 -p0
#%patch23 -p0
#%patch24 -p0
#%patch25 -p0
%endif
%patch9 -p1

# Prepare for docs
rm -rf contrib/specs
rm -rf contrib/ossec-testing
chmod -x contrib/*


%build

# Build the agent version first
pushd src
echo "CEXTRA=-DCLIENT" >> ./Config.OS
%{__make}  setagent all
mv addagent/manage_agents ../bin/manage_client
mv logcollector/ossec-logcollector  ../bin/client-logcollector
mv syscheckd/ossec-syscheckd  ../bin/client-syscheckd

# Rebuild for server
rm -f ./Config.OS
%{__make} clean setdb setprelude all build
popd


# Generate the ossec-init.conf template
echo "DIRECTORY=\"%{_localstatedir}/%{prg}\"" >  %{prg}-init.conf
echo "VERSION=\"%{version}\""                 >> %{prg}-init.conf
echo "DATE=\"`date`\""                        >> %{prg}-init.conf



%install
[ -n "${RPM_BUILD_ROOT}" -a "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
#fixup
mkdir -p ${RPM_BUILD_ROOT}%{_initrddir}
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/%{prg}/{bin,stats,rules,tmp}
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/%{prg}/rules/translated/pure_ftpd
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/%{prg}/logs/{archives,alerts,firewall}
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/%{prg}/queue/{alerts,%{prg},fts,syscheck,rootcheck,agent-info,rids}
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/%{prg}/var/run
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/%{prg}/etc/shared
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/%{prg}/etc/templates
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/%{prg}/etc/mysql
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/%{prg}/active-response/bin

install -m 0600 %{prg}-init.conf ${RPM_BUILD_ROOT}%{_sysconfdir}
install -m 0644 etc/%{prg}.conf ${RPM_BUILD_ROOT}%{_localstatedir}/%{prg}/etc/%{prg}.conf.sample
install -m 0644 etc/%{prg}-{agent,server}.conf ${RPM_BUILD_ROOT}%{_localstatedir}/%{prg}/etc
install -m 0644 etc/*.xml ${RPM_BUILD_ROOT}%{_localstatedir}/%{prg}/etc
install -m 0644 etc/internal_options* ${RPM_BUILD_ROOT}%{_localstatedir}/%{prg}/etc
install -m 0644 etc/rules/*xml ${RPM_BUILD_ROOT}%{_localstatedir}/%{prg}/rules
install -m 0644 etc/rules/translated/pure_ftpd/* ${RPM_BUILD_ROOT}%{_localstatedir}/%{prg}/rules/translated/pure_ftpd
install -m 0644 etc/templates/config/* ${RPM_BUILD_ROOT}%{_localstatedir}/%{prg}/etc/templates/
install -m 0750 bin/* ${RPM_BUILD_ROOT}%{_localstatedir}/%{prg}/bin
install -m 0755 active-response/*.sh ${RPM_BUILD_ROOT}%{_localstatedir}/%{prg}/active-response/bin
install -m 0644 src/rootcheck/db/*.txt ${RPM_BUILD_ROOT}%{_localstatedir}/%{prg}/etc/shared
install -m 0644 src/os_dbd/mysql.schema ${RPM_BUILD_ROOT}%{_localstatedir}/%{prg}/etc/mysql/mysql.schema
install -m 0550 src/init/%{prg}-{client,server}.sh ${RPM_BUILD_ROOT}%{_localstatedir}/%{prg}/bin
install -m 0755 %{SOURCE2} ${RPM_BUILD_ROOT}%{_initrddir}/%{name}

# create the faux ossec.conf, %ghost'ed files must exist in the buildroot
touch ${RPM_BUILD_ROOT}%{_localstatedir}/%{prg}/etc/%{prg}.conf

%if %{asl}
mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d
install -m 0644 %{SOURCE3} ${RPM_BUILD_ROOT}%{_localstatedir}/%{prg}/rules
install -m 0644 %{SOURCE4} ${RPM_BUILD_ROOT}%{_localstatedir}/%{prg}/rules
install -m 0644 %{SOURCE9} ${RPM_BUILD_ROOT}%{_localstatedir}/%{prg}/rules
install -m 0755 %{SOURCE5} ${RPM_BUILD_ROOT}%{_localstatedir}/%{prg}/active-response/bin/asl-shun.pl
install -m 0644 %{SOURCE6} ${RPM_BUILD_ROOT}/etc/logrotate.d/ossec-hids
install -m 0755 %{SOURCE7} ${RPM_BUILD_ROOT}%{_localstatedir}/%{prg}/active-response/bin/zabbix-alert.sh
install -m 0755 %{SOURCE8} ${RPM_BUILD_ROOT}%{_localstatedir}/%{prg}/bin/ossec-configure
%endif

%pre
if ! id -g %{prg} > /dev/null 2>&1; then
  groupadd -r %{prg}
fi
if ! id -u %{prg} > /dev/null 2>&1; then
  useradd -g %{prg} -G %{prg}       \
	-d %{_localstatedir}/%{prg} \
	-r -s /sbin/nologin %{prg}
fi

%pre server
if ! id -u %{prg}m > /dev/null 2>&1; then
  useradd -g %{prg} -G %{prg}       \
	-d %{_localstatedir}/%{prg} \
	-r -s /sbin/nologin %{prg}m
fi
if ! id -u %{prg}e > /dev/null 2>&1; then
  useradd -g %{prg} -G %{prg}       \
	-d %{_localstatedir}/%{prg} \
	-r -s /sbin/nologin %{prg}e
fi
if ! id -u %{prg}r > /dev/null 2>&1; then
  useradd -g %{prg} -G %{prg}       \
	-d %{_localstatedir}/%{prg} \
	-r -s /sbin/nologin %{prg}r
fi


%post client
if [ $1 = 1 ]; then
  chkconfig --add %{name}
  chkconfig %{name} on
fi

echo "TYPE=\"agent\"" >> %{_sysconfdir}/%{prg}-init.conf

if [ ! -f  %{_localstatedir}/%{prg}/etc/%{prg}.conf ]; then
  ln -sf %{prg}-agent.conf %{_localstatedir}/%{prg}/etc/%{prg}.conf
fi

ln -sf %{prg}-client.sh %{_localstatedir}/%{prg}/bin/%{prg}-control

# daemon trickery
ln -sf /var/ossec/bin/ossec-client-logcollector /var/ossec/bin/ossec-logcollector
ln -sf /var/ossec/bin/ossec-client-syscheckd    /var/ossec/bin/ossec-syscheckd
ln -sf %{_localstatedir}/%{prg}/bin/client-logcollector  %{_localstatedir}/%{prg}/bin/%{prg}-logcollector
ln -sf %{_localstatedir}/%{prg}/bin/client-syscheckd  %{_localstatedir}/%{prg}/bin/%{prg}-syscheckd

touch %{_localstatedir}/%{prg}/logs/ossec.log
chown %{prg}:%{prg} %{_localstatedir}/%{prg}/logs/ossec.log
chmod 0664 %{_localstatedir}/%{prg}/logs/ossec.log

if [ -f %{_localstatedir}/lock/subsys/%{name} ]; then
  %{_initrddir}/%{name} restart
fi

%post server
if [ $1 = 1 ]; then
  chkconfig --add %{name}
  chkconfig %{name} on
fi

echo "TYPE=\"server\"" >> %{_sysconfdir}/%{prg}-init.conf

if [ ! -f %{_localstatedir}/%{prg}/etc/%{prg}.conf ]; then
  ln -sf %{prg}-server.conf %{_localstatedir}/%{prg}/etc/%{prg}.conf
fi

ln -sf %{prg}-server.sh %{_localstatedir}/%{prg}/bin/%{prg}-control

touch %{_localstatedir}/%{prg}/logs/ossec.log
chown %{prg}:%{prg} %{_localstatedir}/%{prg}/logs/ossec.log
chmod 0664 %{_localstatedir}/%{prg}/logs/ossec.log

if [ -f %{_localstatedir}/lock/subsys/%{name} ]; then
  %{_initrddir}/%{name} restart
fi


%preun client
if [ $1 = 0 ]; then
  chkconfig %{name} off
  chkconfig --del %{name}

  if [ -f %{_localstatedir}/lock/subsys/%{name} ]; then
    %{_initrddir}/%{name} stop
  fi

  rm -f %{_localstatedir}/%{prg}/etc/localtime
  rm -f %{_localstatedir}/%{prg}/etc/%{prg}.conf
  rm -f %{_localstatedir}/%{prg}/bin/%{prg}-control
  rm -f %{_localstatedir}/%{prg}/bin/%{prg}-logcollector
  rm -f %{_localstatedir}/%{prg}/bin/%{prg}-syscheckd
fi

%preun server
if [ $1 = 0 ]; then
  chkconfig %{name} off
  chkconfig --del %{name}

  if [ -f %{_localstatedir}/lock/subsys/%{name} ]; then
    %{_initrddir}/%{name} stop
  fi

  rm -f %{_localstatedir}/%{prg}/etc/localtime
  rm -f %{_localstatedir}/%{prg}/etc/%{prg}.conf
  rm -f %{_localstatedir}/%{prg}/bin/%{prg}-control
fi


%triggerin -- glibc
[ -r %{_sysconfdir}/localtime ] && cp -fpL %{_sysconfdir}/localtime %{_localstatedir}/%{prg}/etc


%clean
[ -n "${RPM_BUILD_ROOT}" -a "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc BUGS CONFIG INSTALL* README
%doc %dir doc
%attr(550,root,%{prg}) %dir %{_localstatedir}/%{prg}
%attr(550,root,%{prg}) %dir %{_localstatedir}/%{prg}/active-response
%attr(550,root,%{prg}) %dir %{_localstatedir}/%{prg}/active-response/bin
%attr(550,root,%{prg}) %dir %{_localstatedir}/%{prg}/bin
%attr(550,root,%{prg}) %dir %{_localstatedir}/%{prg}/etc
%attr(770,%{prg},%{prg}) %dir %{_localstatedir}/%{prg}/etc/shared
%attr(750,%{prg},%{prg}) %dir %{_localstatedir}/%{prg}/etc/templates
%attr(640,%{prg},%{prg}) %{_localstatedir}/%{prg}/etc/templates/*
%attr(750,%{prg},%{prg}) %dir %{_localstatedir}/%{prg}/logs
%attr(550,root,%{prg}) %dir %{_localstatedir}/%{prg}/queue
%attr(770,%{prg},%{prg}) %dir %{_localstatedir}/%{prg}/queue/alerts
%attr(770,%{prg},%{prg}) %dir %{_localstatedir}/%{prg}/queue/%{prg}
%attr(750,%{prg},%{prg}) %dir %{_localstatedir}/%{prg}/queue/syscheck
%attr(550,root,%{prg}) %dir %{_localstatedir}/%{prg}/var
%attr(770,root,%{prg}) %dir %{_localstatedir}/%{prg}/var/run
%if %{asl}
%config(noreplace) /etc/logrotate.d/ossec-hids
%{_localstatedir}/%{prg}/bin/%{prg}-configure
%endif


%files client
%defattr(-,root,root)
%attr(600,root,root) %verify(not md5 size mtime) %{_sysconfdir}/%{prg}-init.conf
%{_initrddir}/*
%config(noreplace) %{_localstatedir}/%{prg}/etc/%{prg}-agent.conf
%config(noreplace) %{_localstatedir}/%{prg}/etc/internal_options*
%config(noreplace) %{_localstatedir}/%{prg}/etc/shared/*
%{_localstatedir}/%{prg}/etc/*.sample
%{_localstatedir}/%{prg}/active-response/bin/*
%{_localstatedir}/%{prg}/bin/%{prg}-client.sh
%{_localstatedir}/%{prg}/bin/%{prg}-agentd
%{_localstatedir}/%{prg}/bin/client-logcollector
%{_localstatedir}/%{prg}/bin/client-syscheckd
%{_localstatedir}/%{prg}/bin/%{prg}-execd
%{_localstatedir}/%{prg}/bin/manage_client
%attr(755,%{prg},%{prg}) %dir %{_localstatedir}/%{prg}/queue/rids

%files server
%defattr(-,root,root)
%attr(600,root,root) %verify(not md5 size mtime) %{_sysconfdir}/%{prg}-init.conf
%{_initrddir}/*
%ghost %config(missingok,noreplace) %{_localstatedir}/%{prg}/etc/ossec.conf
%config(noreplace) %{_localstatedir}/%{prg}/etc/%{prg}-server.conf
%config(noreplace) %{_localstatedir}/%{prg}/etc/internal_options*
#%config(noreplace) %{_localstatedir}/%{prg}/etc/*.xml
%config %{_localstatedir}/%{prg}/etc/*.xml
%config(noreplace) %{_localstatedir}/%{prg}/etc/shared/*
%{_localstatedir}/%{prg}/etc/mysql/mysql.schema
%{_localstatedir}/%{prg}/etc/*.sample
%{_localstatedir}/%{prg}/active-response/bin/*
%{_localstatedir}/%{prg}/bin/ossec-server.sh
%{_localstatedir}/%{prg}/bin/ossec-agentd
%{_localstatedir}/%{prg}/bin/ossec-analysisd
%{_localstatedir}/%{prg}/bin/ossec-execd
%{_localstatedir}/%{prg}/bin/ossec-logcollector
%{_localstatedir}/%{prg}/bin/ossec-maild
%{_localstatedir}/%{prg}/bin/ossec-monitord
%{_localstatedir}/%{prg}/bin/ossec-remoted
%{_localstatedir}/%{prg}/bin/ossec-syscheckd
%{_localstatedir}/%{prg}/bin/ossec-dbd
%{_localstatedir}/%{prg}/bin/ossec-reportd
%{_localstatedir}/%{prg}/bin/ossec-agentlessd
%{_localstatedir}/%{prg}/bin/ossec-makelists
%{_localstatedir}/%{prg}/bin/ossec-csyslogd
%{_localstatedir}/%{prg}/bin/ossec-regex
%{_localstatedir}/%{prg}/bin/list_agents
%{_localstatedir}/%{prg}/bin/manage_agents
%{_localstatedir}/%{prg}/bin/syscheck_update
%{_localstatedir}/%{prg}/bin/clear_stats
%{_localstatedir}/%{prg}/bin/agent_control
%{_localstatedir}/%{prg}/bin/rootcheck_control
%{_localstatedir}/%{prg}/bin/syscheck_control
%{_localstatedir}/%{prg}/bin/ossec-logtest
%{_localstatedir}/%{prg}/bin/verify-agent-conf


%attr(750,%{prg},%{prg}) %dir %{_localstatedir}/%{prg}/logs/archives
%attr(750,%{prg},%{prg}) %dir %{_localstatedir}/%{prg}/logs/alerts
%attr(750,%{prg},%{prg}) %dir %{_localstatedir}/%{prg}/logs/firewall
%attr(755,%{prg}r,%{prg}) %dir %{_localstatedir}/%{prg}/queue/agent-info
%attr(755,%{prg}r,%{prg}) %dir %{_localstatedir}/%{prg}/queue/rids
%attr(700,%{prg},%{prg}) %dir %{_localstatedir}/%{prg}/queue/fts
%attr(700,%{prg},%{prg}) %dir %{_localstatedir}/%{prg}/queue/rootcheck
%attr(550,root,%{prg}) %dir %{_localstatedir}/%{prg}/rules
#%config(noreplace) %{_localstatedir}/%{prg}/rules/*
%config %{_localstatedir}/%{prg}/rules/*
%attr(750,%{prg},%{prg}) %dir %{_localstatedir}/%{prg}/stats
%attr(770,root,%{prg}) %dir %{_localstatedir}/%{prg}/tmp


%changelog

* Fri Sep 16 2011 Didier Fabert <dfabert@b2pweb.com> 2.6-1
- Update

* Thu Mar 17 2011 Didier Fabert <dfabert@b2pweb.com> 2.5.1-9
- Rebuild

* Fri Dec 17 2010 Support <support@atomicorp.com> - 2.5.1-8
- Changed asl-shun sqlite database to /var/ossec/var/blocklist3.sqlite
- asl-shun database format now stores the full alertid

* Sun Dec 5 2010 Support <support@atomicorp.com> - 2.5.1-7
- Update to snapshot 101203

* Wed Dec 1 2010 Support <support@atomicorp.com> - 2.5.1-6
- Update to snapshot 101125

* Mon Nov 1 2010 Support <support@atomicorp.com> - 2.5.1-5
- Added alertid support to os_dbd, this involves a schema update

* Mon Nov 1 2010 Support <support@atomicorp.com> - 2.5.1-4
- Added dst ip, src prt, and dst prt capture support to os_dbd

* Fri Oct 29 2010 Support <support@atomicorp.com> - 2.5.1-3
- Bugfix #XXX, manage_agents was built in client mode for the server package.

* Thu Oct 28 2010 Support <support@atomicorp.com> - 2.5.1-2
- Add clamav decoder & ruleset

* Wed Oct 13 2010 Support <support@atomicorp.com> - 2.5.1-1
- Update to 2.5.1 final

* Thu Sep 30 2010 Support <support@atomicorp.com> - 2.5-1
- Update to 2.5 final

* Tue Sep 28 2010 Support <support@atomicorp.com> - 2.5-0.9
- Update to 0928 snapshot

* Sat Sep 25 2010 Support <support@atomicorp.com> - 2.5-0.8
- Extended no_ar into ossec-dbd

* Wed Sep 23 2010 Support <support@atomicorp.com> - 2.5-0.7
- Add no_ar option to disable active response per rule

* Wed Sep 20 2010 Support <support@atomicorp.com> - 2.5-0.6
- Update to snapshot 100920

* Wed Sep 8 2010 Support <support@atomicorp.com> - 2.5-0.1
- Update snapshot to 100907

* Wed Sep 1 2010 Support <support@atomicorp.com> - 2.4.1-11.2
- Snapshot 100901

* Tue Aug 31 2010 Support <support@atomicorp.com> - 2.4.1-11.1
- Added test fix for os_dbd

* Thu Aug 26 2010 Support <support@atomicorp.com> - 2.4.1-10
- Bugfix #376, ossec-control will now properly stop and reload

* Thu Aug 19 2010 Support <support@atomicorp.com> - 2.4.1-9
- Update to 0809 snapshot

* Tue Aug 10 2010 Support <support@atomicorp.com> - 2.4.1-8
- Relink against native mysql

* Wed Jul 30 2010 Support <support@atomicorp.com> - 2.4.1-7
- Add minicon decoder from les fenison

* Wed Jul 7 2010 Support <support@atomicorp.com> - 2.4.1-6
- Update to 100707 snapshot
- Feature Request #371, add ossec.log to logrotate

* Mon Jun 21 2010 Support <support@atomicorp.com> - 2.4.1-5
- Updated to 100615 snapshot

* Thu Apr 29 2010 Support <support@atomicorp.com> - 2.4.1-4
- Updated init and ossec-server scripts to support the new reload feature.

* Tue Apr 20 2010 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.4.1-1
- Update to 2.4.1

* Fri Apr 9 2010 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.4-5
- Added zabbix reporting active response

* Thu Apr 1 2010 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.4-4
- Update to 2.4 final
- Lowered courier rule 3910 (failures) from 6 over 240 to 10 over 10
- Lowered courier rule 3911 (success) from 10 over 60 to 30 over 20

* Tue Mar 23 2010 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.4-1
- Rebuilt for atomic repo

* Thu Mar 22 2010 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.4-0.2
- Update to CVS 100317

* Thu Mar 11 2010 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.4-0.1
- Update to CVS 100311
- Add decoder for denyhosts
- Update asl_rules.xml to include denyhosts rules

* Tue Mar 9 2010 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.3-8
- Update to CVS 100309

* Fri Mar 5 2010 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.3-7
- Added new decoder for smtp_auth
- Added rules to detect smtp_auth brute force attempts
- Added rules to detect imap/pop brute force attempts

* Mon Dec 7 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.3-6
- Updated ossec-server.conf to be in parity with the ASL config
- Added templates dir for generating configs

* Mon Dec 7 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.3-1
- Update to 2.3 release

* Mon Nov 9 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.2-5
- Update to snapshot 091109

* Tue Sep 29 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.2-4
- Update to snapshot 091008

* Tue Sep 29 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.2-3
- Update to snapshot 090925
- Added timestamp field to the mysql schema
- Bugfix #XXX, for the ossec-client.init script to call the correct (renamed) ossec syscheckd/logcollector daemons
- Appologies for not updating the previous changelogs. Missed a few updates!

* Mon Aug 31 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.2.0.beta2.1
- Update to snapshot 090827
- Feature Request #225, Added logrotate event to active-response log
- Updated system_audit_rcl.txt to look for the correct php.ini file

* Mon Aug 24 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.2.0.beta1.1
- Update to 090824, beta 1 release

* Wed Aug 12 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.1.1-5
- Update to 090812 snapshot

* Thu Jul 28 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.1.1-3
- Rebuild agent daemons with -DCLIENT, added symlink trickery

* Thu Jul 2 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.1.1-1
- update to 2.1.1

* Wed Jun 30 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.1-3
- update to 090630 snapshot, this has fixes for CentOS/RHEL 4 64-bit environments

* Wed Jun 12 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.1-1
- update to 2.1 final

* Wed Jun 12 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.0-11
- update to snapshot 090612

* Wed Jun 10 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.0-10
- update to snapshot 090610

* Wed Jun 3 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.0-9
- update to snapshot 090603

* Mon Apr 27 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.0-8
- Disable postgresql support, to get around an undesirable dependency on EL4

* Mon Apr 17 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.0-7
- Update to snapshot 090417

* Mon Apr 13 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.0-6
- Update to snapshot 090413 (this adds in inotify support)

* Wed Apr 10 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.0-5
- Update to snapshot 090410 (this adds in inotify support)

* Wed Apr 8 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.0-4
- Update to snapshot 090408

* Thu Mar 5 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.0-2
- Added authpsa rules back in, this is used to detect brute force attacks
- Added conditional building support for ASL modifications

* Fri Feb 27 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.0-1
- Update to 2.0 official release

* Thu Feb 26 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.0.0-0.090225.1
- update to snapshot 090225

* Sun Feb 20 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.0.0-0.090220.1
- update to snapshot 090220

* Fri Feb 6 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.0.0-0.090206.1
- update to snapshot 090206

* Mon Feb 5 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 2.0.0-0.090205.1
- update to snapshot 090205

* Fri Jan 30 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 1.99-2
- update to CVS code 090129, this is not an offical release. Its for testing only

* Tue Jan 27 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 1.99-1
- update to CVS code 090126, this is not an offical release. Its for testing only

* Thu Oct 9 2008 Scott R. Shinn <scott@atomicrocketturtle.com> - 1.6.1-1
- update to 1.6.1

* Wed Sep 3 2008 Scott R. Shinn <scott@atomicrocketturtle.com> - 1.6-1
- update to 1.6

* Thu Jun 26 2008 Scott R. Shinn <scott@atomicrocketturtle.com> - 1.5.1-1
- update to 1.5.1

* Mon Jun 9 2008 Scott R. Shinn <scott@atomicrocketturtle.com> - 1.5-3
- added mysql support

* Tue May 20 2008 Scott R. Shinn <scott@atomicrocketturtle.com> - 1.5-2
- Added Stanislaw Polak's excellent ban-hackers script to manage shunning more intelligently.

* Tue May 13 2008 Scott R. Shinn <scott@atomicrocketturtle.com> - 1.5-1
- update to 1.5

* Mon Nov 26 2007 Scott R. Shinn <scott@atomicrocketturtle.com> - 1.4-2
- fix on active-response locking bug that prevented some rules from expiring.

* Mon Nov 19 2007 Scott R. Shinn <scott@atomicrocketturtle.com> - 1.4-1
- update to ossec 1.4

* Mon Oct 15 2007 Scott R. Shinn <scott@atomicrocketturtle.com> - 1.3-4
- update snapshot to ossec-hids-071011.tar.gz
- relinked C4, FC4, FC5 against mysql4

* Tue Oct 9 2007 Scott R. Shinn <scott@atomicrocketturtle.com> - 1.3-3
- update to snapshot ossec-hids-071006.tar.gz

* Wed Sep 5 2007 Scott R. Shinn <scott@atomicrocketturtle.com> - 1.3-2
- update to shun blocklist tracking used by ASL
- added authpsa rules + decoder

* Tue Aug 14 2007 Scott R. Shinn <scott@atomicrocketturtle.com> - 1.3-1
- update to 1.3

* Wed Aug 8 2007 Scott R. Shinn <scott@atomicrocketturtle.com> - 1.2-8
- minor adjustment in %post, to check for config file before overwriting it

* Fri Aug 3 2007 Scott R. Shinn <scott@atomicrocketturtle.com> - 1.2-7
- v6 was first version of the patch.
- added in logging in active-response for better ASL support
- Disabled conf event in %post, to keep from overwriting config files.

* Mon Jun 25 2007 Scott R. Shinn <scott@atomicrocketturtle.com> - 1.2-5
- changed permissions on queue/syscheck so it can be read by the ossec group (tweak for web gui)

* Fri Jun 15 2007 Scott R. Shinn <scott@atomicrocketturtle.com> - 1.2-4
- removed the noreplace settings from decoder and the rules
- patch for a more ASL friendly client config

* Thu Jun 14 2007 Scott R. Shinn <scott@atomicrocketturtle.com> - 1.2-3
- release -2 had a bug.
- added ASL rules (asl_rules.xml)
- added decoder for the asl style modsecurity logging
- adjusted syslog_rules for qmail-scanner issue (BUG #ASL-18)
- Added http index in asl_rules.xml (BUG #ASL-7)

* Tue May 15 2007 Scott R. Shinn <scott@atomicrocketturtle.com> - 1.2-1
- update to 1.2

* Tue Apr 24 2007 Scott R. Shinn <scott@atomicrocketturtle.com> - 1.1-1
- update to 1.1

* Tue Mar 6 2007 Scott R. Shinn <scott@atomicrocketturtle.com> - 1.0-2
- configuration change for ASL

* Wed Jan 17 2007 Scott R. Shinn <scott@atomicrocketturtle.com> - 1.0
- updated to 1.0

* Fri Dec 8 2006 Scott R. Shinn <scott@atomicrocketturtle.com>
- import into ART
- changed their naming conventions a bit, 0.9-3 to 0.9.3. Please dont be cross with me.

* Thu Nov 02 2006 peter.pramberger@member.fsf.org
- new version (0.9-3)

* Fri Sep 29 2006 peter.pramberger@member.fsf.org
- new version (0.9-2)

* Thu Sep 07 2006 peter.pramberger@member.fsf.org
- new version (0.9-1a)

* Thu Aug 24 2006 peter.pramberger@member.fsf.org
- new version (0.9-1)

* Wed Jul 26 2006 peter.pramberger@member.fsf.org
- new version (0.9)

* Fri Jul 14 2006 peter.pramberger@member.fsf.org
- some bugfixes

* Fri Jul 07 2006 peter.pramberger@member.fsf.org
- created

