%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Gravatar

Summary:          PEAR Package of Gravatar
Name:             php-pear-mediawiki-gravatar
Version:          1.1.0
Release:          1%{?dist}
License:          BSD
Group:            Development/Languages
URL:              http://pear.php.net/
Source0:          http://mediawiki.googlecode.com/svn/tags/%{pear_name}/%{pear_name}-%{version}.tgz
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:        noarch
BuildRequires:    php-pear(PEAR)
BuildRequires:    php-channel(mediawiki.googlecode.com/svn)
Requires:         php >= 5.2.4
Requires:         php-pear(PEAR) >= 1.3.6
Requires(post):   %{__pear}
Requires(postun): %{__pear}
Provides:         php-pear(%{pear_name}) = %{version}
Requires:         php-channel(mediawiki.googlecode.com/svn)
Requires:         php-pear(mediawiki.googlecode.com/svn/StubManager)

%description
Provides integration with http://site.gravatar.com

%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pear_name}-%{version}/%{pear_name}.xml
cd %{pear_name}-%{version}

%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
rm -rf $RPM_BUILD_ROOT docdir
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{pear_name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*
rm -rf %{buildroot}/%{pear_metadir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{pear_name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%post
%{__pear} install --nodeps --soft --force --register-only \
       %{pear_xmldir}/%{pear_name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
       %{__pear} uninstall --nodeps --ignore-errors --register-only \
       %{pear_name} >/dev/null || :
fi

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{pear_xmldir}/%{pear_name}.xml
%{pear_phpdir}/*

%changelog
* Fri Jul 26 2013 Didier Fabert <didier.fabert@gmail.com> - 1.1.0-1
- First release
