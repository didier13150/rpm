%global check_postgres_ver      2.20.0
%global check_mysql_health_ver  2.1.8.2
%global nagios_plugins_snmp_ver 0.6.0
%global nagios_snmp_plugins_ver 1.1.1
%global nagios_plugins_ver      1.4.16

Name:           shinken-plugins
Version:        1.0.0
Release:        5%{?dist}
Summary:        Plugins needed by default shinken install
License:        GPLv2+

Group:          Applications/Productivity
URL:            http://nagiosplug.sourceforge.net/
Source0:        http://downloads.sourceforge.net/project/nagiosplug/nagiosplug/%{nagios_plugins_ver}/nagios-plugins-%{nagios_plugins_ver}.tar.gz
Source1:        http://sourceforge.net/projects/nagios-snmp/files/nagios-plugins-snmp-C/0.6/nagios-plugins-snmp-%{nagios_plugins_snmp_ver}.tgz
Source2:        https://raw.github.com/willixix/WL-NagiosPlugins/master/check_netint.pl
Source3:        https://raw.github.com/justintime/nagios-plugins/master/check_mem/check_mem.pl
Source4:        http://nagios.manubulon.com/nagios-snmp-plugins.%{nagios_snmp_plugins_ver}.tgz
Source5:        http://bucardo.org/downloads/check_postgres.tar.gz
Source6:        http://labs.consol.de/download/shinken-nagios-plugins/check_mysql_health-%{check_mysql_health_ver}.tar.gz
Patch1:         nagios-plugins-0001-Do-not-use-usr-local-for-perl.patch
Patch2:         nagios-plugins-0002-Remove-assignment-of-not-parsed-to-jitter.patch
Patch3:         nagios-plugins-0003-Fedora-specific-fixes-for-searching-for-diff-and-tai.patch
Patch4:         nagios-plugins-0004-Fedora-specific-patch-for-not-to-fixing-fully-qualif.patch
# https://bugzilla.redhat.com/512559
Patch6:         nagios-plugins-0006-Prevent-check_swap-from-returning-OK-if-no-swap-acti.patch
Patch7:         nagios-plugins-0007-undef-gets-and-glibc-2.16.patch
Patch8:         nagios-plugins-0008-ntpdate-and-ntpq-paths.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

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
BuildRequires:  openldap-devel
BuildRequires:  mysql-devel
BuildRequires:  net-snmp-utils
BuildRequires:  samba-client
BuildRequires:  postgresql-devel
BuildRequires:  gettext
BuildRequires:  %{_bindir}/ssh
BuildRequires:  bind-utils
BuildRequires:  ntp
BuildRequires:  %{_bindir}/mailq
BuildRequires:  %{_sbindir}/fping
BuildRequires:  perl(Net::SNMP)
BuildRequires:  radiusclient-ng-devel
BuildRequires:  qstat
Obsoletes:      nagios-plugins-shinken < 1.0.0-3
Provides:       nagios-plugins = %{nagios_plugins_ver}
Conflicts:      nagios-plugins-breeze
Conflicts:      nagios-plugins-by_ssh
Conflicts:      nagios-plugins-dhcp
Conflicts:      nagios-plugins-dig
Conflicts:      nagios-plugins-disk
Conflicts:      nagios-plugins-disk_smb
Conflicts:      nagios-plugins-dns
Conflicts:      nagios-plugins-dummy
Conflicts:      nagios-plugins-file_age
Conflicts:      nagios-plugins-flexlm
Conflicts:      nagios-plugins-fping
Conflicts:      nagios-plugins-hpjd
Conflicts:      nagios-plugins-http
Conflicts:      nagios-plugins-icmp
Conflicts:      nagios-plugins-ide_smart
Conflicts:      nagios-plugins-ircd
Conflicts:      nagios-plugins-ldap
Conflicts:      nagios-plugins-load
Conflicts:      nagios-plugins-log
Conflicts:      nagios-plugins-mailq
Conflicts:      nagios-plugins-mrtg
Conflicts:      nagios-plugins-mrtgtraf
Conflicts:      nagios-plugins-mysql
Conflicts:      nagios-plugins-nagios
Conflicts:      nagios-plugins-nt
Conflicts:      nagios-plugins-ntp
Conflicts:      nagios-plugins-ntp-perl
Conflicts:      nagios-plugins-nwstat
Conflicts:      nagios-plugins-oracle
Conflicts:      nagios-plugins-overcr
Conflicts:      nagios-plugins-pgsql
Conflicts:      nagios-plugins-ping
Conflicts:      nagios-plugins-procs
Conflicts:      nagios-plugins-game
Conflicts:      nagios-plugins-real
Conflicts:      nagios-plugins-rpc
Conflicts:      nagios-plugins-smtp
Conflicts:      nagios-plugins-snmp
Conflicts:      nagios-plugins-ssh
Conflicts:      nagios-plugins-swap
Conflicts:      nagios-plugins-tcp
Conflicts:      nagios-plugins-time
Conflicts:      nagios-plugins-ups
Conflicts:      nagios-plugins-users
Conflicts:      nagios-plugins-wave
Conflicts:      nagios-plugins-cluster
%ifnarch ppc ppc64 sparc sparc64
Conflicts:      nagios-plugins-sensors
%endif

