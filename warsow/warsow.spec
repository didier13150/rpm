%define shortver 15
Summary:          The most fast-paced sport on the web
Name:             warsow
Version:          1.5
Release:          1%{?dist}
License:          GPLv2
Group:            Amusements/Games
URL:              http://www.warsow.net/
Source0:          http://www.warsow.net:1337/~%{name}/%{version}/%{name}_%{shortver}_sdk.tar.gz
Source1:          http://www.warsow.net:1337/~%{name}/%{version}/%{name}_%{shortver}_unified.tar.gz
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:    libcurl-devel
BuildRequires:    openal-soft-devel
BuildRequires:    libogg-devel
BuildRequires:    libvorbis-devel
BuildRequires:    alsa-lib-devel
BuildRequires:    SDL-devel
BuildRequires:    libstdc++-static
BuildRequires:    libtheora-devel
BuildRequires:    zlib-devel
BuildRequires:    libXinerama-devel
BuildRequires:    libXi-devel
BuildRequires:    freetype-devel
BuildRequires:    libjpeg-turbo-devel
BuildRequires:    libpng-devel
Requires:         SDL
Requires:         openal-soft
Requires:         zlib
Requires:         freetype

BuildRequires:    tree

%description
Warsow is set in a futuristic cartoonish world where rocketlauncher-wielding
pigs and lasergun-carrying cyberpunks roam the streets. It is a completely
free, fast-paced first-person shooter for Windows, Linux, and Mac OS X.

Speed and movement is what Warsow is all about. Like a true cyberathlete you
jump, dash, dodge, and walljump your way through the game. Grab power-ups
before your enemy does, plant a bomb before anyone sees you, and steal the
enemy’s flag before they know what is going on!

%package data
Requires:         %{name} = %{version}-%{release}
Summary:          Data files for warsow
Group:            Amusements/Games
License:          Warsow Content License
#BuildArch:        noarch


%description data
All artwork, musics, dialogues, stories, names, 3d models, etc... are under 
a proprietary license. This means you cannot reuse those in any way.

%prep
%setup -qc %{name}-%{version}
tar -xzf %{SOURCE1}

%build
pushd source/source/
%{__make} %{?_smp_mflags}
popd
%{__rm} -f warsow_15/basewsw/*.so
cat << EOF > %{name}
#!/bin/bash
%{_bindir}warsow.%{_arch} +set fs_basepath %{_datadir}/%{name} +set fs_usehomedir 1
EOF


%install
%{__mkdir_p} %{buildroot}%{_datadir}/%{name}
%{__mkdir_p} %{buildroot}%{_libdir}/%{name}
%{__mkdir_p} %{buildroot}%{_bindir}
%{__cp} %{name} %{buildroot}%{_bindir}/
%{__cp} source/source/release/%{name}.%{_arch} %{buildroot}%{_bindir}/
%{__cp} source/source/release/libs/* %{buildroot}%{_libdir}/%{name}/
%{__cp} source/source/release/basewsw/* %{buildroot}%{_libdir}/%{name}/
%{__cp} -r warsow_15/basewsw %{buildroot}%{_datadir}/%{name}/
pushd %{buildroot}%{_datadir}/%{name}
ln -s %{_libdir}/warsow/ libs
popd
tree ../../BUILDROOT

%files
%defattr(-, root, root, 0755)
%doc warsow_15/docs/*.txt
%{_bindir}/%{name}*
%{_libdir}/%{name}
%dir %{_datadir}/%{name}/basewsw
%{_datadir}/%{name}/libs

%files data
%defattr(-, root, root, 0755)
%{_datadir}/%{name}/basewsw/configs
%{_datadir}/%{name}/basewsw/*.pk3
%{_datadir}/%{name}/basewsw/*.cfg


%changelog
* Fri May 09 2014 Didier Fabert <didier.fabert@gmail.com> 1.5-1
- First Import
