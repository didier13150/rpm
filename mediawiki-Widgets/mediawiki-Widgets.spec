%global wiki_path %{_datadir}/mediawiki
%global wiki_ext_path %{wiki_path}/extensions
%global extname Widgets

Name:      mediawiki-%{extname}
Version:   0.1
Release:   1%{?dist}
License:   GPLv2+
Group:     Development/Tools
URL:       http://www.mediawiki.org/
Summary:   %{extname} extension for mediawiki
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:   https://gerrit.wikimedia.org/r/p/mediawiki/extensions/%{extname}.tgz
BuildArch: noarch
Requires:  mediawiki >= 1.25.0

%description
The Widgets extension allows the creation of raw HTML pages that can be
embedded (similary to templates) in normal wiki pages. You do this by
creating pages in the Widget namespace. They avoid the security problems of
raw HTML in editable wiki pages because the privilege to edit in the Widget
namespace is managed. Many pre-written Widgets are available.

%prep
%setup -qn %{extname}

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{wiki_ext_path}
cp -r ../%{extname} %{buildroot}%{wiki_ext_path}

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

