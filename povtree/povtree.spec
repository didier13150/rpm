Name:           povtree
Version:        1.5
Release:        2%{?dist}
Summary:        Tree generator for POV-Ray
License:        GPLv2
Group:          Applications/Multimedia
URL:            http://web.archive.org/web/20071101052625/propro.ru/go/Wshop/povtree/download.html
Source0:        http://web.archive.org/web/20071101052625/propro.ru/go/Wshop/povtree/%{name}%{version}.zip
Source1:        %{name}.desktop
Source2:        %{name}
Source3:        make-icons.sh
Source4:        icon.svg
Source5:        README.icon

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  java-devel
BuildRequires:  jpackage-utils
BuildRequires:  ImageMagick
Requires:       java
Requires:       jpackage-utils

%description
POV-Tree is a Java tree generator for POV-Ray. Tree generation algorithm
which is used in this program was based on TOMTREE macro developed by
Tom Aust.

You can think of this program as of GUI for that macro. In addition to the
possibility to define numerous parameters you can also preview tree and
save it either as an include file or as a mesh file.

%prep
%setup -qc %{name}%{version}
cp %{SOURCE3} %{SOURCE4} %{SOURCE5} .

%build
sed -i -e 's/@appname@/%{name}/' make-icons.sh
chmod +x make-icons.sh
bash make-icons.sh

%install
rm -rf $RPM_BUILD_ROOT
%{__mkdir_p} $RPM_BUILD_ROOT%{_bindir}
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/applications
for size in 16 22 32 48 64 128 256
do
  %{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${size}x${size}
done
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/%{name}
%{__mkdir_p} $RPM_BUILD_ROOT%{_javadir}/%{name}
%{__install} %{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}
%{__install} TOMTREE-1.5.inc $RPM_BUILD_ROOT%{_javadir}/%{name}
%{__install} help.jpg $RPM_BUILD_ROOT%{_javadir}/%{name}
%{__install} %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/applications
%{__install} %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}
%{__cp} -r de en fr it ja ru $RPM_BUILD_ROOT%{_javadir}/%{name}/
for size in 16 22 32 48 64 128 256
do
  %{__install} %{name}-hi${size}.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${size}x${size}/%{name}.png
done
%{__install} %{name}-hi32.png $RPM_BUILD_ROOT%{_datadir}/icons/%{name}.png
%{__install} icon.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/%{name}.svg
sed -i -e 's#@datadir@#%{_javadir}/%{name}#' $RPM_BUILD_ROOT%{_bindir}/%{name}
# Remove icon sources
%{__rm} -f make-icons.sh icon.svg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README.icon
%{_bindir}/%{name}
%{_javadir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/%{name}.png
%{_datadir}/icons/hicolor/scalable/%{name}.svg
%{_datadir}/icons/%{name}.png

%changelog
* Sun Jan 12 2014 Didier Fabert <didier.fabert@gmail.com> 1.5-2
- Add icons

* Mon Feb 25 2013 Didier Fabert <didier.fabert@gmail.com> 1.5-1
- First Release
