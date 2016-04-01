Name:           netdata
Version:        1.0.0
Release:        1%{?dist}
Summary:        Real-time performance monitoring
License:        GPLv3
Group:          Applications/Productivity
URL:            https://github.com/firehol/%{name}
Source0:        https://github.com/firehol/%{name}/archive/v%{version}.tar.gz
Source1:        netdata.conf
Source2:        netdata.tmpfiles.conf

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  zlib-devel
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  git
BuildRequires:  autoconf
BuildRequires:  autogen
BuildRequires:  automake
BuildRequires:  pkgconfig
BuildRequires:  systemd
Requires:       nodejs


%description
netdata is a highly optimized Linux daemon providing real-time performance
monitoring for Linux systems, Applications, SNMP devices, over the web!

It tries to visualize the truth of now, in its greatest detail, so that you
can get insights of what is happening now and what just happened, on your
systems and applications.

%prep
%setup -qn %{name}-%{version}

%build
./autogen.sh
%configure \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir} \
    --localstatedir=%{_localstatedir} \
    --with-zlib --with-math --with-user=netdata
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name '.keep' -delete
# Unit file
%{__mkdir_p} %{buildroot}%{_unitdir}
%{__mkdir_p} %{buildroot}%{_tmpfilesdir}
install -Dp -m0644 system/netdata-systemd %{buildroot}%{_unitdir}/%{name}.service
install %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install %{SOURCE2} %{buildroot}%{_tmpfilesdir}/%{name}.conf

%pre
getent group netdata > /dev/null || groupadd -r netdata
getent passwd netdata > /dev/null || useradd -r -g netdata -c "NetData User" -s /sbin/nologin -d /var/log/%{name} netdata

%post
%if 0%{?systemd_post:1}
%systemd_post %{name}.service
%else
if [ $1 = 1 ]; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
%endif

%preun
%if 0%{?systemd_preun:1}
%systemd_preun %{name}.service
%else
if [ "$1" = 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable %{name}.service >/dev/null 2>&1 || :
    /bin/systemctl stop %{name}.service >/dev/null 2>&1 || :
fi
exit 0
%endif

%postun
%if 0%{?systemd_postun_with_restart:1}
%systemd_postun_with_restart %{name}.service
%else
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ]; then
# Package upgrade, not uninstall
    /bin/systemctl try-restart %{name}.service >/dev/null 2>&1 || :
fi
%endif

%files
%doc README.md ChangeLog
%{_sbindir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}
%{_libexecdir}/%{name}
%dir %{_datadir}/%{name}
%attr(0755, netdata, netdata) %{_datadir}/%{name}/web
%{_unitdir}/%{name}.service
%{_tmpfilesdir}/%{name}.conf
%attr(0755, netdata, netdata) %dir %{_localstatedir}/cache/%{name}
%attr(0755, netdata, netdata) %dir %{_localstatedir}/log/%{name}
%attr(4755,root,root) %{_libexecdir}/%{name}/plugins.d/apps.plugin

%changelog
* Fri Apr 01 2016 Didier Fabert <didier.fabert@gmail.com> 1.0.0-1
- First Release
