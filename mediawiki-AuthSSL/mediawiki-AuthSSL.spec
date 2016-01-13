%global wiki_path %{_datadir}/mediawiki
%global wiki_ext_path %{wiki_path}/extensions
%global extname AuthSSL

Name:      mediawiki-%{extname}
Version:   0.1
Release:   1%{?dist}
License:   GPLv2+
Group:     Development/Tools
URL:       http://www.mediawiki.org/
Summary:   %{extname} extension for mediawiki
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:   http://nas.b2pweb.com/reposrc/%{name}/SSLAuthPlugin.php
BuildArch: noarch
Requires:  mediawiki >= 1.25.0

%description
SSL Authentication is an extension that automatically logs users into the wiki
using their SSL certificate. It uses mod_ssl in Apache to fetch the DN from the
client certificate and maps that to a MediaWiki user name. All users are
automatically logged in, and all users are required to use certificates.
These certificates must be vouched for by one of the certification authorities
on file, specified by SSLCACertificateFile option. Wiki user names are taken
from the user's certificate (SSL_CLIENT_S_DN_CN), and if that user name does
not already exist, it is created.

%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{wiki_ext_path}/%{extname}
%{__install} -m 0644 %{SOURCE0} %{buildroot}%{wiki_ext_path}/%{extname}/

# Remove vcs directories
find %{buildroot}%{wiki_path} -type d -name '.git*' -exec rm -rf {} \; || :

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{wiki_ext_path}/%{extname}

%changelog
* Tue Jan 12 2016 Didier Fabert <didier.fabert@gmail.com> - 
- Initial build.

