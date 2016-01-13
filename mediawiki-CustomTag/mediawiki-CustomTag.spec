%global wiki_path %{_datadir}/mediawiki
%global wiki_ext_path %{wiki_path}/extensions
%global extname CustomTag

Name:      mediawiki-%{extname}
Version:   0.1
Release:   1%{?dist}
License:   GPLv2+
Group:     Development/Tools
URL:       http://www.mediawiki.org/
Summary:   %{extname} extension for mediawiki
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:   http://nas.b2pweb.com/reposrc/%{name}/Linux.tag.php
BuildArch: noarch
Requires:  mediawiki >= 1.25.0

%description
CustomTag extension support custom tags to modify display:
<path>, <package>, <app>, <class>

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

