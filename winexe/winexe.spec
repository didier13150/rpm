# norootforbuild

Summary: Remote Windows-command executor
Name: winexe
Version: 1.1
Release: 1%{?dist}
License: GPL3
Group: Administration/Network
Source: %{name}-%{version}.tar.gz
Patch0: samba-libs-suffixed.patch
BuildRequires: automake
BuildRequires: gcc
BuildRequires: mingw-binutils-generic
BuildRequires: mingw-filesystem-base
BuildRequires: mingw32-binutils
BuildRequires: mingw32-cpp
BuildRequires: mingw32-crt
BuildRequires: mingw32-filesystem
BuildRequires: mingw32-gcc
BuildRequires: mingw32-headers
BuildRequires: mingw64-binutils
BuildRequires: mingw64-cpp
BuildRequires: mingw64-crt
BuildRequires: mingw64-filesystem
BuildRequires: mingw64-gcc
BuildRequires: mingw64-headers
BuildRequires: libcom_err-devel
BuildRequires: popt-devel
BuildRequires: zlib-devel
BuildRequires: zlib-static
BuildRequires: glibc-devel
BuildRequires: glibc-static
BuildRequires: python-devel
BuildRequires: samba-devel

BuildRoot: %{_tmppath}/%{name}-%{version}-build

%description
Winexe remotely executes commands on Windows systems.

%prep
%setup -qn %{name}
%patch0 -p1

%build
cd source
./waf --samba-lib-dirs=%{_libdir}/samba configure build

%install
rm -rf %{buildroot}
%{__install} -d %{buildroot}%{_bindir}
%{__install} source/build/winexe %{buildroot}%{_bindir}
%{__install} -d %{buildroot}%{_mandir}/man1
%{__install} source/%{name}.1 %{buildroot}%{_mandir}/man1

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%attr(755,root,root) /usr/bin/winexe
%doc COPYING NEWS README
%{_mandir}/man1/*

%changelog
* Tue Nov 10 2015 didier Fabert <didier.fabert@gmail.com> 1.1-1
- First release