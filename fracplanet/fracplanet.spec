Name:           fracplanet
Version:        0.4.0
Release:        2%{?dist}
Summary:        Fractal planet and terrain generator
License:        GPLv2
Group:          Applications/Multimedia
URL:            http://sourceforge.net/projects/fracplanet
Source0:        http://sourceforge.net/projects/fracplanet/files/fracplanet/%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}.desktop
Patch0:         fracplanet-libglu.patch
Patch1:         fracplanet-doxygen-png-img.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  qt-devel, boost-devel, mesa-libGLU-devel, doxygen, libxslt
BuildRequires:  graphviz
Requires:       qt, boost, mesa-libGLU

%description
Interactive application to generate and view random fractal planets and terrain
with oceans, mountains, icecaps and rivers, then export them to POV-Ray format
or Blender. Written in C++ using Qt and OpenGL.

%package apidoc
Group: Documentation
Summary: fracplanet API docs
Requires: fracplanet = %{version}-%{release}

%description apidoc
Documentation for the fracplanet API

%prep
%setup -qn %{name}
%patch0 -p1
%patch1 -p1
echo "ERROR" > usage_text.h
xsltproc -stringparam version %{version} -html htm_to_qml.xsl fracplanet.htm | \
	sed 's/"/\\"/g' | sed 's/^/"/g' | sed 's/$/\\n"/g'> usage_text.h

qmake-qt4 "VERSION_NUMBER=%{version}" fracplanet.pro
doxygen -u doxygen.cfg
doxygen doxygen.cfg

%build
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%{__mkdir_p} $RPM_BUILD_ROOT%{_bindir}
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/applications
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/apidoc
%{__mkdir_p} $RPM_BUILD_ROOT%{_mandir}/man1
%{__mkdir_p} $RPM_BUILD_ROOT%{_mandir}
%{__install} fracplanet $RPM_BUILD_ROOT%{_bindir}
%{__install} man/man1/fracplanet.1 $RPM_BUILD_ROOT%{_mandir}/man1
%{__install} %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/applications
%{__cp} -r doc/* $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/apidoc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/fracplanet
%{_datadir}/applications/fracplanet.desktop
%doc fracplanet.htm fracplanet.css BUGS LICENSE NEWS README THANKS TODO
%{_mandir}/man1/fracplanet.1*

%files apidoc
%defattr(-,root,root,-)
%{_datadir}/%{name}-%{version}/apidoc

%changelog
* Thu Feb 14 2013 Didier Fabert <didier.fabert@gmail.com> 0.4.0-2
- Add desktop file
- Include doc, man
- Add sub package apidoc

* Thu Feb 14 2013 Didier Fabert <didier.fabert@gmail.com> 0.4.0-1
- First Release