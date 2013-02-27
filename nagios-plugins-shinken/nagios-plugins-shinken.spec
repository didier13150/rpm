Name:           nagios-plugins-shinken
Version:        1.0.0
Release:        1%{?dist}
Summary:        Nagios Plugins needed by default shinken install
License:        GPLv2+

Group:          Applications/Productivity
URL:            http://www.shinken-monitoring.org
Source0:        http://sourceforge.net/projects/nagios-snmp/files/nagios-plugins-snmp-C/0.6/nagios-plugins-snmp-0.6.0.tgz
Source1:        https://raw.github.com/willixix/WL-NagiosPlugins/master/check_netint.pl
Source2:        https://raw.github.com/justintime/nagios-plugins/master/check_mem/check_mem.pl
Source3:        http://nagios.manubulon.com/nagios-snmp-plugins.1.1.1.tgz
Source4:        http://bucardo.org/downloads/check_postgres.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}


Requires:       nagios-plugins-all
Requires:       perl
Requires:       grep
Requires:       bash
Requires:       sed
Requires:       sh-utils
Requires:       sudo
Requires:       sysstat
Requires:       vnstat
Requires:       ethtool
Requires:       perl-Nagios-Plugin
Requires:       httping
Requires:       net-snmp
BuildRequires:  sed
BuildRequires:  net-snmp-devel

%description
Nagios Plugins needed by default shinken install

%prep
%setup -qn nagios-plugins-snmp
%{__tar} -xzf %{SOURCE3}
%{__tar} -xzf %{SOURCE4}

%build
%configure \
    --libexecdir=%{_libdir}/nagios/plugins \
    --disable-nls
make %{?_smp_mflags}
find . -name '*.pl' -exec sed -i -e 's#/usr/local/nagios/libexec#/usr/lib64/nagios/plugins#g' {} \;

%install
rm -rf $RPM_BUILD_ROOT
%{__install} -d -m0755 %{buildroot}%{_libdir}/nagios/plugins
make DESTDIR=%{buildroot} install

# Workaround for check perl modules requires
%{__sed} -i \
    -e 's/use snmp v2c/-use- snmp v2c/' \
    -e 's/use it as/-use- it as/' \
    %{SOURCE1}

%{__install} -m0755 %{SOURCE1} %{buildroot}%{_libdir}/nagios/plugins/
%{__install} -m0755 %{SOURCE2} %{buildroot}%{_libdir}/nagios/plugins/
%{__install} -m0755 check_postgres*/check_postgres.pl %{buildroot}%{_libdir}/nagios/plugins/
%{__install} -m0755 nagios_plugins/check_snmp_boostedge.pl %{buildroot}%{_libdir}/nagios/plugins/
%{__install} -m0755 nagios_plugins/check_snmp_cpfw.pl %{buildroot}%{_libdir}/nagios/plugins/
%{__install} -m0755 nagios_plugins/check_snmp_css.pl %{buildroot}%{_libdir}/nagios/plugins/
%{__install} -m0755 nagios_plugins/check_snmp_css_main.pl %{buildroot}%{_libdir}/nagios/plugins/
%{__install} -m0755 nagios_plugins/check_snmp_env.pl %{buildroot}%{_libdir}/nagios/plugins/
%{__install} -m0755 nagios_plugins/check_snmp_int.pl %{buildroot}%{_libdir}/nagios/plugins/
%{__install} -m0755 nagios_plugins/check_snmp_linkproof_nhr.pl %{buildroot}%{_libdir}/nagios/plugins/
%{__install} -m0755 nagios_plugins/check_snmp_load.pl %{buildroot}%{_libdir}/nagios/plugins/
%{__install} -m0755 nagios_plugins/check_snmp_mem.pl %{buildroot}%{_libdir}/nagios/plugins/
%{__install} -m0755 nagios_plugins/check_snmp_nsbox.pl %{buildroot}%{_libdir}/nagios/plugins/
%{__install} -m0755 nagios_plugins/check_snmp_process.pl %{buildroot}%{_libdir}/nagios/plugins/
%{__install} -m0755 nagios_plugins/check_snmp_storage.pl %{buildroot}%{_libdir}/nagios/plugins/
%{__install} -m0755 nagios_plugins/check_snmp_vrrp.pl %{buildroot}%{_libdir}/nagios/plugins/
%{__install} -m0755 nagios_plugins/check_snmp_win.pl %{buildroot}%{_libdir}/nagios/plugins/

%files
%defattr(-,root,root,-)
%{_libdir}/nagios/plugins/check_snmp_int
%{_libdir}/nagios/plugins/check_snmp_process
%{_libdir}/nagios/plugins/check_snmp_storage
%{_libdir}/nagios/plugins/check_mem.pl
%{_libdir}/nagios/plugins/check_netint.pl
%{_libdir}/nagios/plugins/check_snmp_boostedge.pl
%{_libdir}/nagios/plugins/check_snmp_cpfw.pl
%{_libdir}/nagios/plugins/check_snmp_css.pl
%{_libdir}/nagios/plugins/check_snmp_css_main.pl
%{_libdir}/nagios/plugins/check_snmp_env.pl
%{_libdir}/nagios/plugins/check_snmp_int.pl
%{_libdir}/nagios/plugins/check_snmp_linkproof_nhr.pl
%{_libdir}/nagios/plugins/check_snmp_load.pl
%{_libdir}/nagios/plugins/check_snmp_mem.pl
%{_libdir}/nagios/plugins/check_snmp_nsbox.pl
%{_libdir}/nagios/plugins/check_snmp_process.pl
%{_libdir}/nagios/plugins/check_snmp_storage.pl
%{_libdir}/nagios/plugins/check_snmp_vrrp.pl
%{_libdir}/nagios/plugins/check_snmp_win.pl
%{_libdir}/nagios/plugins/check_postgres.pl
%doc AUTHORS COPYING ChangeLog NEWS README nagios_plugins/doc/


%changelog
* Thu Feb 21 2013 Didier Fabert <dfabert@b2pweb.com> - 1.0.0-1
- First release