%description
Shinken Plugins needed by default install. It contains official Nagios plugins.

%package snmp
Summary: Shinken SNMP Plugins
Group: Applications/System
Requires:       %{name} = %{version}-%{release}
Requires:       %{_bindir}/snmpgetnext
Requires:       %{_bindir}/snmpget

%description snmp
Shinken Plugins to monitore host by SNMP

%package mysql
Requires:       %{name} = %{version}-%{release}
Requires:       perl-DBD-MySQL
Summary:        Shinken MySQL plugin
Group:          Applications/Productivity

%description mysql
Shinken Plugins to monitore a MySQL database

%package postgresql
Requires:       %{name} = %{version}-%{release}
Requires:       perl-DBD-Pg
Summary:        Shinken PostgreSQL plugin
Group:          Applications/Productivity

%description postgresql
Shinken Plugins to monitore a PostgreSQL database

%package oracle
Requires:       %{name} = %{version}-%{release}
Summary:        Shinken Oracle plugin
Group:          Applications/Productivity

%description oracle
Shinken Plugins to monitore an Oracle database

%package all
Summary:        Shinken All Plugins
Group:          Applications/System
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-snmp = %{version}-%{release}
Requires:       %{name}-mysql = %{version}-%{release}
Requires:       %{name}-postgresql = %{version}-%{release}
Requires:       %{name}-oracle = %{version}-%{release}
Provides:       nagios-plugins-all = %{nagios_plugins_ver}

%description all
This package provides all Shinken plugins.

%prep
%setup -qn nagios-plugins-%{nagios_plugins_ver}
%patch1 -p1 -b .no_usr_local
%patch2 -p1 -b .not_parsed
%patch3 -p1 -b .proper_paths
%patch4 -p1 -b .no_need_fo_fix_paths
%patch6 -p1 -b .fix_missing_swap
%patch7 -p1 -b .gets
%patch8 -p1 -b .ext_ntp_cmds
tar -xzf %{SOURCE1}
tar -xzf %{SOURCE4}
tar -xzf %{SOURCE5}
tar -xzf %{SOURCE6}

%build
%configure \
    --libexecdir=%{_libdir}/nagios/plugins \
    --with-mysql \
    PATH_TO_QSTAT=%{_bindir}/quakestat \
    PATH_TO_FPING=%{_sbindir}/fping \
    PATH_TO_NTPQ=%{_sbindir}/ntpq \
    PATH_TO_NTPDC=%{_sbindir}/ntpdc \
    PATH_TO_NTPDATE=%{_sbindir}/ntpdate \
    PATH_TO_RPCINFO=%{_sbindir}/rpcinfo \
    --with-ps-command="`which ps` -eo 's uid pid ppid vsz rss pcpu etime comm args'" \
    --with-ps-format='%s %d %d %d %d %d %f %s %s %n' \
    --with-ps-cols=10 \
    --enable-extra-opts \
    --disable-nls \
    --with-ps-varlist='procstat,&procuid,&procpid,&procppid,&procvsz,&procrss,&procpcpu,procetime,procprog,&pos'
make %{?_smp_mflags}

#pushd plugins
#make check_ide_smart
#make check_ldap
#make check_radius
#make check_pgsql
#popd

