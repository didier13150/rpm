# TODO
# generate ssl cert for authd: 
# openssl genrsa -out /var/ossec/etc/sslmanager.key 2048
# openssl req -new -x509 -key /var/ossec/etc/sslmanager.key -out /var/ossec/etc/sslmanager.cert -days 365 

%define asl 1
%define _default_patch_fuzz 2

%define prg  ossec
%define cvs  rc1

Summary:     An Open Source Host-based Intrusion Detection System
Name:        ossec-hids
Version:     2.7
Release:     20%{?dist}
License:     GPLv2
Group:       Applications/System
Source0:     http://www.ossec.net/files/%{name}-%{version}.tar.gz
Source2:     %{name}.init
Source5:     asl-shun.pl
Source6:     ossec-hids.logrotate
Source7:     zabbix-alert.sh
Source8:     ossec-configure
Source9:     ossec-hids-agent.conf
Patch1:      syscheck-increase-sleep.patch
Patch4:      ossec-client-conf.patch
Patch5:      firewall-drop-update.patch
Patch6:      disable-psql.patch
Patch20:     ossec-hids-mysql-schema-fix1.patch
Patch21:     ossec-hids-server-init.patch
Patch22:     ossec-hids-2.7-duplicate-suppression-revert.patch
Patch23:     Make.patch
Patch24:     pam-decoder-update.patch

URL:         http://www.ossec.net/
BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires(pre):    /usr/sbin/groupadd /usr/sbin/useradd

BuildRequires: coreutils glibc-devel httpd-devel openssl-devel
BuildRequires: mysql-devel 
%if 0%{?rhel} >= 6
BuildRequires: inotify-tools-devel
%endif
BuildRequires: libprelude-devel
BuildRequires: zlib-devel

Provides: ossec = %{version}-%{release}
Requires: inotify-tools

%description
OSSEC is a scalable, multi-platform, open source Host-based Intrusion Detection
System (HIDS). It has a powerful correlation and analysis engine, integrating
log analysis, file integrity checking, Windows registry monitoring, centralized
policy enforcement, rootkit detection, real-time alerting and active response.
It runs on most operating systems, including Linux, OpenBSD, FreeBSD, MacOS,
Solaris and Windows.

This package contains common files required for all packages.
%package client
Summary:     The OSSEC HIDS Client
Group:       System Environment/Daemons
Provides:    ossec-client = %{version}-%{release}
Requires:    %{name} = %{version}-%{release}
Requires(post):   /sbin/chkconfig 
Requires(preun):  /sbin/chkconfig /sbin/service
Requires(postun): /sbin/service 
Conflicts:   %{name}-server
%if %{asl}
Requires:    perl-DBD-SQLite
%endif

%description client
The %{name}-client package contains the client part of the
OSSEC HIDS. Install this package on every client to be
monitored.

%package server
Summary:     The OSSEC HIDS Server
Group:       System Environment/Daemons
Provides:    ossec-server = %{version}-%{release}
Requires:    %{name} = %{version}-%{release} 
Conflicts:   %{name}-client
Requires(pre):    /usr/sbin/groupadd /usr/sbin/useradd
Requires(post):   /sbin/chkconfig 
Requires(preun):  /sbin/chkconfig /sbin/service
Requires(postun): /sbin/service 
%if %{asl}
Requires:    perl-DBD-SQLite
%endif

%description server
The %{name}-server package contains the server part of the
OSSEC HIDS. Install this package on a central machine for
log collection and alerting.

%prep
%setup -q -n %{name}-%{version}
%if %{asl}
%patch1 -p1
%patch4 -p0
%patch5 -p0
%patch6 -p0
%patch20 -p1
%patch21 -p1
# new
%patch22 -p1 
%patch23 -p1 
%patch24 -p1
%endif

