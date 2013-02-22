%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7
%global with_systemd 1
%else
%global with_systemd 0
%endif

Name:          pnp4nagios
Version:       0.6.19
Release:       1%{?dist}
License:       GPLv2
URL:           http://pnp4nagios.org
Source0:       http://sourceforge.net/projects/pnp4nagios/files/PNP-0.6/%{name}-%{version}.tar.gz
Source1:       npcd.service
Group:         Applications/Productivity
BuildRoot:     %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
Summary:       A performance data graphing solution

%if %{with_systemd}
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
# For triggerun
Requires(post):   systemd-sysv
%else
Requires:         initscripts
Requires:         libevent
Requires(post):   /sbin/chkconfig
Requires(preun):  /sbin/chkconfig, /sbin/service
Requires(postun): /sbin/service
%endif
BuildRequires:    rrdtool-devel
BuildRequires:    rrdtool-perl
BuildRequires:    perl(Time::HiRes)
Requires:         perl(Gearman::Worker), perl(Crypt::Rijndael)
Requires:         rrdtool
Requires:         perl(Time::HiRes)
Requires:         shinken
Requires(post):   httpd-tools

%description
PNP is an add-on to Nagios which analyzes performance data provided by plugins
and stores them automatically into RRD-databases (Round Robin Databases, see
RRD Tool).

%prep
echo %{_arch}
%setup -q
%{__sed} -i -e 's/MANDIR=@mandir@/MANDIR=\/usr\/share\/man/' man/Makefile.in

%build
%configure --with-nagios-user=shinken \
    --with-nagios-group=shinken \
    --sysconfdir=%{_sysconfdir}/%{name} \
    --libdir=%{_datadir}/%{name} \
    --datarootdir=%{_datadir}/%{name} \
    --with-perfdata-dir=%{_localstatedir}/lib/pnp4nagios \
    --with-perfdata-spool-dir=%{_localstatedir}/lib/pnp4nagios/spool \
    --with-perfdata-logfile=%{_localstatedir}/log/pnp4nagios/pnp4nagios.log

%{__make} all %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_localstatedir}/log/pnp4nagios
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
mkdir -p %{buildroot}%{_localstatedir}/lib/pnp4nagios
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
%{__make} install fullinstall DESTDIR=$RPM_BUILD_ROOT INIT_OPTS= INSTALL_OPTS=


%{__cp} %{buildroot}%{_sysconfdir}/%{name}/rra.cfg-sample %{buildroot}%{_sysconfdir}/%{name}/rra.cfg
%{__sed} -i -e "/AuthUserFile/ s|/usr/local/nagios/etc/htpasswd.users|/etc/pnp4nagios/pnp4nagios.htpasswd|" \
    %{buildroot}%{_sysconfdir}/httpd/conf.d/pnp4nagios.conf

%{__sed} -i -e 's#log_file = /var/npcd.log#log_file = /var/log/pnp4nagios/npcd.log#' %{buildroot}%{_sysconfdir}/%{name}/npcd.cfg

%if %{with_systemd}
# Unit file
%{__mkdir_p} %{buildroot}%{_unitdir}/
install -Dp -m0644 %{SOURCE1} %{buildroot}%{_unitdir}/npcd.service
%{__rm} %{buildroot}%{_initrddir}/npcd
%endif
%{__rm} %{buildroot}%{_initrddir}/pnp_gearman_worker
%{__mkdir_p} %{buildroot}%{_libdir}/%{name}
%{__mv} %{buildroot}%{_datadir}/%{name}/npcdmod.o %{buildroot}%{_libdir}/%{name}/

%clean
rm -rf $RPM_BUILD_ROOT

%post 
%if 0%{?systemd_post:1}
%systemd_post npcd.service
%else
if [ $1 = 1 ]; then
# Initial installation
%if %{with_systemd}
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
%else
    /sbin/chkconfig --add npcd
%endif
fi
%endif
/sbin/ldconfig
echo "Setup /etc/pnp4nagios/pnp4nagios.htpasswd file with default account: admin, password: admin"
htpasswd -b -c /etc/pnp4nagios/pnp4nagios.htpasswd admin admin

%preun
%if 0%{?systemd_preun:1}
%systemd_preun npcd.service
%else
if [ "$1" = 0 ] ; then
# Package removal, not upgrade
%if %{with_systemd}
    /bin/systemctl --no-reload disable npcd.service >/dev/null 2>&1 || :
    /bin/systemctl stop npcd.service >/dev/null 2>&1 || :
%else
    /sbin/service npcd stop > /dev/null 2>&1
    /sbin/chkconfig --del npcd
%endif
fi
exit 0
%endif
/sbin/ldconfig

%postun
%if 0%{?systemd_postun_with_restart:1}
%systemd_postun_with_restart npcd.service
%else
%if %{with_systemd}
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ]; then
# Package upgrade, not uninstall
    /bin/systemctl try-restart npcd.service >/dev/null 2>&1 || :
fi
%else
if [ "$1" -ge 1 ]; then
    /sbin/service npcd restart > /dev/null 2>&1
fi
exit 0
%endif
%endif

%triggerun -- npcd
%if %{with_systemd}
if [ -f /etc/rc.d/init.d/npcd ]; then
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply npcd
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save npcd >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del npcd >/dev/null 2>&1 || :
/bin/systemctl try-restart npcd.service >/dev/null 2>&1 || :
fi
%endif

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING INSTALL README THANKS
%config(noreplace) %{_sysconfdir}/%{name}/npcd.cfg
%config(noreplace) %{_sysconfdir}/%{name}/rra.cfg
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%config %{_sysconfdir}/%{name}/process_perfdata.cfg
%config %{_sysconfdir}/%{name}/pages/web_traffic.cfg-sample
%config %{_sysconfdir}/%{name}/check_commands/check_nwstat.cfg-sample
%config %{_sysconfdir}/%{name}/check_commands/check_all_local_disks.cfg-sample
%config %{_sysconfdir}/%{name}/check_commands/check_nrpe.cfg-sample
%config %{_sysconfdir}/%{name}/background.pdf
%config %{_sysconfdir}/%{name}/config.php*
%config %{_sysconfdir}/%{name}/config_local.php
%config %{_sysconfdir}/%{name}/misccommands.cfg-sample
%config %{_sysconfdir}/%{name}/nagios.cfg-sample
%config %{_sysconfdir}/%{name}/pnp4nagios_release
%config %{_sysconfdir}/%{name}/rra.cfg-sample
%docdir %{_defaultdocdir}
%if %{with_systemd}
%{_unitdir}/npcd.service
%else
%attr(0755,root,root) %{_initrddir}/npcd
%endif
%{_bindir}/npcd
%{_libdir}/%{name}/npcdmod.o
%{_libexecdir}/check_pnp_rrds.pl
%{_libexecdir}/rrd_modify.pl
%{_libexecdir}/process_perfdata.pl
%{_libexecdir}/rrd_convert.pl
%{_datadir}/%{name}
%{_mandir}/man8/npcd.8.gz
%defattr(-,shinken,shinken)
%{_localstatedir}/lib/%{name}
%{_localstatedir}/log/%{name}

%changelog
* Thu Feb 21 2013 Didier Fabert <didier.fabert@gmail.com> 0.6.19-1
- First release
