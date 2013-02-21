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

%build
%configure \
    --libexecdir=%{_libdir}/nagios/plugins \
    --disable-nls
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%{__install} -d -m0755 %{buildroot}%{_libdir}/nagios/plugins
make DESTDIR=%{buildroot} install

%{__install} -m0755 %{SOURCE1} %{buildroot}%{_libdir}/nagios/plugins/
%{__install} -m0755 %{SOURCE2} %{buildroot}%{_libdir}/nagios/plugins/

%files
%defattr(-,root,root,-)
%{_libdir}/nagios/plugins/check_snmp_int
%{_libdir}/nagios/plugins/check_snmp_process
%{_libdir}/nagios/plugins/check_snmp_storage
%{_libdir}/nagios/plugins/check_mem.pl
%{_libdir}/nagios/plugins/check_netint.pl

%changelog
* Thu Feb 21 2013 Didier Fabert <dfabert@b2pweb.com> - 1.0.0-1
- First release