# Prepare for docs
rm -rf contrib/specs
chmod -x contrib/*

%build
# no
CFLAGS="$RPM_OPT_FLAGS -fpie"
LDFLAGS="-fPIE -pie -Wl,-z,relro"
# no
SH_LDFLAGS="-fPIE -pie -Wl,-z,relro"
##LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now"
export CFLAGS LDFLAGS SH_LDFLAGS

# Build the agent version first
pushd src
%{__make}  setagent all
mv addagent/manage_agents ../bin/manage_client
mv logcollector/ossec-logcollector  ../bin/client-logcollector
mv syscheckd/ossec-syscheckd  ../bin/client-syscheckd
mv client-agent/ossec-agentd  ../bin/client-agentd

# Rebuild for server
%{__make} clean setdb setprelude all build
popd

# Bugfix, Cleanup for agentd
rm -f bin/ossec-agentd
mv bin/client-agentd bin/ossec-agentd


# Generate the ossec-init.conf template
echo "DIRECTORY=\"%{_localstatedir}/ossec\"" >  ossec-init.conf
echo "VERSION=\"%{version}\""                 >> ossec-init.conf
echo "DATE=\"`date`\""                        >> ossec-init.conf

%install
[ -n "${RPM_BUILD_ROOT}" -a "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
#fixup
mkdir -p ${RPM_BUILD_ROOT}%{_initrddir}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_sysconfdir}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_datadir}/ossec/contrib
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_localstatedir}/{log,run}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/active-response/bin
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/agentless
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/{bin,stats,rules,tmp}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/rules/translated/pure_ftpd
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/logs/{archives,alerts,firewall}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/queue/{alerts,agentless,agent-info,diff,fts,ossec,rids,rootcheck,syscheck}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/var/run
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/etc/shared
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/etc/templates
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/etc/mysql
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/etc/decoders.d
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/etc/rules.d
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/stats
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/tmp
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/var/run
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/.ssh

%{__install} -m 0755 %{SOURCE2} ${RPM_BUILD_ROOT}%{_initrddir}/%{name}
install -m 0600 ossec-init.conf ${RPM_BUILD_ROOT}%{_sysconfdir}

install -m 0644 etc/ossec.conf ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/etc/ossec.conf.sample
install -m 0644 etc/ossec-{agent,server}.conf ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/etc
install -m 0644 etc/*.xml ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/etc
install -m 0644 etc/internal_options* ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/etc
install -m 0644 etc/rules/*xml ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/rules
install -m 0644 etc/rules/translated/pure_ftpd/* ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/rules/translated/pure_ftpd
install -m 0644 etc/templates/config/* ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/etc/templates/
install -m 0750 bin/* ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/bin
install -m 0755 active-response/*.sh ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/active-response/bin
install -m 0644 src/rootcheck/db/*.txt ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/etc/shared
install -m 0644 src/os_dbd/mysql.schema ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/etc/mysql/mysql.schema
install -m 0550 src/init/ossec-{client,server}.sh ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/bin
install -m 0550 src/agentlessd/scripts/* ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/agentless
%{__install} -m 0755 bin/agent-auth           ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/bin

# Install contrib files
pushd contrib
%{__install} -m 0750 {config2xml,*.pl,*.sh}   ${RPM_BUILD_ROOT}%{_datadir}/ossec/contrib
%{__install} -m 0640 *.{conf,pm,sql,txt}      ${RPM_BUILD_ROOT}%{_datadir}/ossec/contrib
popd

# create an empty ossec.conf, ghost'ed files must exist in the buildroot
touch ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/etc/ossec.conf

%if %{asl}
mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d
install -m 0755 %{SOURCE5} ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/active-response/bin/asl-shun.pl
install -m 0644 %{SOURCE6} ${RPM_BUILD_ROOT}/etc/logrotate.d/%{name}
install -m 0755 %{SOURCE7} ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/active-response/bin/zabbix-alert.sh
install -m 0755 %{SOURCE8} ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/bin/ossec-configure
install -m 0644 %{SOURCE9} ${RPM_BUILD_ROOT}%{_localstatedir}/ossec/etc/shared/agent.conf
%endif

%pre
if ! id -g ossec > /dev/null 2>&1; then
  groupadd -r ossec
fi
if ! id -u ossec > /dev/null 2>&1; then
  useradd -g ossec -G ossec \
    -d %{_localstatedir}/ossec \
    -r -s /sbin/nologin ossec
fi
if ! id -u ossecr > /dev/null 2>&1; then
  useradd -g ossec -G ossec \
    -d %{_localstatedir}/ossec \
    -r -s /sbin/nologin ossecr
fi

%pre server
if ! id -u ossecm > /dev/null 2>&1; then
  useradd -g ossec -G ossec \
    -d %{_localstatedir}/ossec \
    -r -s /sbin/nologin ossecm
fi
if ! id -u ossece > /dev/null 2>&1; then
  useradd -g ossec -G ossec \
    -d %{_localstatedir}/ossec \
    -r -s /sbin/nologin ossece
fi

%post client
if [ $1 = 1 ]; then
  chkconfig --add %{name}
  chkconfig %{name} on
fi

echo "TYPE=\"agent\"" >> %{_sysconfdir}/ossec-init.conf

if [ ! -f  %{_localstatedir}/ossec/etc/ossec.conf ]; then
  ln -sf ossec-agent.conf %{_localstatedir}/ossec/etc/ossec.conf
fi

ln -sf ossec-client.sh %{_localstatedir}/ossec/bin/ossec-control

# daemon trickery
ln -sf /var/ossec/bin/ossec-client-logcollector /var/ossec/bin/ossec-logcollector
ln -sf /var/ossec/bin/ossec-client-syscheckd    /var/ossec/bin/ossec-syscheckd
ln -sf %{_localstatedir}/ossec/bin/client-logcollector  %{_localstatedir}/ossec/bin/ossec-logcollector 
ln -sf %{_localstatedir}/ossec/bin/client-syscheckd  %{_localstatedir}/ossec/bin/ossec-syscheckd 

touch %{_localstatedir}/ossec/logs/ossec.log
chown ossec:ossec %{_localstatedir}/ossec/logs/ossec.log
chmod 0664 %{_localstatedir}/ossec/logs/ossec.log


if [ -f %{_localstatedir}/lock/subsys/%{name} ]; then
  %{_initrddir}/%{name} restart
fi

%post server
if [ $1 = 1 ]; then
  chkconfig --add %{name}
  chkconfig %{name} on
fi

echo "TYPE=\"server\"" >> %{_sysconfdir}/ossec-init.conf

if [ ! -f %{_localstatedir}/ossec/etc/ossec.conf ]; then
  ln -sf ossec-server.conf %{_localstatedir}/ossec/etc/ossec.conf
fi

ln -sf ossec-server.sh %{_localstatedir}/ossec/bin/ossec-control

touch %{_localstatedir}/ossec/logs/ossec.log
chown ossec:ossec %{_localstatedir}/ossec/logs/ossec.log

# fixup for ASL 2.2 -> ASL 3.0
if grep -q asl_rules /var/ossec/etc/ossec.conf; then
  /usr/bin/perl -p -i -e "s[<include>asl_rules.xml</include>][]g" /var/ossec/etc/ossec.conf
  if [ -f /etc/asl/config ]; then
    /usr/bin/perl -p -i -e s[OSSEC_VERSION=.*][OSSEC_VERSION=0] /etc/asl/VERSION
  fi
fi

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

  rm -f %{_localstatedir}/ossec/etc/localtime
  rm -f %{_localstatedir}/ossec/etc/ossec.conf
  rm -f %{_localstatedir}/ossec/bin/ossec-control
  rm -f %{_localstatedir}/ossec/bin/ossec-logcollector 
  rm -f %{_localstatedir}/ossec/bin/ossec-syscheckd 
fi

%preun server
if [ $1 = 0 ]; then
  chkconfig %{name} off
  chkconfig --del %{name}

  if [ -f %{_localstatedir}/lock/subsys/%{name} ]; then
    %{_initrddir}/%{name} stop
  fi

  rm -f %{_localstatedir}/ossec/etc/localtime
  rm -f %{_localstatedir}/ossec/etc/ossec.conf
  rm -f %{_localstatedir}/ossec/bin/ossec-control
fi

%triggerin -- glibc
[ -r %{_sysconfdir}/localtime ] && cp -fpL %{_sysconfdir}/localtime %{_localstatedir}/ossec/etc

%clean
[ -n "${RPM_BUILD_ROOT}" -a "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%doc BUGS CONFIG INSTALL* README
%doc %dir doc
%attr(550,root,ossec) %dir %{_localstatedir}/ossec
%attr(550,root,ossec) %dir %{_localstatedir}/ossec/active-response
%attr(550,root,ossec) %{_localstatedir}/ossec/active-response/bin
%attr(550,root,ossec) %{_localstatedir}/ossec/agentless
%attr(550,root,ossec) %dir %{_localstatedir}/ossec/bin
%attr(550,root,ossec) %dir %{_localstatedir}/ossec/etc
%attr(770,ossec,ossec) %dir %{_localstatedir}/ossec/etc/shared
%attr(750,ossec,ossec) %dir %{_localstatedir}/ossec/etc/templates
%attr(640,ossec,ossec) %{_localstatedir}/ossec/etc/templates/*
%attr(770,ossec,ossec) %dir %{_localstatedir}/ossec/logs
%attr(550,root,ossec) %dir %{_localstatedir}/ossec/queue
%attr(770,ossec,ossec) %dir %{_localstatedir}/ossec/queue/ossec
%attr(750,ossec,ossec) %dir %{_localstatedir}/ossec/queue/diff
%attr(550,root,ossec) %dir %{_localstatedir}/ossec/var
%attr(770,root,ossec) %dir %{_localstatedir}/ossec/var/run
%if %{asl}
%config(noreplace) /etc/logrotate.d/%{name}
%{_localstatedir}/ossec/bin/ossec-configure
%endif

%files client
%defattr(-,root,root)
%attr(600,root,root) %verify(not md5 size mtime) %{_sysconfdir}/ossec-init.conf
%{_initrddir}/*
%config(noreplace) %{_localstatedir}/ossec/etc/ossec-agent.conf
%config(noreplace) %{_localstatedir}/ossec/etc/internal_options*
%config(noreplace) %{_localstatedir}/ossec/etc/shared/*
%{_localstatedir}/ossec/etc/*.sample
%{_localstatedir}/ossec/bin/ossec-client.sh
%{_localstatedir}/ossec/bin/ossec-agentd
%{_localstatedir}/ossec/bin/client-logcollector
%{_localstatedir}/ossec/bin/client-syscheckd
%{_localstatedir}/ossec/bin/ossec-execd
%{_localstatedir}/ossec/bin/manage_client
%{_localstatedir}/ossec/bin/agent-auth
%attr(550,root,ossec) %dir %{_localstatedir}/ossec/queue/alerts
%attr(775,root,ossec) %dir %{_localstatedir}/ossec/queue/rids
%attr(550,root,ossec) %dir %{_localstatedir}/ossec/queue/syscheck

%files server
%defattr(-,root,root)
%attr(600,root,root) %verify(not md5 size mtime) %{_sysconfdir}/ossec-init.conf
%{_initrddir}/*
%ghost %config(missingok,noreplace) %{_localstatedir}/ossec/etc/ossec.conf
%config(noreplace) %{_localstatedir}/ossec/etc/ossec-server.conf
%config(noreplace) %{_localstatedir}/ossec/etc/internal_options*
%attr(640,ossec,ossec) %dir %{_localstatedir}/ossec/etc/shared/agent.conf
%config %{_localstatedir}/ossec/etc/*.xml
%config(noreplace) %{_localstatedir}/ossec/etc/shared/*
%dir %{_datadir}/ossec/contrib
%{_datadir}/ossec/*
%{_localstatedir}/ossec/etc/mysql/mysql.schema
%{_localstatedir}/ossec/etc/rules.d/
%{_localstatedir}/ossec/etc/decoders.d/
%{_localstatedir}/ossec/etc/*.sample
%{_localstatedir}/ossec/bin/ossec-authd
%{_localstatedir}/ossec/bin/agent_control
%{_localstatedir}/ossec/bin/clear_stats
%{_localstatedir}/ossec/bin/list_agents
%{_localstatedir}/ossec/bin/manage_agents
%{_localstatedir}/ossec/bin/ossec-agentd
%{_localstatedir}/ossec/bin/ossec-agentlessd
%{_localstatedir}/ossec/bin/ossec-analysisd
%{_localstatedir}/ossec/bin/ossec-csyslogd
%{_localstatedir}/ossec/bin/ossec-dbd
%{_localstatedir}/ossec/bin/ossec-execd
%{_localstatedir}/ossec/bin/ossec-logcollector
%{_localstatedir}/ossec/bin/ossec-logtest
%{_localstatedir}/ossec/bin/ossec-maild
%{_localstatedir}/ossec/bin/ossec-makelists
%{_localstatedir}/ossec/bin/ossec-monitord
%{_localstatedir}/ossec/bin/ossec-regex
%{_localstatedir}/ossec/bin/ossec-remoted
%{_localstatedir}/ossec/bin/ossec-reportd
%{_localstatedir}/ossec/bin/ossec-server.sh
%{_localstatedir}/ossec/bin/ossec-syscheckd
%{_localstatedir}/ossec/bin/rootcheck_control
%{_localstatedir}/ossec/bin/syscheck_control
%{_localstatedir}/ossec/bin/syscheck_update
%{_localstatedir}/ossec/bin/verify-agent-conf

%attr(750,ossec,ossec) %dir %{_localstatedir}/ossec/logs/archives
%attr(770,ossec,ossec) %dir %{_localstatedir}/ossec/logs/alerts
%attr(750,ossec,ossec) %dir %{_localstatedir}/ossec/logs/firewall
%attr(755,ossecr,ossec) %dir %{_localstatedir}/ossec/queue/agent-info
%attr(755,ossec,ossec) %dir %{_localstatedir}/ossec/queue/agentless
%attr(770,ossec,ossec) %dir %{_localstatedir}/ossec/queue/alerts
%attr(750,ossec,ossec) %dir %{_localstatedir}/ossec/queue/fts
%attr(755,ossecr,ossec) %dir %{_localstatedir}/ossec/queue/rids
%attr(750,ossec,ossec) %dir %{_localstatedir}/ossec/queue/rootcheck
%attr(750,ossec,ossec) %dir %{_localstatedir}/ossec/queue/syscheck
%attr(550,root,ossec) %dir %{_localstatedir}/ossec/rules
%config %{_localstatedir}/ossec/rules/*
%attr(750,ossec,ossec) %dir %{_localstatedir}/ossec/stats
%attr(550,root,ossec) %dir %{_localstatedir}/ossec/tmp
%attr(550,root,ossec) %dir %{_localstatedir}/ossec/agentless


%changelog
* Mon Feb 11 2013 Didier Fabert <didier.fabert@gmail.com> 2.7-20
- Update to 2.7 final

* Mon Dec 10 2012 Support <support@atomicorp.com> - 2.7-19
- Feature Request #XXX, revert duplicate detection in log events to help detect extremely fast brute force attacks
- Add FORTIFY_SOURCE, PIE, and relro (full)

* Thu Nov 15 2012 Support <support@atomicorp.com> - 2.7-17
- Update to 2.7-rc2 

* Wed Nov 14 2012 Support <support@atomicorp.com> - 2.6-16
- Update to 2.7-rc1

* Wed Aug 1 2012 Support <support@atomicorp.com> - 2.6-15
- Move active response components under the common package 

* Tue Jun 19 2012 Support <support@atomicorp.com> - 2.6-14
- bugfix #xxx, correct ownership permissions on fts dir

* Mon Jun 18 2012 Support <support@atomicorp.com> - 2.6-13
- Update to init script to suppress spurious execd output
- Add alerts queue to server package with ossec/ossec permissions

* Thu Jun 7 2012 Support <support@atomicorp.com> - 2.6-12
- Bugfix #XXX, correct any/agentd condition

* Thu Jun 7 2012 Support <support@atomicorp.com> - 2.6-11
- Moved agentless packages under server

* Mon Apr 16 2012 Support <support@atomicorp.com> - 2.6-10
- Drop timeid and cat_id indexes from schema

* Tue Apr 10 2012 Support <support@atomicorp.com> - 2.6-9
- Add new index, timeid to alerts table.

* Mon Mar 26 2012 Support <support@atomicorp.com> - 2.6-8
- Add cmoraes patch, Adds config options for enabling/disabling rootkit/syscheck options, and agent config profiles
- Add ossec-memleaks patch
- Add agentless directories, and agent.conf
- Bugfix #XXX, ossec-hids.init will now return an exit code on status

* Thu Nov 10 2011 Support <support@atomicorp.com> - 2.6-7
- Add prelink_cmd support

* Tue Aug 23 2011 Support <support@atomicorp.com> - 2.6-6
- Bugfix #XXX, display multi-line events in data table correcty


* Wed Aug 17 2011 Support <support@atomicorp.com> - 2.6-5
- Update to asl-shun.pl purge event to default to 24 hours.

* Fri Aug 05 2011 Support <support@atomicorp.com> - 2.6-4
- Update to asl-shun.pl to change ordering of block rules
- Revert from 0805 snapshot

* Fri Aug 05 2011 Support <support@atomicorp.com> - 2.6-3
- Update to 0805 snapshot

* Mon Aug 01 2011 Support <support@atomicorp.com> - 2.6-2
- Update to 0801 snapshot
- Update asl-shun.pl to log to active-responses.log, blocks now go to the named chain ASL-ACTIVE-RESPONSE, and delete events are more redundant.

* Tue Jul 25 2011 Support <support@atomicorp.com> - 2.6-1
- Update to OSSEC 2.6 Final

* Mon Jul 11 2011 Support <support@atomicorp.com> - 2.6.0-0.10
- Update to snapshot 110711

* Mon Jun 13 2011 Support <support@atomicorp.com> - 2.6.0-0.9
- Update to snapshot 110613

* Thu Jun 9 2011 Support <support@atomicorp.com> - 2.6.0-0.8
- Update to snapshot 110609

* Mon Jun 6 2011 Support <support@atomicorp.com> - 2.6.0-0.7
- Update to snapshot 110606
- Moved ossecr user creation event to the ossec-hids core package

* Tue May 31 2011 Support <support@atomicorp.com> - 2.6.0-0.6
- Update to snapshot 110531

* Wed May 26 2011 Support <support@atomicorp.com> - 2.6.0-0.5
- Update to snapshot 110526

* Wed May 4 2011 Support <support@atomicorp.com> - 2.6.0-0.4
- Update to snapshot 110504

* Wed Apr 20 2011 Support <support@atomicorp.com> - 2.6.0-0.3
- Bugfix #536, Increase the default sleep time for syscheck

* Mon Apr 12 2011 Support <support@atomicorp.com> - 2.6.0-0.1
- Renamed to 2.6 branch

* Wed Apr 6 2011 Support <support@atomicorp.com> - 2.5.1-10
- Add support for the rules/decoders dir system

* Tue Apr 5 2011 Support <support@atomicorp.com> - 2.5.1-9
- Update to snapsot 110405
- Update asl-shun to support ossec alert ids
- First B2PWeb build

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
- minor adjustment in post, to check for config file before overwriting it

* Fri Aug 3 2007 Scott R. Shinn <scott@atomicrocketturtle.com> - 1.2-7
- v6 was first version of the patch.
- added in logging in active-response for better ASL support
- Disabled conf event in post, to keep from overwriting config files. 

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

