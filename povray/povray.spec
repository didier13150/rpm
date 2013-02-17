%define majorver 3.7
Name:          povray
Version:       %{majorver}.0.RC6
Release:       2%{?dist}
License:       Freeware
Summary:       Persistence of Vision Raytracer
URL:           http://www.povray.org
Source0:       http://www.povray.org/redirect/www.povray.org/beta/source/%{name}-%{version}.tar.gz
Patch0:        povray-boost-1.50.patch
Patch1:        povray-print-cmdline.patch
Group:         Applications/Multimedia
BuildRoot:     %{_tmppath}/%{name}-%{version}-root
BuildRequires: autoconf, automake, binutils, sed, grep, gcc-c++, libXpm
BuildRequires: libjpeg-devel, libtiff-devel, libpng-devel, zlib-devel
BuildRequires: svgalib-devel, libX11-devel, libXt-devel, xorg-x11-proto-devel
BuildRequires: boost-devel, SDL-devel, dos2unix
Requires:      boost, SDL

%description
The Persistence of Vision Raytracer is a high-quality, totally
free tool for creating stunning three-dimensional graphics. It
is available in official versions for Windows, Mac OS/Mac OS X
and i86 Linux. The source code is available for those wanting 
to do their own ports. 

%prep
%setup -q
%patch0 -p1
%patch1 -p1
find . -name '*.sh' -exec dos2unix {} \;

%build
CXXFLAGS="-Wno-multichar -Wdeprecated"
%configure \
           COMPILED_BY="rpmbuild" \
           --with-boost-thread=boost_thread-mt
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make DESTDIR=%{buildroot} install
# Add executable flag to script
chmod 0755 %{buildroot}%{_datadir}/%{name}-%{majorver}/scenes/camera/mesh_camera/bake.sh
# Delete empty hidden directory
%{__rm} -rf %{buildroot}%{_datadir}/%{name}-%{majorver}/include/.directory

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_docdir}/%{name}-%{majorver}/*
%{_mandir}/man1/povray.*
%{_datadir}/%{name}-%{majorver}/*
%config(noreplace) %{_sysconfdir}/%{name}/%{majorver}/*
%doc AUTHORS COPYING ChangeLog NEWS README VERSION changes.txt revision.txt

%changelog
* Sun Feb 17 2013 Didier Fabert <didier.fabert@gmail.com> 3.7.0.RC6-2
- Print command line on stdout

* Sun Jul 15 2012 Didier Fabert <didier.fabert@gmail.com> 3.7.0.RC6-1
- Update to 3.7.0.RC6

* Fri Jun 08 2007 <roma@lcg.ufrj.br> 3.6.1-2
- Included missing BRs.

* Wed Aug 02 2006 <roma@lcg.ufrj.br> 3.6.1-1
- Rebuilt for Fedora 5.

* Thu Nov  4 2004 <fenn@stanford.edu> 3.6.1-0
- RPM based off subpop.net FC1 3.50c package
- inc. Wolfgang Wieser's patchset 
  (http://www.cip.physik.uni-muenchen.de/~wwieser/render/povray/patches/)
