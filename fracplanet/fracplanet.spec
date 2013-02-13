Name:           fracplanet
Version:        0.4.0
Release:        1%{?dist}
Summary:        Fractal planet and terrain generator
License:        GPLv2
Group:          Sound and Video
URL:            http://sourceforge.net/projects/fracplanet
Source0:        %{name}-%{version}.tar.gz
Patch0:         fracplanet-libglu.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  qt-devel, boost-devel, mesa-libGLU-devel
Requires:       qt, boost, mesa-libGLU

%description
Interactive application to generate and view random fractal planets and terrain
with oceans, mountains, icecaps and rivers, then export them to POV-Ray format
or Blender. Written in C++ using Qt and OpenGL.

%prep
%setup -qn %{name}
%patch0 -p1
export QTDIR=%{_prefix}
./configure

%build
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%{__mkdir_p} $RPM_BUILD_ROOT%{_bindir}
%{__install} fracplanet $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/fracplanet

%changelog
* Thu Feb 14 2012 Didier Fabert <didier.fabert@gmail.com> 0.4.0-1
- First Release