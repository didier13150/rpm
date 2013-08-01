Summary:        Manage Certificate Authority
Name:           manageCA
Version:        0.7.1
Release:        1%{?dist}
License:        GPLv3+
Group:          Applications/System
URL:            https://github.com/didier13150
Source0:        https://github.com/didier13150/%{name}/archive/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
Requires:       openssl
BuildArch:      noarch

%description
CLI tool to Manage Certificate Authority. It can set up a PKI very easily,
even you don't know a lot about SSL certificate.

%prep
%setup -qn %{name}-%{version}

%build
rm -rf .git*

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_sbindir}
%{__cp} %{name}.sh %{buildroot}%{_sbindir}/%{name}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc README.md
%{_sbindir}/%{name}

%changelog
* Thu Aug 01 2013 Didier Fabert <didier.fabert@gmail.com> 0.7.1-1
- Update

* Tue Jul 30 2013 Didier Fabert <didier.fabert@gmail.com> 0.7-1
- Update

* Mon Jul 29 2013 Didier Fabert <didier.fabert@gmail.com> 0.6-2
- Remove openssl-clients dependency

* Mon Jul 29 2013 Didier Fabert <didier.fabert@gmail.com> 0.6-1
- Update

* Thu Jul 04 2013 Didier Fabert <didier.fabert@gmail.com> 0.5-1
- First Import
