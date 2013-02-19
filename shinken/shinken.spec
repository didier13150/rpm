%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7
%global with_systemd 1
%else
%global with_systemd 0
%endif

%if 0%{?rhel} >= 6 || 0%{?fedora} >= 1
%global __pythonname python
%global __python /usr/bin/python
%else
%global __pythonname python2.6
%global __python /usr/bin/python26
%endif
%global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")

# Shinken process user and group
%define shinken_user shinken
%define shinken_group shinken

Summary:      Monitoring tool compatible with Nagios configuration and plugins
Name:         shinken
Version:      1.2.4
Release:      1%{?dist}
License:      AGPLv3+
Group:        Applications/System
URL:          http://www.shinken-monitoring.org
Source0:      http://www.shinken-monitoring.org/pub/%{name}-%{version}.tar.gz
Patch0:       shinken-user-on-init-scripts.patch

%if 0%{?rhel} >= 6 || 0%{?fedora} >= 1
Requires:      python, python-pyro, chkconfig
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

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:    noarch

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
Summary: Shinken WUI to configure architecture of Shinken
Group:   Applications/System
Requires: %{name} = %{version}-%{release}
Requires: python-simplejson, python-sqlite2, httpd

%description skonf
sKonf is a web interface done to configure easily the architecture of Shinken

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
All Shinken Modules in one meta-package


%prep
%setup -q
%patch0 -p1 -b .hcuser

%if 0%{?rhel} < 6
find -name '*.py' | xargs %{__sed} -i 's|^#!/usr/bin/python|#!/usr/bin/env python2.6|'
find -name '*.py' | xargs %{__sed} -i 's|^#!/usr/bin/env python|#!/usr/bin/env python2.6|'
%endif
sed -i -e 's!./$SCRIPT!%{__python} ./$SCRIPT!' test/quick_tests.sh
%{__sed} -i -e "s|/usr/lib/nagios/plugins|%{_libdir}/nagios/plugins|" setup.{cfg,py}
find . -name '.gitignore' -exec rm -f {} \;
chmod +rx %{name}/webui/plugins/impacts/impacts.py
rm -rf  shinken/webui/plugins/eue 

