%global pkgname dj_database_url

Name:           python-django15-database-url
Version:        0.3.0
Release:        1%{?dist}
Summary:        Use Database URLs in your Django Application

Group:          Development/Languages
License:        BSD
URL:            https://github.com/etianen/django-reversion
Source0:        https://pypi.python.org/packages/source/d/dj-database-url/dj-database-url-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Requires:       python-django15

Provides:       %{pkgname} = %{version}-%{release}
Obsoletes:      %{pkgname} < 0.3.0-1

%description
This simple Django utility allows you to utilize the 12factor inspired
DATABASE_URL environment variable to configure your Django application.


%prep
%setup -q -n dj-database-url-%{version}

# remove bundled egg-info
rm -rf %{pkgname}.egg-info

%build
%{__python} setup.py build


%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT


%files
%doc PKG-INFO README.rst
%{python_sitelib}/%{pkgname}.py*
%{python_sitelib}/%{pkgname}-%{version}-py?.?.egg-info

%changelog
* Mon May 26 2014 Didier Fabert <didier.fabert@gmail.com> 0.3.0-1
- Initial RPM release
