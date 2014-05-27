%define major_ver 0.60
Name:           geomorph
Version:        %{major_ver}.1
Release:        1%{?dist}
Summary:        A height field editor for Linux
License:        GPLv2
Group:          Applications/Multimedia
URL:            http://geomorph.sourceforge.net
Source0:        http://sourceforge.net/projects/geomorph/files/geomorph/%{major_ver}/%{name}-%{version}.tar.gz
Source1:        geomorph.desktop

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  gtkglext-devel, mesa-libGLU-devel
Requires:       gtkglext-libs, mesa-libGLU

%description
Geomorph is a height field generator and editor for the Linux operating system.
A height field is a kind of topographic map.  It is a 2D projection of a 
3D landscape.
Geomorph generates square images and shows a 3D preview of the resulting
landscape.  The resulting 2D image can be processed with a tool like Povray
for rendering the landscape.

%prep
%setup -qn %{name}-%{version}
# Tarball contains an already compiled app.
# Remove and recompile it.
%{__rm} -f scenes/colmap
%configure \
    --disable-rpath

%build
pushd scenes
g++ colmap.c -o colmap
popd
make %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

# Remove sources
%{__rm} -rf %{buildroot}%{_prefix}/src
# Create directories
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/applications
# Copy new desktop file
%{__install} %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/applications
# Copy icon file
%{__cp} GeoMorph.xpm $RPM_BUILD_ROOT%{_datadir}/icons

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/geomorph
%{_datadir}/geomorph
%{_datadir}/locale/*/LC_MESSAGES/geomorph.mo
%{_datadir}/applications/geomorph.desktop
%{_datadir}/icons/GeoMorph.xpm

%changelog
* Tue Feb 14 2012 Didier Fabert <didier.fabert@gmail.com> 0.60.1-1
- First Release
