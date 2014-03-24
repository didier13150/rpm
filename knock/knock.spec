%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7
%global with_systemd 1
%else
%global with_systemd 0
%endif

Summary:          Port-knocking tools
Name:             knock
Version:          0.5
Release:          4%{?dist}
License:          GPLv2
Group:            Applications/System
URL:              http://www.zeroflux.org
Source0:          http://www.zeroflux.org/proj/knock/files/%{name}-%{version}.tar.gz
Source1:          knockd.service
Source2:          knockd.init
Patch0:           knock-path-max.patch
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:         libpcap
BuildRequires:    libpcap-devel
%if %{with_systemd}
BuildRequires:    systemd
%endif

%description
A knock client makes the port-hits by sending a TCP (or UDP) packet to a port
on the server. This port need not be open -- since knockd listens at the link-
layer level, it sees all traffic even if it's destined for a closed port.

%package server
Requires:         %{name} = %{version}-%{release}
Summary:          Port-knocking server
Group:            System Environment/Daemons
%if %{with_systemd}
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
# For triggerun
Requires(post):   systemd-sysv
%else
Requires: initscripts
Requires: libevent
Requires(post):   /sbin/chkconfig
Requires(preun):  /sbin/chkconfig, /sbin/service
Requires(postun): /sbin/service
%endif

%description server
knockd is a port-knock server. It listens to all traffic on an ethernet
interface, looking for special "knock" sequences of port-hits.

When the server detects a specific sequence of port-hits, it runs a
command defined in its configuration file. This can be used to open up
holes in a firewall for quick access.

%prep
%setup -q
%patch0 -p0

%build
%configure \
        --disable-schemas-install
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}
%{__mkdir_p} %{buildroot}%{_sysconfdir}/sysconfig
%if %{with_systemd}
# Unit file
%{__mkdir_p} %{buildroot}%{_unitdir}
install -Dp -m0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}d.service
%else
# Init script
%{__mkdir_p} %{buildroot}%{_initrddir}
install -Dp -m0755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}d
%endif

%{__sed} -i -e "/command/ s|/usr/sbin/iptables|/sbin/iptables|g" %{buildroot}%{_sysconfdir}/%{name}d.conf

# Default config
cat << EOF > %{buildroot}%{_sysconfdir}/sysconfig/%{name}d
## knockd daemon

# Network interface to listen on (default is eth0 )
KNOCKD_IFACE=eth0

# Config file to use ( default is /etc/knockd.conf )
#KNOCKD_CONF_FILE=/etc/knockd.conf

OPTIONS="-c \${KNOCKD_CONF_FILE} -i \${KNOCKD_IFACE}"

EOF

%clean
%{__rm} -rf %{buildroot}

%post server
%if 0%{?systemd_post:1}
%systemd_post %{name}d.service
%else
if [ $1 = 1 ]; then
# Initial installation
%if %{with_systemd}
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
%else
    /sbin/chkconfig --add %{name}d
%endif
fi
%endif

%preun server
%if 0%{?systemd_preun:1}
%systemd_preun %{name}d.service
%else
if [ "$1" = 0 ] ; then
# Package removal, not upgrade
%if %{with_systemd}
    /bin/systemctl --no-reload disable %{name}d.service >/dev/null 2>&1 || :
    /bin/systemctl stop %{name}d.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name}d stop > /dev/null 2>&1
    /sbin/chkconfig --del %{name}d
%endif
fi
exit 0
%endif

%postun server
%if 0%{?systemd_postun_with_restart:1}
%systemd_postun_with_restart %{name}d.service
%else
%if %{with_systemd}
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ]; then
# Package upgrade, not uninstall
    /bin/systemctl try-restart %{name}d.service >/dev/null 2>&1 || :
fi
%else
if [ "$1" -ge 1 ]; then
    /sbin/service %{name}d restart > /dev/null 2>&1
fi
exit 0
%endif
%endif

%triggerun -- knockd
%if %{with_systemd}
if [ -f /etc/rc.d/init.d/knockd ]; then
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply memcached
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save knockd >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del knockd >/dev/null 2>&1 || :
/bin/systemctl try-restart knockd.service >/dev/null 2>&1 || :
fi
%endif

%files
%defattr(-, root, root, 0755)
%doc ChangeLog COPYING  README TODO
%doc %{_mandir}/man?/%{name}.*
%{_bindir}/%{name}

%files server
%defattr(-, root, root, 0755)
%config(noreplace) %{_sysconfdir}/%{name}d.conf
%{_sbindir}/%{name}d
%{_sysconfdir}/sysconfig/%{name}d
%if %{with_systemd}
%{_unitdir}/%{name}d.service
%else
%attr(0755,root,root) %{_initrddir}/%{name}d
%endif
%doc %{_mandir}/man?/%{name}d.*

%changelog
* Sun Jan 20 2013 Didier Fabert <didier.fabert@gmail.com> 0.5-4
- Add patch for fedora (systemd)

* Mon Nov 14 2011 Didier Fabert <didier.fabert@gmail.com> 0.5-3
- Add patch for CentOS-6

* Thu Sep 22 2011 Didier Fabert <didier.fabert@gmail.com> 0.5-2
- rebuild against libpcap 0.9.4 instead of 1.0.0 for CentOS-5

* Fri May 20 2011 Didier Fabert <didier.fabert@gmail.com> 0.5-1
- First B2PWeb package
