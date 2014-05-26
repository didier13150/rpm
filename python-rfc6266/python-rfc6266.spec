%bcond_without  python3
%global pkgname rfc6266

Name:           python-%{pkgname}
Version:        0.0.4
Release:        1%{?dist}
Summary:        Parse and generate Content-Disposition headers

Group:          Development/Languages
License:        ASL 2.0
URL:            https://pypi.python.org
Source:         https://pypi.python.org/packages/source/r/%{pkgname}/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel 
BuildRequires:  python-setuptools
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

Provides: %{pkgname} = %{version}-%{release}

%description
This module parses and generates HTTP Content-Disposition headers. These
headers are used when getting resources for download; they provide a hint
of whether the file should be downloaded, and of what filename to use when
saving.

%if 0%{?with_python3}
%package -n python3-%{pkgname}
Summary:        Intelligent schema migrations for Django apps
Group:          Development/Languages

%description -n python3-%{pkgname}
This module parses and generates HTTP Content-Disposition headers. These
headers are used when getting resources for download; they provide a hint
of whether the file should be downloaded, and of what filename to use when
saving.
%endif

%prep
%setup -qn %{pkgname}-%{version}
# remove bundled egg-info
rm -rf %{pkgname}.egg-info

%if 0%{?with_python3}
cp -a . %{py3dir}
%endif

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd
%endif

%files
%doc README PKG-INFO
%{python_sitelib}/*%{pkgname}.py*
%{python_sitelib}/%{pkgname}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{pkgname}
%doc README PKG-INFO
%{python3_sitelib}/*%{pkgname}.py*
%{python3_sitelib}/__pycache__/*%{pkgname}.cpython-33.py?
%{python3_sitelib}/%{pkgname}-%{version}-py?.?.egg-info
%endif

%changelog
* Sat May 24 2014 Didier Fabert <didier.fabert@gmail.com> 0.0.4-1
- Initial RPM release
