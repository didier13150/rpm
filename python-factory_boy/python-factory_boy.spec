%bcond_without  python3
%global pkgname factory_boy

Name:           python-%{pkgname}
Version:        2.3.1
Release:        1%{?dist}
Summary:        A verstile test fixtures replacement based on thoughtbot's factory_girl for Ruby.

Group:          Development/Languages
License:        ASL 2.0
URL:            https://pypi.python.org
Source:         https://pypi.python.org/packages/source/f/%{pkgname}/%{pkgname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python2-devel 
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

Provides: %{pkgname} = %{version}-%{release}
Provides: factory-boy = %{version}-%{release}

%description
factory_boy is a fixtures replacement based on thoughtbot's `factory_girl <http://github.com/thoughtbot/factory_girl>`_.

Its features include:

- Straightforward syntax
- Support for multiple build strategies (saved/unsaved instances, attribute
  dicts, stubbed objects)
- Powerful helpers for common cases (sequences, sub-factories, reverse
  dependencies, circular factories, ...)
- Multiple factories per class support, including inheritance
- Support for various ORMs (currently Django, Mogo, SQLAlchemy)

%if 0%{?with_python3}
%package -n python3-%{pkgname}
Summary:        Intelligent schema migrations for Django apps
Group:          Development/Languages

%description -n python3-%{pkgname}
factory_boy is a fixtures replacement based on thoughtbot's `factory_girl <http://github.com/thoughtbot/factory_girl>`_.

Its features include:

- Straightforward syntax
- Support for multiple build strategies (saved/unsaved instances, attribute
  dicts, stubbed objects)
- Powerful helpers for common cases (sequences, sub-factories, reverse
  dependencies, circular factories, ...)
- Multiple factories per class support, including inheritance
- Support for various ORMs (currently Django, Mogo, SQLAlchemy)

%endif

%package apidoc
Group: Documentation
Summary: python-%{pkgname} API docs
Requires: %{name} = %{version}-%{release}

%description apidoc
Documentation for the %{name} API

%prep
%setup -qn %{pkgname}-%{version}
# remove bundled egg-info
rm -rf %{pkgname}.egg-info

%if 0%{?with_python3}
cp -a . %{py3dir}
%endif

%build
%{__python} setup.py build
pushd docs
make html
make man
popd

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/apidoc
%{__mkdir_p} $RPM_BUILD_ROOT%{_mandir}/man1
%{__cp} docs/_build/man/factoryboy.1 $RPM_BUILD_ROOT%{_mandir}/man1/factory_boy.1
%{__cp} -r docs/_build/html/* $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/apidoc

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd
%endif

%files
%doc README.rst PKG-INFO
%{_mandir}/man1/%{pkgname}*
%{python_sitelib}/factory
%{python_sitelib}/%{pkgname}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{pkgname}
%{_mandir}/man1/%{pkgname}*
%doc README.rst PKG-INFO
%{python3_sitelib}/factory
%{python3_sitelib}/%{pkgname}-%{version}-py?.?.egg-info
%endif

%files apidoc
%{_datadir}/%{name}-%{version}/apidoc

%changelog
* Sat May 24 2014 Didier Fabert <didier.fabert@gmail.com> 2.3.1-1
- Initial RPM release
