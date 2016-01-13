%global wiki_path %{_datadir}/mediawiki
%global wiki_ext_path %{wiki_path}/extensions
%global extname PdfHandler

Name:      mediawiki-%{extname}
Version:   0.1
Release:   1%{?dist}
License:   GPLv2+
Group:     Development/Tools
URL:       http://www.mediawiki.org/
Summary:   %{extname} extension for mediawiki
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:   https://git.wikimedia.org/git/mediawiki/extensions/%{extname}.tgz
BuildArch: noarch
Requires:  mediawiki >= 1.25.0
Requires:  ghostscript, poppler-utils, php-mbstring

%description
The PdfHandler extension shows uploaded pdf files in a multipage preview layout.
With the Proofread Page extension enabled, pdfs can be displayed side-by-side
with text for transcribing books and other documents, as is commonly done with
DjVu files.

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

