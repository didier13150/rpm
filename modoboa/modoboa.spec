Name:           modoboa
Version:        1.1.2
Release:        1%{?dist}
Summary:        Mail hosting and management platform
Group:          Applications/Communications
License:        GPLv2+
URL:            http://modoboa.org
Source0:        https://github.com/tonioo/%{name}/archive/%{version}.tar.gz
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Requires:       python-django15
Requires:       python-django15-reversion
Requires:       python-django15-south
Requires:       python-django15-database-url
Requires:       python-factory_boy
Requires:       python-rfc6266
Requires:       python-sievelib
Requires:       python-passlib
Requires:       python-chardet
Requires:       python-crypto
Requires:       python-lxml
Requires:       python-LEPL
Requires:       rrdtool-python
Requires:       MySQL-python

%description
Modoboa is a mail hosting and management platform including a modern and
simplified Web User Interface. It provides useful components such as an
administration panel or a webmail.

Modoboa integrates with well known software such as Postfix or Dovecot.
A SQL database (MySQL, PostgreSQL or SQLite) is used as a central point of
communication between all components.
Modoboa is developed with modularity in mind, expanding it is really easy.

%prep
%setup -qn %{name}-%{version}

%build
%{__python} setup.py build

%install
%{__python} setup.py install --skip-build --root %{buildroot}

%post
ln -s %{python_sitelib}/Django-1.5.6-py2.7.egg/django \
    %{python_sitelib}/django

%files
%{_bindir}/%{name}-admin.py
%{python_sitelib}/%{name}
%{python_sitelib}/%{name}-*.egg-info

%changelog
* Fri May 23 2014 Didier Fabert <didier.fabert@gmail.com> 1.1.2-1
- Initial package