%{__sed} -i -e "s#@user@:@group@#%{shinken_user}:%{shinken_group}#" for_fedora/init.d/*

%build
%{__python} setup.py build

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

cat << 'EOF' > %{name}-tmpfiles.d.conf
d /var/run/shinken   710 %{shinken_user} %{shinken_group}
EOF

%install
rm -rf %{buildroot}
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py install -O1 --skip-build --root %{buildroot} --install-scripts=%{_sbindir}

# Remove empty files
find %{buildroot} -size 0 -delete

# Remove win files, we are not seduced by the dark side of the Force
%{__rm} -f %{buildroot}%{_sysconfdir}/%{name}/*-windows*
# Remove void files
find %{buildroot}%{_localstatedir} -name '*void_for_git*' -delete

%{__sed} -i -e "s|\.\./var|%{_localstatedir}/lib/%{name}|" %{buildroot}%{_sysconfdir}/%{name}/brokerd.ini
%{__sed} -i -e "s|\.\./var|%{_localstatedir}/lib/%{name}|" %{buildroot}%{_sysconfdir}/%{name}/pollerd.ini
%{__sed} -i -e "s|\.\./var|%{_localstatedir}/lib/%{name}|" %{buildroot}%{_sysconfdir}/%{name}/reactionnerd.ini
%{__sed} -i -e "s|\.\./var|%{_localstatedir}/lib/%{name}|" %{buildroot}%{_sysconfdir}/%{name}/schedulerd.ini
%{__sed} -i -e 's!%{buildroot}!!g' %{buildroot}%{_sysconfdir}/%{name}/*.{ini,cfg}

%if %{with_systemd}
# Unit file
 rm -rf %{buildroot}%{_sysconfdir}/init.d
%{__mkdir_p} %{buildroot}%{_unitdir}/
%{__cp} for_fedora/systemd/shinken-arbiter.service %{buildroot}%{_unitdir}/shinken-arbiter.service
%{__cp} for_fedora/systemd/shinken-broker.service %{buildroot}%{_unitdir}/shinken-broker.service
%{__cp} for_fedora/systemd/shinken-poller.service %{buildroot}%{_unitdir}/shinken-poller.service
%{__cp} for_fedora/systemd/shinken-reactionner.service %{buildroot}%{_unitdir}/shinken-reactionner.service
%{__cp} for_fedora/systemd/shinken-receiver.service %{buildroot}%{_unitdir}/shinken-receiver.service
%{__cp} for_fedora/systemd/shinken-scheduler.service %{buildroot}%{_unitdir}/shinken-scheduler.service
%{__cp} for_fedora/systemd/shinken-skonf.service %{buildroot}%{_unitdir}/shinken-skonf.service
%else
# Init script
%{__mkdir_p} %{buildroot}%{_initrddir}
%{__cp} for_fedora/init.d/shinken-arbiter %{buildroot}%{_initrddir}/shinken-arbiter
%{__cp} for_fedora/init.d/shinken-broker %{buildroot}%{_initrddir}/shinken-broker
%{__cp} for_fedora/init.d/shinken-poller %{buildroot}%{_initrddir}/shinken-poller
%{__cp} for_fedora/init.d/shinken-reactionner %{buildroot}%{_initrddir}/shinken-reactionner
%{__cp} for_fedora/init.d/shinken-receiver %{buildroot}%{_initrddir}/shinken-receiver
%{__cp} for_fedora/init.d/shinken-scheduler %{buildroot}%{_initrddir}/shinken-scheduler
%{__cp} for_fedora/init.d/shinken-skonf %{buildroot}%{_initrddir}/shinken-skonf
%endif

find  %{buildroot}%{python_sitelib}/%{name}/webui/htdocs -type f -exec chmod -x {} \;
find  %{buildroot}%{python_sitelib}/%{name} -name '*.tpl' -exec chmod -x {} \;
find  %{buildroot}%{python_sitelib}/%{name} -name '*.js' -exec chmod -x {} \;
find  %{buildroot}%{python_sitelib}/%{name} -name '*.css' -exec chmod -x {} \;
find  %{buildroot}%{python_sitelib}/%{name} -name '*.png' -exec chmod -x {} \;

%{__mkdir_p} %{buildroot}%{_sysconfdir}/logrotate.d/
%{__cp} shinken.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/shinken

install -d -m0755 %{buildroot}%{_sysconfdir}/tmpfiles.d
install -m0644 %{name}-tmpfiles.d.conf %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf

install -d -m0755 %{buildroot}%{_usr}/lib/%{name}/plugins
install  -m0755 libexec/*{.py,.ini} %{buildroot}%{_usr}/lib/%{name}/plugins

install -d -m0755 %{buildroot}%{_mandir}/man3
install -p -m0644 doc/man/* %{buildroot}%{_mandir}/man3

%{__sed} -i -e "s|\.\./var|%{_localstatedir}/lib/%{name}|" %{buildroot}%{_sysconfdir}/%{name}/brokerd.ini
%{__sed} -i -e "s|\.\./var|%{_localstatedir}/lib/%{name}|" %{buildroot}%{_sysconfdir}/%{name}/pollerd.ini
%{__sed} -i -e "s|\.\./var|%{_localstatedir}/lib/%{name}|" %{buildroot}%{_sysconfdir}/%{name}/reactionnerd.ini
%{__sed} -i -e "s|\.\./var|%{_localstatedir}/lib/%{name}|" %{buildroot}%{_sysconfdir}/%{name}/schedulerd.ini
%{__sed} -i -e 's!%{buildroot}!!g' %{buildroot}%{_sysconfdir}/default/%{name}
%{__sed} -i -e 's!%{buildroot}!!g' %{buildroot}%{_sysconfdir}/%{name}/*.{ini,cfg}

sed -i -e 's!/usr/local/shinken/libexec!%{_libdir}/nagios/plugins!' %{buildroot}%{_sysconfdir}/%{name}/resource.cfg
sed -i -e 's!/usr/lib/nagios/plugins!%{_libdir}/nagios/plugins!' %{buildroot}%{_sysconfdir}/%{name}/resource.cfg
sed -i -e "s!/usr/local/shinken/src/!%{_sbindir}!" FROM_NAGIOS_TO_SHINKEN
sed -i -e "s!/usr/local/nagios/etc/!%{_sysconfdir}/shinken/!" FROM_NAGIOS_TO_SHINKEN
sed -i -e "s!/usr/local/shinken/src/etc/!%{_sysconfdir}/shinken/!" FROM_NAGIOS_TO_SHINKEN
sed -i -e 's!(you can also be even more lazy and call the bin/launch_all.sh script).!!' FROM_NAGIOS_TO_SHINKEN

chmod +x %{buildroot}%{python_sitelib}/%{name}/*.py

%{__rm} -f %{buildroot}%{_sysconfdir}/default/%{name}

%clean
rm -rf %{buildroot}

%post
echo "Setup htpasswd file"
htpasswd -b -c /etc/shinken/htpasswd.users admin m0n1t0r3
chown %{shinken_user}:%{shinken_group} /etc/shinken/htpasswd.users
chmod 0660 /etc/shinken/htpasswd.users

echo "If you have pnp4nagios installed, change owner and permissions of its directories"
echo "chown -R %{shinken_user}:%{shinken_group} /var/{log,lib}/pnp4nagios"
echo
echo "Don't forget to install php for pnp4nagios, because it's not a shinken dependency, instead of nagios"

%pre
if ! /usr/bin/id %{shinken_user} &>/dev/null; then
    /usr/sbin/useradd -r -d %{_localstatedir}/lib/%{name} -s /bin/nologin -c "Shinken user" -p shinkenpasswd %{shinken_user} || \
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

%post arbiter
if [ $1 -eq 1 ] ; then 
  %if %{with_systemd}
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  %else
    /sbin/chkconfig --add %{name}-arbiter || :
  %endif
fi

%post broker
if [ $1 -eq 1 ] ; then 
  %if %{with_systemd}
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  %else
    /sbin/chkconfig --add %{name}-broker || :
%endif
fi

%post poller
if [ $1 -eq 1 ] ; then 
  %if %{with_systemd}
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  %else
    /sbin/chkconfig --add %{name}-poller || :
  %endif
fi

%post reactionner
if [ $1 -eq 1 ] ; then 
  %if %{with_systemd}
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  %else
    /sbin/chkconfig --add %{name}-reactionner || :
%endif
fi

%post scheduler
if [ $1 -eq 1 ] ; then 
  %if %{with_systemd}
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  %else
    /sbin/chkconfig --add %{name}-scheduler || :
  %endif
fi

%post receiver
if [ $1 -eq 1 ] ; then 
  %if %{with_systemd}
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  %else
    /sbin/chkconfig --add %{name}-receiver || :
  %endif
fi

%preun arbiter 
if [ $1 -eq 0 ] ; then
  %if %{with_systemd}
    /bin/systemctl --no-reload disable %{name}-arbiter.service > /dev/null 2>&1 || :
    /bin/systemctl stop %{name}-arbiter.service > /dev/null 2>&1 || :
  %else
    /sbin/service %{name}-arbiter stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}-arbiter || :
  %endif
fi

%preun broker 
if [ $1 -eq 0 ] ; then
  %if %{with_systemd}
    /bin/systemctl --no-reload disable %{name}-broker.service > /dev/null 2>&1 || :
    /bin/systemctl stop %{name}-broker.service > /dev/null 2>&1 || :
  %else
    /sbin/service %{name}-broker stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}-broker || :
  %endif
fi

%preun poller 
if [ $1 -eq 0 ] ; then
  %if %{with_systemd}
    /bin/systemctl --no-reload disable %{name}-poller.service > /dev/null 2>&1 || :
    /bin/systemctl stop %{name}-poller.service > /dev/null 2>&1 || :
  %else
    /sbin/service %{name}-poller stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}-poller || :
  %endif
fi

%preun reactionner 
if [ $1 -eq 0 ] ; then
  %if %{with_systemd}
    /bin/systemctl --no-reload disable %{name}-reactionner.service > /dev/null 2>&1 || :
    /bin/systemctl stop %{name}-reactionner.service > /dev/null 2>&1 || :
  %else
    /sbin/service %{name}-reactionner stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}-reactionner || :
  %endif
fi

%preun scheduler 
if [ $1 -eq 0 ] ; then
  %if %{with_systemd}
    /bin/systemctl --no-reload disable %{name}-scheduler.service > /dev/null 2>&1 || :
    /bin/systemctl stop %{name}-scheduler.service > /dev/null 2>&1 || :
  %else
    /sbin/service %{name}-scheduler stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}-scheduler || :
  %endif
fi

%preun receiver 
if [ $1 -eq 0 ] ; then
  %if %{with_systemd}
    /bin/systemctl --no-reload disable %{name}-receiver.service > /dev/null 2>&1 || :
    /bin/systemctl stop %{name}-receiver.service > /dev/null 2>&1 || :
  %else
    /sbin/service %{name}-receiver stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}-receiver || :
  %endif
fi

%postun arbiter
%if %{with_systemd}
  /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  if [ $1 -ge 1 ] ; then
    /bin/systemctl try-restart %{name}-arbiter.service >/dev/null 2>&1 || :
  fi
%endif

%postun broker
%if %{with_systemd}
  /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  if [ $1 -ge 1 ] ; then
    /bin/systemctl try-restart %{name}-broker.service >/dev/null 2>&1 || :
  fi
%endif

%postun poller
%if %{with_systemd}
  /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  if [ $1 -ge 1 ] ; then
    /bin/systemctl try-restart %{name}-poller.service >/dev/null 2>&1 || :
  fi
%endif

%postun reactionner
%if %{with_systemd}
  /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  if [ $1 -ge 1 ] ; then
    /bin/systemctl try-restart %{name}-reactionner.service >/dev/null 2>&1 || :
  fi
%endif

%postun scheduler
%if %{with_systemd}
  /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  if [ $1 -ge 1 ] ; then
    /bin/systemctl try-restart %{name}-scheduler.service >/dev/null 2>&1 || :
  fi
%endif

%postun receiver
%if %{with_systemd}
  /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  if [ $1 -ge 1 ] ; then
    /bin/systemctl try-restart %{name}-receiver.service >/dev/null 2>&1 || :
  fi
%endif

%files arbiter
%if %{with_systemd}
  %{_unitdir}/%{name}-arbiter.service
%else
  %attr(0755,root,root) %{_initrddir}/%{name}-arbiter
%endif
%{_sbindir}/%{name}-arbiter*
%{_mandir}/man3/%{name}-arbiter*

%files reactionner
%if %{with_systemd}
  %{_unitdir}/%{name}-reactionner.service
%else
  %attr(0755,root,root) %{_initrddir}/%{name}-reactionner
%endif
%{_sbindir}/%{name}-reactionner*
%{_mandir}/man3/%{name}-reactionner*

%files scheduler
%if %{with_systemd}
  %{_unitdir}/%{name}-scheduler.service
%else
  %attr(0755,root,root) %{_initrddir}/%{name}-scheduler
%endif
%{_sbindir}/%{name}-scheduler*
%{_mandir}/man3/%{name}-scheduler*

%files poller
%if %{with_systemd}
  %{_unitdir}/%{name}-poller.service
%else
  %attr(0755,root,root) %{_initrddir}/%{name}-poller
%endif
%{_sbindir}/%{name}-poller*
%{_mandir}/man3/%{name}-poller*

%files broker
%if %{with_systemd}
  %{_unitdir}/%{name}-broker.service
%else
  %attr(0755,root,root) %{_initrddir}/%{name}-broker
%endif
%{_sbindir}/%{name}-broker*
%{_mandir}/man3/%{name}-broker*

%files receiver
%if %{with_systemd}
  %{_unitdir}/%{name}-receiver.service
%else
  %attr(0755,root,root) %{_initrddir}/%{name}-receiver
%endif
%{_sbindir}/%{name}-receiver*
%{_mandir}/man3/%{name}-receiver*

%files skonf
%if %{with_systemd}
  %{_unitdir}/%{name}-skonf.service
%else
  %attr(0755,root,root) %{_initrddir}/%{name}-skonf
%endif
%{_sbindir}/%{name}-skonf*
%{_mandir}/man3/%{name}-skonf*

%files all
%defattr(-,root,root)
%doc shinken-all

%files
%{python_sitelib}/%{name}
%{python_sitelib}/Shinken-%{version}-py*.egg-info
%doc etc/packs README.rst COPYING Changelog THANKS db doc FROM_NAGIOS_TO_SHINKEN
%{_sbindir}/%{name}-receiver*
%{_sbindir}/%{name}-discovery
%{_sbindir}/%{name}-admin
%{_sbindir}/%{name}-hostd
%{_sbindir}/%{name}-packs
%{_mandir}/man3/%{name}-admin*
%{_mandir}/man3/%{name}-discovery*
%{_usr}/lib/%{name}/plugins
%config(noreplace) %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/tmpfiles.d/%{name}.conf
%attr(-,%{shinken_user} ,%{shinken_group}) %dir %{_localstatedir}/log/%{name}
%attr(-,%{shinken_user} ,%{shinken_group}) %dir %{_localstatedir}/lib/%{name}
%attr(-,%{shinken_user} ,%{shinken_group}) %dir %{_localstatedir}/run/%{name}

%changelog
* Wed Jan 23 2013 Didier Fabert <dfabert@b2pweb.com> - 1.2.2-1
- Update from upstream

* Wed Jun 20 2012 Didier Fabert <dfabert@b2pweb.com> - 1.0.1-1
- Update from upstream

* Fri Mar 09 2012 Didier Fabert <dfabert@b2pweb.com> - 1.0-1
- Update from upstream

* Wed Feb 09 2011 Didier Fabert <dfabert@b2pweb.com> - 0.5.1-1
- Initial build.
