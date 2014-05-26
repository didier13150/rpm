%bcond_without  python3
%global pkgname LEPL

Name:           python-%{pkgname}
Version:        5.1.3
Release:        1%{?dist}
Summary:        A Parser Library for Python

Group:          Development/Languages
License:        ASL 2.0
URL:            https://pypi.python.org
Source:         https://pypi.python.org/packages/source/L/%{pkgname}/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel 
BuildRequires:  python-setuptools

Provides: %{pkgname} = %{version}-%{release}

%description
LEPL is a recursive descent parser, written in Python, which has a a friendly,
easy-to-use syntax. The underlying implementation includes several features
that make it more powerful than might be expected.


%prep
%setup -qn %{pkgname}-%{version}
# remove bundled egg-info
rm -rf %{pkgname}.egg-info


%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT


%files
%doc PKG-INFO
%{python_sitelib}/lepl
%{python_sitelib}/%{pkgname}-%{version}-py?.?.egg-info

%changelog
* Sat May 24 2014 Didier Fabert <didier.fabert@gmail.com> 1.2.1-1
- Initial RPM release
