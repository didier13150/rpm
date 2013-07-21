%define svnrevision 1305095
Name:           kpovmodeler
Version:        1.1.3
Release:        0.2.svn%{svnrevision}%{?dist}
Summary:        KDE Graphical 3D modeler for POV-Ray
License:        GPLv2
URL:            http://www.kpovmodeler.org
Group:         Applications/Multimedia
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#  svn export -r 1305095 svn://anonsvn.kde.org/home/kde/trunk/extragear/graphics/kpovmodeler kpovmodeler-1.1.3
#  tar -czvf kpovmodeler-1.1.3.tar.gz kpovmodeler-1.1.3
Source0:        %{name}-%{version}.tar.gz
# Remove radiosity option from command line ( removed option with povray > 3.6 )
Patch0:         kpovmodeler-povray37-no-radiosity-opt.patch
# Add include path for freetype2 (ftheader.h moved from freetype to freetype-devel)
Patch1:         kpovmodeler-freetype2-include-path.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  cmake, kdelibs-devel, freetype-devel
Requires:       povray, freetype

%description
KPovModeler is a modeling and composition program for creating POV-Ray scenes
in KDE.

For most modelers, POV-Ray is nothing but a rendering engine. This greatly
limits the innate possibilities of the POV-Ray scripted language. This is not
the case for KPovModeler, which allows you to use all the features of POV-Ray
through the translation of POV-Ray language into a graphical tree. 

%prep
%setup -q
%patch0 -p0
%patch1 -p0

%build
cmake . \
        -DCMAKE_INSTALL_PREFIX="%{_prefix}" \
        -DCMAKE_BUILD_TYPE=RelWithDebInfo

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_libdir}/kde4/lib%{name}part.so
%{_libdir}/libl%{name}.so*
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/icons/oxygen/*/mimetypes/%{name}_doc.png
%{_datadir}/applications/kde4/%{name}.desktop
%{_datadir}/dbus-1/interfaces/org.kde.%{name}.xml
%{_datadir}/kde4/apps/%{name}
%{_datadir}/kde4/services/%{name}part.desktop
%doc AUTHORS BUGS COPYING ChangeLog README REQUIREMENTS StyleConvention TODO

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%changelog
* Sat Jul 21 2013 Didier Fabert <didier.fabert@gmail.com> 1.1.3-0.2.svn1305095
- Add freetype-devel for build requires

* Sat Jun 15 2013 Didier Fabert <didier.fabert@gmail.com> 1.1.3-0.1.svn1305095
- First Release