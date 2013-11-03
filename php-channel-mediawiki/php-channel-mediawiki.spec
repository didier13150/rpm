%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}

Summary:           Adds the mediawiki channel from googlecode to PEAR
Name:              php-channel-mediawiki
# Use REST version
Version:           1.0
Release:           1%{?dist}
License:           Public Domain
Group:             Development/Languages
URL:               http://mediawiki.googlecode.com/svn
Source:            http://mediawiki.googlecode.com/svn/channel.xml
Requires:          php-pear(PEAR)
Requires(post):    %{__pear}
Requires(postun):  %{__pear}
Provides:          php-channel(mediawiki.googlecode.com/svn)
BuildRequires:     php-pear >= 1:1.4.9-1.2
BuildArch:         noarch
BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This package adds the mediawiki channel which allows PEAR packages
from this channel to be installed.

%prep
%setup -q -c -T

%build

%install
rm -rf $RPM_BUILD_ROOT
install -D -p -m 644 %{SOURCE0} $RPM_BUILD_ROOT%{pear_xmldir}/%{name}.xml

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ $1 -eq 1 ]; then
  %{__pear} channel-add %{pear_xmldir}/%{name}.xml > /dev/null || :
else
  %{__pear} channel-update %{pear_xmldir}/%{name}.xml > /dev/null ||:
fi

%postun
if [ $1 -eq 0 ]; then
  %{__pear} channel-delete mediawiki.googlecode.com/svn > /dev/null || :
fi

%files
%defattr(-,root,root,-)
%{pear_xmldir}/%{name}.xml

%changelog
* Thu Jul 25 2013 Didier Fabert <didier.fabert@gmail.com> - 1.0-1
- Initial spec file
