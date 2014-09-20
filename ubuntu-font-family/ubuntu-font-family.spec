%global fontdir %{_datadir}/fonts/ubuntu-font-family

Name:       ubuntu-font-family
Version:    0.80
Release:    2%{?dist}
Summary:    The font family used in Ubuntu Linux

Group:      User Interface/X
License:    Ubuntu Font License, based on SIL OFL 1.1
URL:        http://font.ubuntu.com/
Source0:    http://font.ubuntu.com/download/ubuntu-font-family-0.80.zip
BuildArch:  noarch
Requires:   fontconfig

%description
The Ubuntu Font Family are a set of matching new Libre/Open fonts.
The development is being funded by Canonical on behalf the wider Free Software 
community and the Ubuntu project. The technical font design work and 
implementation is being undertaken by Dalton Maag.
For more information visit : http://font.ubuntu.com/about/

%prep
%setup -qn %{name}-%{version}

%build

%install
%{__install} -m 0755 -d %{buildroot}%{fontdir}
%{__install} -m 0644 -p *.ttf %{buildroot}%{fontdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc *.txt
%{fontdir}/Ubuntu-B.ttf
%{fontdir}/Ubuntu-BI.ttf
%{fontdir}/Ubuntu-C.ttf
%{fontdir}/Ubuntu-L.ttf
%{fontdir}/Ubuntu-LI.ttf
%{fontdir}/Ubuntu-M.ttf
%{fontdir}/Ubuntu-MI.ttf
%{fontdir}/Ubuntu-R.ttf
%{fontdir}/Ubuntu-RI.ttf
%{fontdir}/UbuntuMono-B.ttf
%{fontdir}/UbuntuMono-BI.ttf
%{fontdir}/UbuntuMono-R.ttf
%{fontdir}/UbuntuMono-RI.ttf   

%post
# Update font cache
/usr/bin/fc-cache

%postun
# Update font cache
/usr/bin/fc-cache

%changelog
* Sat Sep 20 2014 - Didier Fabert <didier.fabert@gmail.com> - 0.80-2
- Simplify spec.

* Thu May 09 2013 - Prasad K <prasadk@gmx.com> - 0.80-1
- Initial package.
