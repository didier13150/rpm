%bcond_without  python3
%global pkgname TermRecord

Name:           python-%{pkgname}
Version:        1.1.3
Release:        1%{?dist}
Summary:        Terminal session recorder that outputs self-contained HTML

Group:          Development/Languages
License:        MIT
URL:            https://github.com/theonewolf
Source:         https://github.com/theonewolf/%{pkgname}/archive/v%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel 
BuildRequires:  python-setuptools
Requires:       python-jinja2
Requires:       python-argparse
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3-jinja2
Requires:       python3-argparse
%endif

Provides: %{pkgname} = %{version}-%{release}

%description
TermRecord is a simple terminal session recorder with easy-to-share
self-contained HTML output

%if 0%{?with_python3}
%package -n python3-%{pkgname}
Summary:        Terminal session recorder that outputs self-contained HTML
Group:          Development/Languages

%description -n python3-%{pkgname}
TermRecord is a simple terminal session recorder with easy-to-share
self-contained HTML output
%endif

%prep
%setup -qn %{pkgname}-%{version}
sed -i -e '/DEFAULT_TEMPLATE/ s#/usr/local#/usr#' src/TermRecord
sed -i -e '/data_files/ s#/usr/local#/usr#' setup.py
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
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd
%endif

%files
%doc README.md
%{_bindir}/%{pkgname}
%{python_sitelib}/%{pkgname}-%{version}-py?.?.egg-info
%{_datadir}/%{pkgname}

%if 0%{?with_python3}
%files -n python3-%{pkgname}
%doc README.md
%{_bindir}/%{pkgname}
%{python3_sitelib}/%{pkgname}-%{version}-py?.?.egg-info
%{_datadir}/%{pkgname}
%endif

%changelog
* Fri Sep 19 2014 Didier Fabert <didier.fabert@gmail.com> 1.1.3-1
- Initial RPM release
