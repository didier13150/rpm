%define svnrevision 1305095
Name:           kpovmodeler
Version:        1.1.3
Release:        0.3.qt5%{?dist}
Summary:        KDE Graphical 3D modeler for POV-Ray
License:        GPLv2
URL:            http://www.kpovmodeler.org
Group:          Applications/Multimedia
# The source for this package was given from non-official upstream.
# Downloaded from https://app.box.com/s/8rn3tl8lglmvoef3tqwl
Source0:        %{name}-qt5.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  cmake, kdelibs-devel, freetype-devel
Requires:       povray, freetype
Obsoletes:      %{name} <= %{version}-0.2.svn1305095

%description
KPovModeler is a modeling and composition program for creating POV-Ray scenes
in KDE.

For most modelers, POV-Ray is nothing but a rendering engine. This greatly
limits the innate possibilities of the POV-Ray scripted language. This is not
the case for KPovModeler, which allows you to use all the features of POV-Ray
through the translation of POV-Ray language into a graphical tree. 

%prep
%setup -qn %{name}-qt5

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
* Sat Feb 08 2014 Didier Fabert <didier.fabert@gmail.com> 1.1.3-0.qt5
- reworked for qt5, qt3 support removed from qt code, kpart use almost them by eticre

* Sun Jul 21 2013 Didier Fabert <didier.fabert@gmail.com> 1.1.3-0.2.svn1305095
- Add freetype-devel to build requires

* Sat Jun 15 2013 Didier Fabert <didier.fabert@gmail.com> 1.1.3-0.1.svn1305095
- First Release
