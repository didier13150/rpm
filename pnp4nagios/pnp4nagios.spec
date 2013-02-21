Name:          pnp4nagios
Version:       0.6.19
Release:       1%{?dist}
License:       GPLv2
URL:           http://pnp4nagios.org
Source:        http://sourceforge.net/projects/pnp4nagios/files/PNP-0.6/%{name}-%{version}.tar.gz
Group:         Applications/Monitoring
BuildRoot:     %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
Summary:       Gearman version of pnp4nagios

BuildRequires: rrdtool-devel
BuildRequires: perl(Time::HiRes)
Requires:      perl(Gearman::Worker), perl(Crypt::Rijndael)
Requires:      rrdtool
Requires:      perl(Time::HiRes)
Requires:      shinken

%description
From the web page (http://docs.pnp4nagios.org/pnp-0.6/start):

PNP is an addon to Nagios which analyzes performance data provided by plugins
and stores them automatically into RRD-databases (Round Robin Databases, see
RRD Tool).

This is the version with support for Gearman, suitable to use with mod_gearman.

%prep
echo %{_arch}
%setup -q

%build
./configure --with-nagios-user=shinken \
    --with-nagios-group=shinken \
    --sysconfdir=%{_sysconfdir}/%{name} \
    --localstatedir=%{_localstatedir} \
    --sbindir=%{_sbindir} \
    --libdir=%{_libdir}/%{name} \
    --with-init-dir=%{_initrddir} \
    --with-layout=debian \
    --with-perfdata-dir=%{_localstatedir}/lib/pnp4nagios \
    --with-perfdata-spool-dir=%{_localstatedir}/lib/pnp4nagios/spool \
    --with-perfdata-logfile=%{_localstatedir}/log/pnp4nagios/pnp4nagios.log


%{__make} all %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/log/pnp4nagios
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}
mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/lib/pnp4nagios
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/nagios/ssi/
%{__make} install fullinstall DESTDIR=$RPM_BUILD_ROOT INIT_OPTS= INSTALL_OPTS=

%{__mv} $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/misccommands.cfg-sample $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/misccommands.cfg
# no need in >= 0.6.12
# %{__mv} $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/npcd.cfg-sample $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/npcd.cfg
# %{__mv} $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/process_perfdata.cfg-sample $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/process_perfdata.cfg
# need on >= 0.6.12
%{__mv} $RPM_BUILD_ROOT/man $RPM_BUILD_ROOT/%{_datadir}


%{__mv} $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/rra.cfg-sample $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/rra.cfg
%{__mv} $RPM_BUILD_ROOT/%{_datadir}/%{name}/html/install.php $RPM_BUILD_ROOT/%{_datadir}/%{name}/html/install-saved.php
%{__sed} -i -e "/AuthUserFile/ s|/usr/local/nagios/etc/htpasswd.users|/etc/httpd/conf.d/nagios.htpasswd|" $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d/pnp4nagios.conf

cp contrib/ssi/*.ssi $RPM_BUILD_ROOT/%{_datadir}/nagios/ssi/

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
echo
echo "Change value in your nagios.cfg file for \"process_performance_data=1\""
echo "Add \"broker_module=%{_libdir}/%{name}/npcdmod.o config_file=%{_sysconfdir}/%{name}/npcd.cfg\" to your nagios.cfg"
echo
chkconfig --add npcd

%preun
service npcd stop
chkconfig --del npcd

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%docdir %{_defaultdocdir}
%{_prefix}
%{_sysconfdir}
%defattr(-,nagios,root)
%{_localstatedir}

%changelog
* Thu Feb 21 2013 Didier Fabert <didier.fabert@gmail.com> 0.6.19-1
- First release
