%global check_postgres_ver      2.20.0
%global check_mysql_health_ver  2.1.8.2
%global nagios_plugins_snmp_ver 0.6.0
%global nagios_snmp_plugins_ver 1.1.1


Name:           shinken-plugins
Version:        1.0.0
Release:        3%{?dist}
Summary:        Plugins needed by default shinken install
License:        GPLv2+

Group:          Applications/Productivity
URL:            http://www.shinken-monitoring.org
Source0:        http://sourceforge.net/projects/nagios-snmp/files/nagios-plugins-snmp-C/0.6/nagios-plugins-snmp-%{nagios_plugins_snmp_ver}.tgz
Source1:        https://raw.github.com/willixix/WL-NagiosPlugins/master/check_netint.pl
Source2:        https://raw.github.com/justintime/nagios-plugins/master/check_mem/check_mem.pl
Source3:        http://nagios.manubulon.com/nagios-snmp-plugins.%{nagios_snmp_plugins_ver}.tgz
Source4:        http://bucardo.org/downloads/check_postgres.tar.gz
Source5:        http://labs.consol.de/download/shinken-nagios-plugins/check_mysql_health-%{check_mysql_health_ver}.tar.gz

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
BuildRequires:  perl-Test-Simple
Obsoletes:      nagios-plugins-shinken

%description
Shinken Plugins needed by default install

%package mysql
Requires:         %{name}
Requires:         perl-DBD-MySQL
Summary:          Shinken MySQL plugin
Group:            Applications/Productivity

%description mysql
Shinken Plugins to monitore a MySQL database

%package postgresql
Requires:         %{name}
Requires:         perl-DBD-Pg
Summary:          Shinken PostgreSQL plugin
Group:            Applications/Productivity

%description postgresql
Shinken Plugins to monitore a PostgreSQL database

%prep
%setup -qn nagios-plugins-snmp
tar -xzf %{SOURCE3}
tar -xzf %{SOURCE4}
tar -xzf %{SOURCE5}

%build
%configure \
    --libexecdir=%{_libdir}/nagios/plugins \
    --disable-nls
make %{?_smp_mflags}
find . -name '*.pl' -exec sed -i -e 's#/usr/local/nagios/libexec#/usr/lib64/nagios/plugins#g' {} \;

pushd check_postgres-%{check_postgres_ver}
perl Makefile.PL
make %{?_smp_mflags}
popd

pushd check_mysql_health-%{check_mysql_health_ver}
%configure \
  --with-nagios-user=shinken \
  --with-nagios-group=shinken \
  --with-statefiles-dir=/var/tmp/check_mysql_health \
  --with-mymodules-dir=%{libdir}/nagios/plugins \
  --with-mymodules-dyn-dir=%{libdir}/nagios/plugins
make %{?_smp_mflags}
popd

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

pushd nagios_plugins
%{__install} -m0755 check_snmp_boostedge.pl %{buildroot}%{_libdir}/nagios/plugins/
%{__install} -m0755 check_snmp_cpfw.pl %{buildroot}%{_libdir}/nagios/plugins/
%{__install} -m0755 check_snmp_css.pl %{buildroot}%{_libdir}/nagios/plugins/
%{__install} -m0755 check_snmp_css_main.pl %{buildroot}%{_libdir}/nagios/plugins/
%{__install} -m0755 check_snmp_env.pl %{buildroot}%{_libdir}/nagios/plugins/
%{__install} -m0755 check_snmp_int.pl %{buildroot}%{_libdir}/nagios/plugins/
%{__install} -m0755 check_snmp_linkproof_nhr.pl %{buildroot}%{_libdir}/nagios/plugins/
%{__install} -m0755 check_snmp_load.pl %{buildroot}%{_libdir}/nagios/plugins/
%{__install} -m0755 check_snmp_mem.pl %{buildroot}%{_libdir}/nagios/plugins/
%{__install} -m0755 check_snmp_nsbox.pl %{buildroot}%{_libdir}/nagios/plugins/
%{__install} -m0755 check_snmp_process.pl %{buildroot}%{_libdir}/nagios/plugins/
%{__install} -m0755 check_snmp_storage.pl %{buildroot}%{_libdir}/nagios/plugins/
%{__install} -m0755 check_snmp_vrrp.pl %{buildroot}%{_libdir}/nagios/plugins/
%{__install} -m0755 check_snmp_win.pl %{buildroot}%{_libdir}/nagios/plugins/
popd

pushd check_postgres-%{check_postgres_ver}
%{__install} -m0755 check_postgres.pl %{buildroot}%{_libdir}/nagios/plugins/
popd

pushd check_mysql_health-%{check_mysql_health_ver}
%{__install} -m0755 plugins-scripts/check_mysql_health %{buildroot}%{_libdir}/nagios/plugins/
popd

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

%files mysql
%defattr(-,root,root,-)
%{_libdir}/nagios/plugins/check_mysql_health

%files postgresql
%defattr(-,root,root,-)
%{_libdir}/nagios/plugins/check_postgres.pl

%changelog
* Tue Apr 02 2013 Didier Fabert <didier.fabert@gmail.com> - 1.0.0-3
- Define global var for all source versions
- Add BuildRequires: perl-Test-Simple

* Thu Feb 28 2013 Didier Fabert <didier.fabert@gmail.com> - 1.0.0-2
- Add MySQL and PostgreSQL plugins (sub-packages)

* Thu Feb 21 2013 Didier Fabert <didier.fabert@gmail.com> - 1.0.0-1
- First release
