%global wiki_path %{_datadir}/mediawiki
%global wiki_ext_path %{wiki_path}/extensions
%global extname CalcBitrate

Name:      mediawiki-%{extname}
Version:   0.1
Release:   1%{?dist}
License:   GPLv2+
Group:     Development/Tools
URL:       http://www.mediawiki.org/
Summary:   %{extname} extension for mediawiki
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:   http://nas.b2pweb.com/reposrc/%{name}/CalcBitrate.js
Source1:   http://nas.b2pweb.com/reposrc/%{name}/CalcBitrate.php
BuildArch: noarch
Requires:  mediawiki >= 1.25.0

%description
CalcBitrate extension provides a bitrate calculator with the simple tag
"<calcBitrate/>"

%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{wiki_ext_path}/%{extname}
%{__install} -m 0644 %{SOURCE0} %{buildroot}%{wiki_ext_path}/%{extname}/
%{__install} -m 0644 %{SOURCE1} %{buildroot}%{wiki_ext_path}/%{extname}/

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

