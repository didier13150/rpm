%global datadir %{_localstatedir}/www/piwik
Name:           piwik
Version:        2.16.0
Release:        1%{?dist}
Summary:        Web Analytics
License:        GPLv3
Group:          Applications/Internet
URL:            http://piwik.org
Source0:        http://builds.piwik.org/%{name}-%{version}.tar.gz
Source1:        piwik.conf
BuildArch:      noarch
Requires:       webserver

%description
Piwik is the leading open alternative to Google Analytics that gives you full
control over your data. Piwik lets you easily collect data from websites, apps
& the IoT and visualize this data and extract insights. Privacy is built-in.

%prep
%setup -qn %{name}

%build

%install
rm -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{datadir}
%{__mkdir_p} %{buildroot}%{_sysconfdir}/%{name}
%{__mkdir_p} %{buildroot}%{_sysconfdir}/httpd/conf.d
 %{__cp} -r config/* %{buildroot}%{_sysconfdir}/%{name}/
for dir in core js lang libs misc plugins tests tmp vendor
do
     %{__cp} -r $dir %{buildroot}%{datadir}
done
for script in bower.json composer.json composer.lock console index.php piwik.js piwik.php
do
    %{__install} $script %{buildroot}%{datadir}
done
ln -s %{_sysconfdir}/%{name} %{buildroot}%{datadir}/config
%{__install} %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config %{_sysconfdir}/httpd/conf.d/piwik.conf
%attr(0775,apache,apache) %{_localstatedir}/www/%{name}/tmp
%attr(0775,apache,apache) %{_localstatedir}/www/%{name}/config
%{_localstatedir}/www/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*.php
%config(noreplace) %{_sysconfdir}/%{name}/environment/*.php
%doc CHANGELOG.md CONTRIBUTING.md PRIVACY.md README.md SECURITY.md LEGALNOTICE

%changelog
* Wed Mar 23 2016 Didier Fabert <didier.fabert@gmail.com> 2.16.0-1
- Update from upstream

* Fri Dec 18 2015 Didier Fabert <didier.fabert@gmail.com> 2.15.0-1
- First Release

