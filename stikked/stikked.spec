%define githubname Stikked
Name:           stikked
Version:        0.8.6
Release:        1%{?dist}
Summary:        PHP Pastebin
License:        CCO
Group:          Applications/Multimedia
URL:            https://github.com/claudehohl/%{githubname}
Source0:        https://github.com/claudehohl/%{githubname}/archive/%{version}.tar.gz
Source1:        stikked.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       webserver
BuildArch:      noarch

%description
Stikked is an Open-Source PHP Pastebin, with the aim of keeping a simple and
easy to use user interface.
Stikked allows you to easily share code with anyone you wish. Based on the 
original Stikked with lots of bugfixes and improvements.

%prep
%setup -qn %{githubname}-%{version}

%build
%{__cp} htdocs/application/config/stikked.php.dist stikked.php
%{__cp} %{SOURCE1} stikked.conf
%{__sed} -i -e 's#@datadir@#%{_datadir}#g' stikked.conf
%{__sed} -i \
    -e '/db_hostname/ s#127.0.0.1#localhost#g' \
    -e '/theme/ s#default#bootstrap#' \
    stikked.php

%install
%{__mkdir_p} %{buildroot}%{_datadir}/%{name}
%{__mkdir_p} %{buildroot}%{_sysconfdir}/%{name}
%{__mkdir_p} %{buildroot}%{_sysconfdir}/httpd/conf.d
%{__cp} stikked.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/
%{__cp} -r htdocs/* %{buildroot}%{_datadir}/%{name}
ln -s %{_sysconfdir}/%{name}/stikked.php %{buildroot}%{_datadir}/%{name}/application/config/
%{__cp} stikked.php %{buildroot}%{_sysconfdir}/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS.md README.md doc
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/stikked.php

%changelog
* Sat Mar 22 2014 Didier Fabert <didier.fabert@gmail.com> 0.8.6
- First Release
