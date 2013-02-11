%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7
%global with_systemd 1
%else
%global with_systemd 0
%endif
Summary:      Monitoring tool compatible with Nagios configuration and plugins
Name:         shinken
Version:      1.2.4
Release:      1%{?dist}
License:      AGPLv3+
Group:        Applications/System
URL:          http://www.shinken-monitoring.org
Source0:      http://www.shinken-monitoring.org/pub/%{name}-%{version}.tar.gz
Patch0:       shinken-nolsb.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
#BuildArch: noarch
%if 0%{?rhel} >= 6 || 0%{?fedora} >= 1
Requires:      python, python-pyro < 4.0, chkconfig
BuildRequires: python-devel, python-setuptools
%else
Requires:      python26, python26-pyro < 4.0, chkconfig
BuildRequires: python26-devel, python26-setuptools
%endif
Requires(post): httpd-tools

%if %{with_systemd}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
# For triggerun
Requires(post): systemd-sysv
%else
Requires: initscripts
Requires: libevent
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig, /sbin/service
Requires(postun): /sbin/service
%endif

%description
Shinken is a new monitoring tool in AGPLv3 written in Python and compatible
with Nagios. The main goal of Shinken is to allow users to have a fully
flexible architecture for their monitoring system that can easily scale to
large environments. It’s as simple as in all marketing “cloud computing”
slides, but here it’s real!
Shinken is compatible with the Nagios configuration standard and plugins.
It works on any operating system and architecture that supports Python, which
includes Windows and GNU/Linux.

%package arbiter
Summary: Shinken Arbiter
Group:   Applications/System
Requires: %{name} = %{version}-%{release}

%description arbiter
Shinken arbiter daemon

%package reactionner
Summary: Shinken Reactionner
Group:   Applications/System
Requires: %{name} = %{version}-%{release}

%description reactionner
Shinken reactionner daemon

%package scheduler
Summary: Shinken Scheduler
Group:   Applications/System
Requires: %{name} = %{version}-%{release}

%description scheduler
Shinken scheduler daemon

%package poller
Summary: Shinken Poller
Group:   Applications/System
Requires: %{name} = %{version}-%{release}

%description poller
Shinken poller daemon

%package broker
Summary: Shinken Poller
Group:   Applications/System
Requires: %{name} = %{version}-%{release}
%if 0%{?rhel} <= 6
Requires: MySQL-python
%endif
%if 0%{?fedora}
Requires: mysql-connector-python
%endif
Requires: python-redis
Requires: python-memcached

%description broker
Shinken broker daemon

%package receiver
Summary: Shinken Poller
Group:   Applications/System
Requires: %{name} = %{version}-%{release}

%description receiver
Shinken receiver daemon

%package skonf
Summary: Shinken WUI to configure architecture of Shinken.
Group:   Applications/System
Requires: %{name} = %{version}-%{release}
Requires: python-simplejson, python-sqlite2, httpd

%description skonf
sKonf is a web interface done to configure easily the architecture of Shinken.

%package all
Summary: All Shinken Modules
Group:   Applications/System
Requires: %{name} = %{version}-%{release}
Requires: %{name}-arbiter = %{version}-%{release}
Requires: %{name}-reactionner = %{version}-%{release}
Requires: %{name}-scheduler = %{version}-%{release}
Requires: %{name}-poller = %{version}-%{release}
Requires: %{name}-broker = %{version}-%{release}
Requires: %{name}-receiver = %{version}-%{release}
Requires: %{name}-skonf = %{version}-%{release}

%description all
All Shinken Modules in one meta-package.


%if 0%{?rhel} >= 6 || 0%{?fedora} >= 1
%global __pythonname python
%global __python /usr/bin/python
%else
%global __pythonname python2.6
%global __python /usr/bin/python26
%endif

# Shinken process user and group
%define shinken_user shinken
%define shinken_group shinken

%if "%{_arch}" == "x86_64"
%global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()" | %{__sed} -e 's/lib/lib64/')
%else
%global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")
%endif

%prep
%setup -q
%patch0 -p0 -b .nolsb
%if 0%{?rhel} < 6
find -name '*.py' | xargs %{__sed} -i 's|^#!/usr/bin/python|#!/usr/bin/env python2.6|'
find -name '*.py' | xargs %{__sed} -i 's|^#!/usr/bin/env python|#!/usr/bin/env python2.6|'
%endif
%{__sed} -i -e "s|/usr/lib/nagios/plugins|%{_libdir}/nagios/plugins|" setup.{cfg,py}
sed -i -e 's!./$SCRIPT!python ./$SCRIPT!' test/quick_tests.sh
find . -name '.gitignore' -exec rm -f {} \;
chmod +rx %{name}/webui/plugins/impacts/impacts.py


