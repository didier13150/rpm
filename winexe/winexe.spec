Summary: Remote Windows-command executor
Name:    winexe
Version: 1.1
Release: 8%{?dist}
License: GPLv3
Group:   Applications/Productivity
Url:     http://winexe.sourceforge.net/
Source:  %{name}-%{version}.tar.gz
Patch0:  samba-libs-suffixed.patch

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
%if 0%{?fedora} >= 24
BuildRequires: samba43-devel <= 2:4.4.0
%else
BuildRequires: samba-devel
%endif

BuildRoot: %{_tmppath}/%{name}-%{version}-build

%description
Winexe remotely executes commands on Windows systems.

%prep
%setup -qn %{name}
%patch0 -p1

%build
cd source
%if 0%{?fedora} >= 24
./waf --samba-inc-dirs=%{_includedir}/samba43-4.0 --samba-lib-dirs=%{_libdir}/samba43 configure build
%else
./waf --samba-lib-dirs=%{_libdir}/samba configure build
%endif

%install
rm -rf %{buildroot}
%{__install} -d %{buildroot}%{_bindir}
%{__install} source/build/winexe %{buildroot}%{_bindir}
%{__install} -d %{buildroot}%{_mandir}/man1
%{__install} -m 644 source/%{name}.1 %{buildroot}%{_mandir}/man1

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%attr(755,root,root) /usr/bin/winexe
%doc COPYING NEWS README
%{_mandir}/man1/*

%changelog
* Mon Jul 18 2016 Didier Fabert <didier.fabert@gmail.com> 1.1-8
- Rebuild against samba 2:4.3.11-1

* Wed Jun 22 2016 Didier Fabert <didier.fabert@gmail.com> 1.1-7
- Rebuild against samba 2:4.3.10-0

* Tue May 17 2016 Didier Fabert <didier.fabert@gmail.com> 1.1-6
- Rebuild against samba 2:4.3.9-0

* Mon Apr 25 2016 Didier Fabert <didier.fabert@gmail.com> 1.1-5
- Rebuild against samba 2:4.3.8-0

* Mon Mar 14 2016 Didier Fabert <didier.fabert@gmail.com> 1.1-4
- Rebuild against samba 2:4.3.6-0

* Wed Feb 17 2016 Didier Fabert <didier.fabert@gmail.com> 1.1-3
- Rebuild against samba 2:4.3.4-1

* Mon Jan 11 2016 Didier Fabert <didier.fabert@gmail.com> 1.1-2
- Rebuild against samba 2:4.3.3-0
- Tag release with samba major version

* Tue Nov 10 2015 Didier Fabert <didier.fabert@gmail.com> 1.1-1
- First release
