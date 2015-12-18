%define majorver 3.7
Name:          povray
Version:       %{majorver}.1
Release:       2%{?dist}
License:       AGPLv3+
Summary:       Persistence of Vision Raytracer
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
URL:           http://www.povray.org
Source0:       https://github.com/POV-Ray/%{name}/archive/%{majorver}-stable.tar.gz
Patch0:        0001-Fix-encoding.patch
Patch1:        0002-Autotool-massaging.patch
Patch10:       povray-print-cmdline.patch
Patch11:       povray-noprint-authors.patch
Group:         Applications/Multimedia
BuildRoot:     %{_tmppath}/%{name}-%{version}-root
BuildRequires: autoconf, automake, binutils, sed, grep, gcc-c++, libXpm
BuildRequires: libjpeg-devel, libtiff-devel, libpng-devel, zlib-devel
BuildRequires: svgalib-devel, libX11-devel, libXt-devel, xorg-x11-proto-devel
BuildRequires: boost-devel, SDL-devel, dos2unix, OpenEXR-devel
Requires:      boost, SDL

%description
The Persistence of Vision Raytracer is a high-quality, totally
free tool for creating stunning three-dimensional graphics. It
is available in official versions for Windows, Mac OS/Mac OS X
and i86 Linux. The source code is available for those wanting 
to do their own ports. 

%package scenes
Summary:        POV-Ray example scenes
License:        CC-BY-SA
BuildArch:      noarch

%description scenes
POV-Ray example scenes.

%prep
%setup -qn %{name}-%{majorver}-stable
%patch0 -p1
%patch1 -p1
%patch10 -p1
%patch11 -p1
find . -name '*.sh' -exec dos2unix {} \;

# Make sure not to be using bundled libs
rm -rf libraries

# Workaround to automake incompatibility
rm -f config/missing

pushd unix
sed -i \
 -e 's,automake --warnings=all,automake -a -f,' \
 prebuild.sh

sed -i \
 -e 's,AM_INIT_AUTOMAKE(\[1.9 dist-bzip2\]),AM_INIT_AUTOMAKE([1.9 dist-bzip2 subdir-objects]),' \
 configure.ac
 
./prebuild.sh
popd


%build
CXXFLAGS="-Wno-multichar -Wdeprecated"
%configure \
           COMPILED_BY="rpmbuild" \
           --x-includes=%{_includedir} \
           --x-libraries=%{_libdir} \
           --with-boost=%{_libdir} \
           --disable-io-restrictions \
           --with-boost-thread=boost_thread LIBS=-Lboost_system

# Filter out bogus and potentially harmful
# -I%%{_includedir} -L%%{_libdir}
# from Makefiles
find -name Makefile -exec sed -i \
  -e 's,-I%{_includedir}$,,g;s,-I%{_includedir} ,,g;' \
  -e 's,-L%{_libdir}$,,g;s,-L%{_libdir} ,,g' {} \;

# Adjust bogus paths
sed -i \
  -e '/DEFAULT_DIR=/d' \
  -e 's,SYSCONFDIR=\$DEFAULT_DIR/etc,SYSCONFDIR=%{_sysconfdir},' \
  unix/scripts/{allanim,allscene,portfolio}.sh

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
%{_datadir}/%{name}-%{majorver}
%exclude %{_datadir}/%{name}-%{majorver}/scenes
%config(noreplace) %{_sysconfdir}/%{name}/%{majorver}/*
%doc AUTHORS COPYING ChangeLog NEWS README VERSION changes.txt revision.txt

%files scenes
%dir %{_datadir}/povray-%{majorver}
%{_datadir}/%{name}-%{majorver}/scenes

%changelog
* Wed May 27 2015 Didier Fabert <didier.fabert@gmail.com> 3.7.1-2
- Add official fedora binaries patches

* Tue Dec 17 2013 Didier Fabert <didier.fabert@gmail.com> 3.7.1-1
- Update to stable 3.7

* Sun Feb 17 2013 Didier Fabert <didier.fabert@gmail.com> 3.7.0.RC6-3
- No Print about authors, contributors ans libs

* Sun Feb 17 2013 Didier Fabert <didier.fabert@gmail.com> 3.7.0.RC6-2
- Print command line on stdout

* Sun Jul 15 2012 Didier Fabert <didier.fabert@gmail.com> 3.7.0.RC6-1
- First import 3.7.0.RC6
