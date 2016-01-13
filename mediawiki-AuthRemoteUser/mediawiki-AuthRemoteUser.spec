%global wiki_path %{_datadir}/mediawiki
%global wiki_ext_path %{wiki_path}/extensions
%global extname AuthRemoteUser

Name:      mediawiki-%{extname}
Version:   0.1
Release:   1%{?dist}
License:   GPLv2+
Group:     Development/Tools
URL:       http://www.mediawiki.org/
Summary:   %{extname} extension for mediawiki
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:   https://gerrit.wikimedia.org/r/p/mediawiki/extensions/Auth_remoteuser.tgz
BuildArch: noarch
Requires:  mediawiki >= 1.25.0

%description
This extension allows integration with the web server's built-in authentication 
system via the REMOTE_USER environment variable, which is set through HTTP-Auth,
LDAP, CAS, PAM, and other authentication systems. The extension automatically 
logs-in users using the value of the REMOTE_USER environment variable as the 
MediaWiki username. If an account of that name does not already exist, one is 
created.

%prep
%setup -qn Auth_remoteuser

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{wiki_ext_path}/%{extname}
cp -r * %{buildroot}%{wiki_ext_path}/%{extname}/

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

