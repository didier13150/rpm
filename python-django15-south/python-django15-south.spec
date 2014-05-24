%bcond_without  python3

Name:           python-django15-south
Version:        0.8.4
Release:        1%{?dist}
Summary:        Intelligent schema migrations for Django apps

Group:          Development/Languages
License:        ASL 2.0
URL:            http://south.aeracode.org
Source:         http://www.aeracode.org/releases/south/south-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel 
BuildRequires:  python-setuptools
Requires:       python-django15
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

# last built as Django-south-0:0.8.4-1.fc20.noarch
Provides: Django-south = %{version}-%{release} 
Obsoletes: Django-south < 0:0.8.4-1

%description
South brings migrations to Django applications. Its main objectives are to
provide a simple, stable and database-independent migration layer to prevent
all the hassle schema changes over time bring to your Django applications.

%if 0%{?with_python3}
%package -n python3-django-south
Summary:        Intelligent schema migrations for Django apps
Group:          Development/Languages

Requires:       python3-django

%description -n python3-django-south
South brings migrations to Django applications. Its main objectives are to
provide a simple, stable and database-independent migration layer to prevent
all the hassle schema changes over time bring to your Django applications.
%endif

%prep
%setup -q -n South-%{version}
# remove bundled egg-info
rm -rf South.egg-info

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
%doc README
%{python_sitelib}/south
%{python_sitelib}/South-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-django-south
%doc README
%{python3_sitelib}/south
%{python3_sitelib}/South-%{version}-py?.?.egg-info
%endif

%changelog
* Thu Jan 16 2014 Luis Bazan <lbazan@fedoraproject.org> - 0.8.4-1
- the version 0.8.3 have bug
- New Upstream version 0.8.4

* Thu Jan 16 2014 Luis Bazan <lbazan@fedoraproject.org> - 0.8.3-1
- New Upstream version
- python3 add subpackage

* Wed Sep 04 2013 Luis Bazan <lbazan@fedoraproject.org> - 0.8.2-2
- Fix BZ #1002074

* Thu Aug 15 2013 Luis Bazan <lbazan@fedoraproject.org> - 0.8.2-1
- New Upstream version

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 16 2013 Luis Bazan <lbazan@fedoraproject.org> - 0.8.1-1
- New Upstream Version

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 05 2012 Domingo Becker <domingobecker@gmail.com> - 0.7.5-3
- Build requires change from python-devel to python2-devel.
- Remove bundled egg-info.

* Tue Jun 05 2012 Domingo Becker <domingobecker@gmail.com> - 0.7.5-2
- Added README as doc in file section.
- More specific files section.

* Sat Jun 02 2012 Domingo Becker <domingobecker@gmail.com> - 0.7.5-1
- New upstream version.
- Remove docs dir in files section.
- Fixed unpacked directory name.
- Removed first line with python_sitelib...

* Tue May 29 2012 Domingo Becker <domingobecker@gmail.com> - 0.7.3-2
- Removed BuildRoot, clean, defattr and rm -rf buildroot.

* Sun May 27 2012 Domingo Becker <domingobecker@gmail.com> - 0.7.3-1
- Package rename to python-django-south. Please read
  https://fedoraproject.org/wiki/User:Bkabrda/Django_rename

* Mon Dec 20 2010 Domingo Becker <domingobecker@gmail.com> - 0.7.3-1
- New upstream version.

* Thu Nov 05 2010 Diego Búrigo Zacarão <diegobz@gmail.com> 0.7.2-2
- Added patch by beckerde

* Mon Sep 27 2010 Domingo Becker <domingobecker@gmail.com> - 0.7.2-1
- Updated to 0.7.2 Release
- A patch is included for python 2.4 compatibility

* Sat Jul 24 2010 Diego Búrigo Zacarão <diegobz@gmail.com> 0.7.1-2
- Updated to 0.7.1 Release

* Sat Oct 24 2009 Diego Búrigo Zacarão <diegobz@gmail.com> 0.6.1-1
- Updated to 0.6.1 Release

* Wed Aug 13 2009 Diego Búrigo Zacarão <diegobz@gmail.com> 0.6-2
- Updated SPEC to use the upstream tar.gz instead of the VCS checkout

* Sun Aug 11 2009 Diego Búrigo Zacarão <diegobz@gmail.com> 0.6-1
- Updated to 0.6 Release

* Sun Aug 11 2009 Diego Búrigo Zacarão <diegobz@gmail.com> 0.6-0.1.20090811hgrc1
- Initial RPM release
