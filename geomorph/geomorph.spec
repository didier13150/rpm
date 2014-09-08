%global major_ver 0.60
Name:           geomorph
Version:        %{major_ver}.1
Release:        2%{?dist}
Summary:        A height field editor for Linux
License:        GPLv2
Group:          Applications/Multimedia
URL:            http://geomorph.sourceforge.net
Source0:        http://sourceforge.net/projects/geomorph/files/geomorph/%{major_ver}/%{name}-%{version}.tar.gz
Source1:        geomorph.desktop
Patch0:         geomorph-format-security.patch
Patch1:         geomorph-array-bounds.patch
BuildRequires:  gtkglext-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  desktop-file-utils
Requires:       povray

%description
Geomorph is a height field generator and editor for the Linux operating system.
A height field is a kind of topographic map.  It is a 2D projection of a 
3D landscape.
Geomorph generates square images and shows a 3D preview of the resulting
landscape.  The resulting 2D image can be processed with a tool like Povray
for rendering the landscape.

%prep
%setup -qn %{name}-%{version}
%patch0 -p1 -b .format-security
%patch1 -p1 -b .array-bounds

# to avoid rpmlint warnings
# Remove exe bit from pixmaps
find . -name \*.xpm -exec chmod -x {} \;
# Change fsf address
find src -type f -exec sed -i -e '/Foundation/ s#Inc.,.*#51 Franklin Street, Fifth Floor, Boston, MA 02110-1301#' {} \;
# Switch to UTF-8
for file in LISEZMOI AFAIRE FAQ-fr
do
    iconv -f ISO-8859-1 -t UTF-8 $file > $file.utf8
    touch -r $file $file.utf8
    mv -f $file.utf8 $file
done
# Tarball contains an already compiled app.
# Remove and recompile it.
%{__rm} -f scenes/colmap

# Remove Hardcoded path
for file in install-step1-dir install-step2-rcfile install-step3-menu install-step4-desktop install-user
do
    sed -i -e '/^VERSION/ s#=.*#=%{version}#g' \
        -e 's#/usr/local/share/geomorph#%{_datadir}/geomorph#g' \
        $file
done

%configure \
    --disable-rpath

%build
pushd scenes
%{__cc} ${RPM_OPT_FLAGS} -o colmap colmap.c
popd
make %{?_smp_mflags}

%install
make install DESTDIR="%{buildroot}"
%find_lang %{name}
mv %{buildroot}%{_datadir}/geomorph/%{version}/scenes/colmap %{buildroot}%{_bindir}/
%{__rm} -f %{buildroot}%{_datadir}/geomorph/%{version}/scenes/colmap.c
# Create directories
%{__mkdir_p} %{buildroot}%{_datadir}/icons
%{__mkdir_p} %{buildroot}%{_datadir}/applications
# Copy new desktop file
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE1}
# Copy icon file
%{__cp} GeoMorph.xpm %{buildroot}%{_datadir}/icons

%files -f %{name}.lang
%doc ABOUT-NLS AFAIRE AUTHORS ChangeLog FAQ FAQ-fr LISEZMOI NEWS README TODO geomorphrc_de geomorphrc_en geomorphrc_fr
%{_bindir}/geomorph
%{_bindir}/colmap
%{_datadir}/geomorph
%{_datadir}/applications/geomorph.desktop
%{_datadir}/icons/GeoMorph.xpm

%changelog
* Tue May 27 2014 Didier Fabert <didier.fabert@gmail.com> 0.60.1-2
- Follow Fedora Guidelines

* Tue Feb 14 2012 Didier Fabert <didier.fabert@gmail.com> 0.60.1-1
- First Release
