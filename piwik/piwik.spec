%global datadir %{_localstatedir}/www/piwik
Name:           piwik
Version:        2.15.0
Release:        1%{?dist}
Summary:        Web Analytics
License:        GPLv3
Group:          Applications/Internet
URL:            http://piwik.org
Source0:        http://builds.piwik.org/%{name}-%{version}.tar.gz
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
%{__cp} -r config %{buildroot}%{datadir}
%{__cp} -r core %{buildroot}%{datadir}
%{__cp} -r js %{buildroot}%{datadir}
%{__cp} -r lang %{buildroot}%{datadir}
%{__cp} -r libs %{buildroot}%{datadir}
%{__cp} -r misc %{buildroot}%{datadir}
%{__cp} -r plugins %{buildroot}%{datadir}
%{__cp} -r tests %{buildroot}%{datadir}
%{__cp} -r tmp %{buildroot}%{datadir}
%{__cp} -r vendor %{buildroot}%{datadir}
%{__install} bower.json %{buildroot}%{datadir}
%{__install} composer.json %{buildroot}%{datadir}
%{__install} composer.lock %{buildroot}%{datadir}
%{__install} console %{buildroot}%{datadir}
%{__install} index.php %{buildroot}%{datadir}
%{__install} piwik.js %{buildroot}%{datadir}
%{__install} piwik.php %{buildroot}%{datadir}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_localstatedir}/www/%{name}
%attr(-,apache,apache,-) %{_localstatedir}/www/%{name}/tmp
%attr(-,apache,apache,-) %{_localstatedir}/www/%{name}/config
%doc CHANGELOG.md CONTRIBUTING.md PRIVACY.md README.md SECURITY.md LEGALNOTICE

%changelog
* Fri Dec 18 2015 Didier Fabert <didier.fabert@gmail.com> 2.15.0-1
- First Release