gawk -f plugins-scripts/subst contrib/check_linux_raid.pl > contrib/check_linux_raid
mv plugins-scripts/check_ntp.pl plugins-scripts/check_ntp.pl.in
gawk -f plugins-scripts/subst plugins-scripts/check_ntp.pl.in > plugins-scripts/check_ntp.pl

pushd nagios-plugins-snmp
%configure \
    --libexecdir=%{_libdir}/nagios/plugins \
    --disable-nls
make %{?_smp_mflags}
find . -name '*.pl' -exec sed -i -e 's#/usr/local/nagios/libexec#/usr/lib64/nagios/plugins#g' {} \;
popd

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

cat << 'EOF' > shinken-plugins-all
This meta package contains all plugins
EOF

%install
sed -i 's,^MKINSTALLDIRS.*,MKINSTALLDIRS = ../mkinstalldirs,' po/Makefile
rm -rf %{buildroot}
%{__install} -d -m0755 %{buildroot}%{_libdir}/nagios/plugins

make AM_INSTALL_PROGRAM_FLAGS="" DESTDIR=%{buildroot} install
install -m 0755 plugins-root/check_icmp %{buildroot}/%{_libdir}/nagios/plugins
install -m 0755 plugins-root/check_dhcp %{buildroot}/%{_libdir}/nagios/plugins
install -m 0755 contrib/check_linux_raid %{buildroot}/%{_libdir}/nagios/plugins
install -m 0755 plugins/check_ide_smart %{buildroot}/%{_libdir}/nagios/plugins
install -m 0755 plugins/check_ldap %{buildroot}/%{_libdir}/nagios/plugins
install -m 0755 plugins-scripts/check_ntp.pl %{buildroot}/%{_libdir}/nagios/plugins
install -m 0755 plugins/check_radius %{buildroot}/%{_libdir}/nagios/plugins
install -m 0755 plugins/check_pgsql %{buildroot}/%{_libdir}/nagios/plugins
%ifarch ppc ppc64 sparc sparc64
rm -f %{buildroot}/%{_libdir}/nagios/plugins/check_sensors
%endif
chmod 644 %{buildroot}/%{_libdir}/nagios/plugins/utils.pm

pushd nagios-plugins-snmp
make DESTDIR=%{buildroot} install
popd

# Workaround for check perl modules requires
%{__sed} -i \
    -e 's/use snmp v2c/-use- snmp v2c/' \
    -e 's/use it as/-use- it as/' \
    %{SOURCE2}

