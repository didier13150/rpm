Name:           chive
Version:        1.3.1
Release:        1%{?dist}
Summary:        Web based MySQL Data Management tool
License:        GPLv3+
Group:          Applications/Internet
URL:            http://www.chive-project.com/
Source0:        https://launchpad.net/%{name}/1.1/%{version}/+download/%{name}_%{version}.tar.gz
Source1:        chive.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}
BuildArch:      noarch

%description
Chive is a modern Open-Source MySQL Data Management tool. With it's fast and
elaborate user interface it is getting very popular especially by web
engineers.
Chive was created because of an disaffection with existing tools. They usually
were hard to handle and very time-consuming while the daily use of an web
engineer. 


%prep
%setup -qn %{name}
find . -name '.gitignore' -delete
find . -name '.htaccess' -delete


%build

%clean
rm -rf %{buildroot}

%install
rm -rf %{buildroot}
%{__mkdir} -p %{buildroot}%{_datadir}/%{name}
%{__mkdir} -p %{buildroot}%{_localstatedir}/lib/%{name}
%{__mkdir} -p %{buildroot}%{_sysconfdir}/httpd/conf.d/
%{__cp} %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/chive.conf
for dir in css images js protected themes yii
do
    %{__cp} -r $dir %{buildroot}/%{_datadir}/%{name}
done
%{__cp} index.php %{buildroot}/%{_datadir}/%{name}
%{__mv} %{buildroot}/%{_datadir}/%{name}/protected/runtime %{buildroot}%{_localstatedir}/lib/%{name}/

%{__cp} -r assets %{buildroot}%{_localstatedir}/lib/%{name}/
ln -s %{_localstatedir}/lib/%{name}/runtime %{buildroot}/%{_datadir}/%{name}/protected/runtime
ln -s %{_localstatedir}/lib/%{name}/assets %{buildroot}/%{_datadir}/%{name}/assets


%files
%defattr(-,root,root,-)
%doc README.md
%config(noreplace) %{_sysconfdir}/httpd/conf.d/chive.conf
%{_datadir}/%{name}
%dir %attr(755,apache,root) %{_localstatedir}/lib/%{name}
%attr(755,apache,root) %{_localstatedir}/lib/%{name}/*

%changelog
* Mon Mar 24 2014 Didier Fabert <didier.fabert@gmail.com> - 1.3.1-1
- initial package
