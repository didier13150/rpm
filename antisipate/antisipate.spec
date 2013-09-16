# Copyright (c) 2012 David Sugar, Tycho Softworks.
# This file is free software; as a special exception the author gives
# unlimited permission to copy and/or distribute it, with or without
# modifications, as long as this notice is preserved.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY, to the extent permitted by law; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.

Name: antisipate
Summary: ZRTP enabled secure SIP user agent
Version: 0.0.1
Release: 0%{?dist}
License: GPLv3+
URL: http://www.gnutelephony.org
Group: Applications/Communications
Source: http://dev.gnutelephony.org/dist/tarballs/antisipate-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: qt4-devel >= 4.8.0
BuildRequires: cmake >= 2.6.0
BuildRequires: coastal-qt-devel >= 0.4.1
BuildRequires: libzrtpcpp-devel >= 2.3.4
BuildRequires: libeXosip2-devel >= 3.4.0
BuildRequires: ucommon-devel >= 6.0.0
BuildRequires: libccrtp-devel >= 2.0.0
Requires:      libeXosip2
Requires:      ucommon
Requires:      coastal-qt

%package qt
Summary: ZRTP Enabled QT SIP user agent

%package cli
Summary: Stand-alone sip utilities

%description
Qt based cross-platform secure SIP user agent that offers ZRTP support.

%description qt
Qt based cross-platform secure SIP user agent that offers ZRTP support.

%description cli
Stand-alone command line sip utilities built from antisipate package.  These
have no Qt dependencies.

%prep
%setup -q

%build
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} \
      -DSYSCONFDIR=%{_sysconfdir} \
      -DMANDIR=%{_mandir} \
      -DDATADIR=%{_datadir} \
      -DCMAKE_VERBOSE_MAKEFILE=TRUE \
      -DCMAKE_C_FLAGS_RELEASE:STRING="$RPM_OPT_FLAGS" \
      -DCMAKE_CXX_FLAGS_RELEASE:STRING="$RPM_OPT_FLAGS" \
      ..

%{__make} %{?_smp_mflags}

%install
cd build
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}
%{__rm} -rf %{buildroot}%{_libdir}/*.la
%{__rm} -rf %{buildroot}/%{_sysconfdir}/xdg
%{__mkdir_p} %{buildroot}%{_datadir}/icons
%{__cp} ../icons/* %{buildroot}%{_datadir}/icons/

%clean
%{__rm} -rf %{buildroot}

%files qt
%defattr(-,root,root,-)
%doc README COPYING
%{_bindir}/antisipate
%{_mandir}/man1/antisipate.*
%{_datadir}/applications/antisipate.desktop
%{_datadir}/icons/*.png
%{_datadir}/pixmaps/antisipate.png

%files cli
%{_bindir}/sip-*
%{_mandir}/man1/sip-*.*

%changelog

