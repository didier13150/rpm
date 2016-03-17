Name:           firewalld-add-services
Version:        1.0.0
Release:        1%{?dist}
Summary:        More services definition for firewalld
License:        GPLv3+
Group:          Applications/Internet
URL:            http://www.chive-project.com/
Source0:        %{name}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}
BuildArch:      noarch

%description
Additional services definition for firewalld


%prep
%setup -qc


%build

%clean
rm -rf %{buildroot}

%install
rm -rf %{buildroot}
%{__mkdir} -p %{buildroot}%{_prefix}/lib/firewalld/services
%{__cp} *.xml %{buildroot}%{_prefix}/lib/firewalld/services/


%files
%defattr(-,root,root,-)
%doc README.md
%{_prefix}/lib/firewalld/services/*.xml

%changelog
* Thu Mar 17 2016 Didier Fabert <didier.fabert@gmail.com> - 1.0.0-1
- initial package