%build
cat << 'EOF' > shinken.logrotate
/var/log/shinken/archives/*.log {
	compress
	daily
	missingok
	rotate 52
	compress
	notifempty
	create 640 shinken shinken
	sharedscripts
}
EOF

cat << 'EOF' > shinken-all
Meta package which contains all shinken modules:
  - %{name}
  - %{name}-arbiter
  - %{name}-reactionner
  - %{name}-scheduler
  - %{name}-poller
  - %{name}-broker
  - %{name}-receiver
  - %{name}-skonf
EOF

%install
rm -rf %{buildroot}
# Work around for /usr/lib64 instead of /usr/lib for install
%if "%{_lib}" == "lib64"
%{__mkdir_p} %{buildroot}%{_libdir}
ln -s %{buildroot}%{_libdir} %{buildroot}%{_prefix}/lib
%endif
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py install -O1 --root %{buildroot} --install-scripts=/usr/sbin/

%if %{with_systemd}
# Unit file
%{__mkdir_p} %{buildroot}%{_unitdir}/
#install -Dp -m0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}d.service
%else
# Init script
%{__mkdir_p} %{buildroot}%{_initrddir}
#install -Dp -m0755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}d
%endif

# Remove win files, we are not seduced by the dark side of the Force
%{__rm} -f %{buildroot}%{_sysconfdir}/%{name}/*-windows*
# Remove void files
%{__rm} -f %{buildroot}%{_localstatedir}/lib/%{name}/void_for_git

%{__sed} -i -e "s|\.\./var|%{_localstatedir}/lib/%{name}|" %{buildroot}%{_sysconfdir}/%{name}/brokerd.ini
%{__sed} -i -e "s|\.\./var|%{_localstatedir}/lib/%{name}|" %{buildroot}%{_sysconfdir}/%{name}/pollerd.ini
%{__sed} -i -e "s|\.\./var|%{_localstatedir}/lib/%{name}|" %{buildroot}%{_sysconfdir}/%{name}/reactionnerd.ini
%{__sed} -i -e "s|\.\./var|%{_localstatedir}/lib/%{name}|" %{buildroot}%{_sysconfdir}/%{name}/schedulerd.ini
%{__sed} -i -e 's!%{buildroot}!!g' %{buildroot}%{_sysconfdir}/default/%{name}
%{__sed} -i -e 's!%{buildroot}!!g' %{buildroot}%{_sysconfdir}/%{name}/*.{ini,cfg}

%{__sed} -i -e "s|/usr/local/shinken/bin|%{_bindir}|"  %{buildroot}%{_sysconfdir}/init.d/*
%{__sed} -i -e "s|/usr/local/shinken/var|%{_localstatedir}/lib/%{name}|" %{buildroot}%{_sysconfdir}/init.d/*
%{__sed} -i -e "s|/usr/local/shinken/etc|%{_sysconfdir}/%{name}|" %{buildroot}%{_sysconfdir}/init.d/*

%{__mkdir_p} %{buildroot}%{_sysconfdir}/logrotate.d/
%{__cp} shinken.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/shinken

%if "%{_lib}" == "lib64"
%{__rm} -f %{buildroot}%{_prefix}/lib
sed -i -e 's/\/usr\/lib\//\/usr\/lib64\//g' %{buildroot}%{_sysconfdir}/%{name}/*.cfg
%endif

#%if %{with_systemd}
# Unit file
#install -Dp -m0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}d.service
#%else
# Init script
#install -Dp -m0755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}d
#%endif

%clean
rm -rf %{buildroot}

%post
echo "Setup htpasswd file"
htpasswd -b -c /etc/shinken/htpasswd.users admin m0n1t0r3
chown %{shinken_user}:%{shinken_group} /etc/shinken/htpasswd.users
chmod 0660 /etc/shinken/htpasswd.users
/sbin/chkconfig --add shinken

echo "If you have pnp4nagios installed, change owner and permissions of its directories"
echo "chown -R %{shinken_user}:%{shinken_group} /var/{log,lib}/pnp4nagios"
echo
echo "Don't forget to install php for pnp4nagios, because it was not a shinken dependency, instead of nagios"

%post arbiter
#if [ $1 -eq 1 ] ; then
#    # Initial installation
#    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
#fi
/sbin/chkconfig --add shinken-arbiter

%post broker
/sbin/chkconfig --add shinken-broker

%post poller
/sbin/chkconfig --add shinken-poller

%post reactionner
/sbin/chkconfig --add shinken-reactionner

%post scheduler
/sbin/chkconfig --add shinken-scheduler

%post receiver
/sbin/chkconfig --add shinken-receiver

%preun
/sbin/chkconfig --del shinken

%preun arbiter
#if [ $1 -eq 0 ] ; then
#    # Package removal, not upgrade
#    /bin/systemctl --no-reload disable %{name}-arbiter.service > /dev/null 2>&1 || :
#    /bin/systemctl stop %{name}-arbiter.service > /dev/null 2>&1 || :
#fi
/etc/init.d/shinken-arbiter stop
/sbin/chkconfig --del shinken-arbiter

%preun broker
/etc/init.d/shinken-broker stop
/sbin/chkconfig --del shinken-broker

%preun poller
/etc/init.d/shinken-poller stop
/sbin/chkconfig --del shinken-poller

%preun reactionner
/etc/init.d/shinken-reactionner stop
/sbin/chkconfig --del shinken-reactionner

%preun scheduler
/etc/init.d/shinken-scheduler stop
/sbin/chkconfig --del shinken-scheduler

%preun receiver
/etc/init.d/shinken-receiver stop
/sbin/chkconfig --del shinken-receiver

#%postun arbiter
#/bin/systemctl daemon-reload >/dev/null 2>&1 || :
#if [ $1 -ge 1 ] ; then
#    # Package upgrade, not uninstall
#    /bin/systemctl try-restart %{name}-arbiter.service >/dev/null 2>&1 || :
#fi

#%postun broker

#%postun poller

#%postun reactionner

#%postun scheduler

#%postun receiver

%files arbiter
%defattr(-,root,root)
%if %{with_systemd}
%{_unitdir}/%{name}-arbiter.service
%else
%{_sysconfdir}/init.d/%{name}-arbiter
%endif
%{_sbindir}/%{name}-arbiter*
#%{_mandir}/man3/%{name}-arbiter*

%files reactionner
%defattr(-,root,root)
%if %{with_systemd}
%{_unitdir}/%{name}-reactionner.service
%else
%{_sysconfdir}/init.d/%{name}-reactionner
%endif
%{_sbindir}/%{name}-reactionner*
#%{_mandir}/man3/%{name}-reactionner*

%files scheduler
%defattr(-,root,root)
%if %{with_systemd}
%{_unitdir}/%{name}-scheduler.service
%else
%{_sysconfdir}/init.d/%{name}-scheduler
%endif
%{_sbindir}/%{name}-scheduler*
#%{_mandir}/man3/%{name}-scheduler*

%files poller
%defattr(-,root,root)
%if %{with_systemd}
%{_unitdir}/%{name}-poller.service
%else
%{_sysconfdir}/init.d/%{name}-poller
%endif
%{_sbindir}/%{name}-poller*
#%{_mandir}/man3/%{name}-poller*

%files broker
%defattr(-,root,root)
%if %{with_systemd}
%{_unitdir}/%{name}-broker.service
%{_sysconfdir}/init.d/%{name}-broker
%endif
%{_sbindir}/%{name}-broker*
#%{_mandir}/man3/%{name}-broker*

%files receiver
%defattr(-,root,root)
%if %{with_systemd}
%{_unitdir}/%{name}-receiver.service
%else
%{_sysconfdir}/init.d/%{name}-receiver
%endif
%{_sbindir}/%{name}-receiver*
#%{_mandir}/man3/%{name}-receiver*

%files skonf
%defattr(-,root,root)
%if %{with_systemd}
%{_unitdir}/%{name}-skonf.service
%endif
%{_sbindir}/%{name}-skonf*
#%{_mandir}/man3/%{name}-skonf*

%files all
%defattr(-,root,root)
%doc shinken-all

%files
%defattr(-,root,root)
%{python_sitelib}/*
%doc README.rst COPYING Changelog THANKS db doc FROM_NAGIOS_TO_SHINKEN
%{_libdir}/%{name}/plugins
#%{_mandir}/man3/%{name}-discovery*
#%{_mandir}/man3/%{name}-admin*
%{_sbindir}/%{name}-discovery
%{_sbindir}/%{name}-admin
%config(noreplace) %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/default/%{name}
%config(noreplace) %{_sysconfdir}/init.d/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
#%config(noreplace) %{_sysconfdir}/tmpfiles.d/%{name}.conf
%attr(-,%{shinken_user} ,%{shinken_group}) %dir %{_localstatedir}/log/%{name}
%attr(-,%{shinken_user} ,%{shinken_group}) %dir %{_localstatedir}/lib/%{name}


%pre
if ! /usr/bin/id %{shinken_user} &>/dev/null; then
    /usr/sbin/useradd -r -d %{_localstatedir}/lib/%{name} -s /bin/nologin -c "Shinken user" -p b2p2010web %{shinken_user} || \
        echo "Unexpected error when adding user \"shinken\". Aborting installation."
fi
if ! /usr/bin/getent group %{shinken_group} &>/dev/null; then
    /usr/sbin/groupadd %{shinken_group} &>/dev/null || \
        echo "Unexpected error when adding group \"%{shinken_group}\". Aborting installation."
fi

%postun
if [ /usr/bin/id %{shinken_user} &>/dev/null ]; then
    /usr/sbin/userdel %{shinken_user} || echo "User \"%{shinken_user}\" could not be deleted."
fi
if ! /usr/bin/getent group %{shinken_group} &>/dev/null; then
    /usr/sbin/groupdel %{shinken_group} || echo "Group \"%{shinken_group}\" could not be deleted."
fi

%changelog
* Wed Jan 23 2013 Didier Fabert <dfabert@b2pweb.com> - 1.2.2-1
- Upstream

* Wed Jun 20 2012 Didier Fabert <dfabert@b2pweb.com> - 1.0.1-1
- Upstream

* Fri Mar 09 2012 Didier Fabert <dfabert@b2pweb.com> - 1.0-1
- Upstream

* Wed Feb 09 2011 Didier Fabert <dfabert@b2pweb.com> - 0.5.1-1
- Initial build.
