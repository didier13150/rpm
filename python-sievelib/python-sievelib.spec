%bcond_without  python3
%global pkgname sievelib

Name:           python-%{pkgname}
Version:        0.8
Release:        1%{?dist}
Summary:        Client-side SIEVE library

Group:          Development/Languages
License:        ASL 2.0
URL:            https://pypi.python.org
Source:         https://pypi.python.org/packages/source/s/%{pkgname}/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel 
BuildRequires:  python-setuptools

Provides: %{pkgname} = %{version}-%{release}

%description
Client-side Sieve and Managesieve library written in Python.
* Sieve : An Email Filtering Language (RFC 5228)
* ManageSieve : A Protocol for Remotely Managing Sieve Scripts (RFC 5804)


%prep
%setup -qn %{pkgname}-%{version}
# remove bundled egg-info
rm -rf %{pkgname}.egg-info


%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT


%files
%doc README.rst PKG-INFO
%{python_sitelib}/%{pkgname}
%{python_sitelib}/%{pkgname}-%{version}-py?.?.egg-info

%changelog
* Sat May 24 2014 Didier Fabert <didier.fabert@gmail.com> 0.0.4-1
- Initial RPM release
