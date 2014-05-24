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
BuildRequires:  python-django15
#BuildRequires:  python-django-reversion
#BuildRequires:  python-django-south
BuildRequires:  python-pip
BuildRequires:  python-sieve
BuildRequires:  python-argcomplete
BuildRequires:  python-passlib
BuildRequires:  python-chardet
BuildRequires:  python-crypto
BuildRequires:  pycryptopp
BuildRequires:  python-lxml
Requires:       python-django15
#Requires:       python-django-reversion
#Requires:       python-django-south
Requires:       python-sieve
Requires:       python-argcomplete
Requires:       python-passlib
Requires:       python-chardet
Requires:       pycryptopp
Requires:       python-lxml
Requires:       python-crypto
BuildRequires:  tree

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
pip install --install-option="--prefix=%{buildroot}" modoboa
tree %{buildroot}

%files
%{_bindir}/%{name}-admin.py
%{python_sitelib}/%{name}
%{python_sitelib}/%{name}-*.egg-info

%changelog
* Fri May 23 2014 Didier Fabert <didier.fabert@gmail.com> 1.1.2-1
- Initial package
