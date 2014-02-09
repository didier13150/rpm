Name:           ngplant
Version:        0.9.11
Release:        1%{?dist}
Summary:        Plant generation for povray
License:        GPLv2
Group:          Applications/Multimedia
URL:            http://arbaro.sourceforge.net
Source0:        http://sourceforge.net/projects/%{name}/files/%{name}/%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}.desktop
Source2:        http://yorik.uncreated.net/scripts/export_pov.lua

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  wxGTK-devel
BuildRequires:  wxPython-devel
BuildRequires:  python-devel
BuildRequires:  scons
BuildRequires:  tree
BuildRequires:  freeglut-devel
BuildRequires:  libxslt
BuildRequires:  libjpeg-turbo-devel
Requires:       freeglut
Requires:       wxGTK
Requires:       python

%description
ngPlant is a plant modeling software package. ngPlant interactive tool can be
used to create 3D models of different plants and trees. ngPlant software
libraries can be used by developers in their 3D applications, or plant modeling
plugins.

%package apidoc
Group:          Documentation
Requires:       %{name} = %{version}
Summary:        API doc for %{name}

%description apidoc
API documentation for %{name}

%package povray
Group:          Applications/Multimedia
Requires:       %{name} = %{version}
Summary:        Lua script to export to POV-Ray

%description povray
Lua script to export %{name} to POV-Ray format

%prep
%setup -qn %{name}-%{version}

%build
sed -i -e '/PLUGINS_DIR/ s#None#"%{_datadir}/%{name}/plugins"#' SConstruct
/usr/bin/scons
ls -R build || true
ls -R pywrapper/build || true

%install
rm -rf $RPM_BUILD_ROOT
%{__mkdir_p} $RPM_BUILD_ROOT%{_bindir}
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/applications
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/%{name}
%{__mkdir_p} $RPM_BUILD_ROOT%{_docdir}/%{name}/api/images
for dir in plugins samples scripts shaders
do
    %{__cp} -r $dir $RPM_BUILD_ROOT%{_datadir}/%{name}/
done
%{__install} -m0755 devtools/ngpbench $RPM_BUILD_ROOT%{_bindir}
%{__install} -m0755 ngplant/ngplant $RPM_BUILD_ROOT%{_bindir}
%{__install} -m0755 ngpshot/ngpshot $RPM_BUILD_ROOT%{_bindir}
%{__install} -m0755 ngpview/ngpview $RPM_BUILD_ROOT%{_bindir}
#%{__install} -m0755 pywrapper/_ngp.so
%{__install} -m0644 docapi/*.html $RPM_BUILD_ROOT%{_docdir}/%{name}/api/
%{__install} -m0644 docapi/images/*.png $RPM_BUILD_ROOT%{_docdir}/%{name}/api/images
# Copy new desktop file
%{__install} %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/applications
# Copy icon file
%{__cp} ngplant/images/ngplant.xpm $RPM_BUILD_ROOT%{_datadir}/icons
%{__cp} ngplant/images/ngplant.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/
%{__install} %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/%{name}/plugins

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/ngp*
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/icons/%{name}.xpm
%doc README README.extern ReleaseNotes
%exclude %{_docdir}/%{name}/api
%exclude %{_datadir}/%{name}/plugins/export_pov.lua

%files apidoc
%{_docdir}/%{name}/api

%files povray
%{_datadir}/%{name}/plugins/export_pov.lua

%changelog
* Sun Feb 09 2014 Didier Fabert <didier.fabert@gmail.com> 0.9.11-1
- First Release
