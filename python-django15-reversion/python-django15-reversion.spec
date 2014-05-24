%global pkgname django-reversion
%global shortver 1.8

Name:           python-django15-reversion
Version:        %{shortver}.0
Release:        1%{?dist}
Summary:        Version control extension for the Django web framework

Group:          Development/Languages
License:        BSD
URL:            https://github.com/etianen/django-reversion
Source0:        https://github.com/downloads/etianen/django-reversion/%{pkgname}-release-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-sphinx
Requires:       python-django15

Provides:       %{pkgname} = %{version}-%{release}
Obsoletes:      %{pkgname} < 1.7.1-1

%description
Reversion is an extension to the Django web framework that provides
comprehensive version control facilities. 

Features:
* Roll back to any point in a model's history - an unlimited undo facility!
* Recover deleted models - never lose data again!
* Admin integration for maximum usability.
* Group related changes into revisions that can be rolled back in a single
  transaction.
* Automatically save a new version whenever your model changes using Django's
  flexible signalling framework.
* Automate your revision management with easy-to-use middleware. 

Reversion can be easily added to your existing Django project with a minimum
of code changes. 


%package apidoc
Group: Documentation
Summary: python-%{pkgname} API docs
Requires: %{name} = %{version}-%{release}

%description apidoc
Documentation for the %{name} API

%prep
%setup -q -n %{pkgname}-release-%{shortver}

# remove bundled egg-info
rm -rf django_reversion.egg-info

%build
%{__python} setup.py build
pushd docs
make html
make man
popd


%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
# Language files; not under /usr/share, need to be handled manually
(cd $RPM_BUILD_ROOT && find . -name 'django*.mo') | %{__sed} -e 's|^.||' | %{__sed} -e \
  's:\(.*/locale/\)\([^/_]\+\)\(.*\.mo$\):%lang(\2) \1\2\3:' \
  >> %{name}.lang
  
find $RPM_BUILD_ROOT -name "*.po" | xargs rm -f
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/apidoc
%{__mkdir_p} $RPM_BUILD_ROOT%{_mandir}/man1
%{__cp} docs/_build/man/%{pkgname}.1 $RPM_BUILD_ROOT%{_mandir}/man1
%{__cp} -r docs/_build/html/* $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/apidoc


%files -f %{name}.lang
%doc LICENSE CHANGELOG.rst README.rst
%dir %{python_sitelib}/reversion
%{python_sitelib}/reversion/*.py*
%{python_sitelib}/reversion/management/
%{python_sitelib}/reversion/templates/
%{python_sitelib}/reversion/migrations/
%{python_sitelib}/django_reversion-%{version}-py?.?.egg-info
%{_mandir}/man1/%{pkgname}*

%files apidoc
%{_datadir}/%{name}-%{version}/apidoc

%changelog
* Sat May 24 2014 Didier Fabert <didier.fabert@gmail.com> 1.8.0-1
- update to 1.8.0

* Tue Aug 13 2013 Matthias Runge <mrunge@redhat.com> - 1.7.1-1
- update to 1.7.1 (rhbz#979597)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 06 2013 Matthias Runge <mrunge@redhat.com> - 1.7-1
- update to upstream version 1.7

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 13 2012 Matthias Runge <mrunge@redhat.com> - 1-6.5-1
- update to upstream version 1.6.5 (rhbz#886552)

* Wed Oct 31 2012 Matthias Runge <mrunge@redhat.com> - 1.6.4-1
- update to upstream version 1.6.4

* Mon Aug 06 2012 Matthias Runge <mrunge@matthias-runge.de> - 1.6.2-1
- updated to upstream release 1.6.2
- package renamed to python-django-reversion

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 10 2012 Luca Botti <lucabotti@fedoraproject.orf> 1.6.0-1
- Updated to 1.6.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Nov 14 2010 Luca Botti <lucabotti@fedoraproject.org> 1.3.2-2
- Fixed locale handling

* Fri Nov 12 2010 Luca Botti <lucabotti@fedoraproject.org> 1.3.2-1
- Update to 1.3.2

* Tue Sep 29 2009 Luca Botti <lucabotti@fedoraproject.org> 1.1.2-2
- Fixed Spec File

* Fri Aug 21 2009 Luca Botti <lucabotti@fedoraproject.org> 1.1.2-1
- Update to 1.1.2 upstream release

* Fri Jul 17 2009 Tim Niemueller <timn@fedoraproject.org> 1.1.1
- Initial RPM release