%{__install} -m0755 %{SOURCE2} %{buildroot}%{_libdir}/nagios/plugins/
%{__install} -m0755 %{SOURCE3} %{buildroot}%{_libdir}/nagios/plugins/

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
# Extra Plugins
%{_libdir}/nagios/plugins/check_mem.pl
%{_libdir}/nagios/plugins/check_netint.pl
# Official plugins
%doc ACKNOWLEDGEMENTS AUTHORS BUGS ChangeLog CODING COPYING FAQ LEGAL NEWS README REQUIREMENTS SUPPORT THANKS
%{_libdir}/nagios/plugins/negate
%{_libdir}/nagios/plugins/urlize
%{_libdir}/nagios/plugins/utils.sh
%{_libdir}/nagios/plugins/check_apt
%{_libdir}/nagios/plugins/check_breeze
%{_libdir}/nagios/plugins/check_by_ssh
%{_libdir}/nagios/plugins/check_cluster
%{_libdir}/nagios/plugins/check_dig
%{_libdir}/nagios/plugins/check_disk
%{_libdir}/nagios/plugins/check_disk_smb
%{_libdir}/nagios/plugins/check_dns
%{_libdir}/nagios/plugins/check_dummy
%{_libdir}/nagios/plugins/check_file_age
%{_libdir}/nagios/plugins/check_flexlm
%{_libdir}/nagios/plugins/check_game
%{_libdir}/nagios/plugins/check_hpjd
%{_libdir}/nagios/plugins/check_http
%{_libdir}/nagios/plugins/check_icmp
%{_libdir}/nagios/plugins/check_ifoperstatus
%{_libdir}/nagios/plugins/check_ifstatus
%{_libdir}/nagios/plugins/check_ircd
%{_libdir}/nagios/plugins/check_ldap
%{_libdir}/nagios/plugins/check_ldaps
%{_libdir}/nagios/plugins/check_linux_raid
%{_libdir}/nagios/plugins/check_load
%{_libdir}/nagios/plugins/check_log
%{_libdir}/nagios/plugins/check_mailq
%{_libdir}/nagios/plugins/check_mrtg
%{_libdir}/nagios/plugins/check_mrtgtraf
%{_libdir}/nagios/plugins/check_nagios
%{_libdir}/nagios/plugins/check_nt
%{_libdir}/nagios/plugins/check_ntp
%{_libdir}/nagios/plugins/check_ntp_peer
%{_libdir}/nagios/plugins/check_ntp_time
%{_libdir}/nagios/plugins/check_ntp.pl
%{_libdir}/nagios/plugins/check_nwstat
%{_libdir}/nagios/plugins/check_overcr
%{_libdir}/nagios/plugins/utils.pm
%{_libdir}/nagios/plugins/check_ping
%{_libdir}/nagios/plugins/check_procs
%{_libdir}/nagios/plugins/check_radius
%{_libdir}/nagios/plugins/check_real
%{_libdir}/nagios/plugins/check_rpc
%{_libdir}/nagios/plugins/check_smtp
%{_libdir}/nagios/plugins/check_ssh
%{_libdir}/nagios/plugins/check_swap
%{_libdir}/nagios/plugins/check_clamd
%{_libdir}/nagios/plugins/check_ftp
%{_libdir}/nagios/plugins/check_imap
%{_libdir}/nagios/plugins/check_jabber
%{_libdir}/nagios/plugins/check_nntp
%{_libdir}/nagios/plugins/check_nntps
%{_libdir}/nagios/plugins/check_pop
%{_libdir}/nagios/plugins/check_simap
%{_libdir}/nagios/plugins/check_spop
%{_libdir}/nagios/plugins/check_ssmtp
%{_libdir}/nagios/plugins/check_tcp
%{_libdir}/nagios/plugins/check_udp
%{_libdir}/nagios/plugins/check_time
%{_libdir}/nagios/plugins/check_ups
%{_libdir}/nagios/plugins/check_users
%{_libdir}/nagios/plugins/check_wave
%defattr(4750,root,nagios,-)
%{_libdir}/nagios/plugins/check_dhcp
%{_libdir}/nagios/plugins/check_fping
%{_libdir}/nagios/plugins/check_ide_smart
%ifnarch ppc ppc64 sparc sparc64
%{_libdir}/nagios/plugins/check_sensors
%endif

%files snmp
%defattr(-,root,root,-)
# Official plugins
%{_libdir}/nagios/plugins/check_snmp
# Extra Plugins
%{_libdir}/nagios/plugins/check_snmp_int
%{_libdir}/nagios/plugins/check_snmp_process
%{_libdir}/nagios/plugins/check_snmp_storage
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
%doc AUTHORS COPYING ChangeLog NEWS README nagios_plugins/doc/

%files mysql
%defattr(-,root,root,-)
# Official plugins
%{_libdir}/nagios/plugins/check_mysql
%{_libdir}/nagios/plugins/check_mysql_query
# Extra Plugins
%{_libdir}/nagios/plugins/check_mysql_health

%files postgresql
%defattr(-,root,root,-)
# Official plugins
%{_libdir}/nagios/plugins/check_pgsql
# Extra Plugins
%{_libdir}/nagios/plugins/check_postgres.pl

%files oracle
%defattr(-,root,root,-)
# Official plugins
%{_libdir}/nagios/plugins/check_oracle

%files all
%defattr(-,root,root,-)
%doc shinken-plugins-all

%changelog
* Fri Apr 05 2013 Didier Fabert <didier.fabert@gmail.com> - 1.0.0-5
- Add Missing shinken-plugins-all meta-package

* Wed Apr 03 2013 Didier Fabert <didier.fabert@gmail.com> - 1.0.0-4
- Add nagios plugins

* Tue Apr 02 2013 Didier Fabert <didier.fabert@gmail.com> - 1.0.0-3
- Define global var for all source versions
- Add BuildRequires: perl-Test-Simple

* Thu Feb 28 2013 Didier Fabert <didier.fabert@gmail.com> - 1.0.0-2
- Add MySQL and PostgreSQL plugins (sub-packages)

* Thu Feb 21 2013 Didier Fabert <didier.fabert@gmail.com> - 1.0.0-1
- First release
