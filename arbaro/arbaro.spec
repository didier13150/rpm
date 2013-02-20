%define us_ver %(echo %{version} | sed -e 's/\\\./_/g')
Name:           arbaro
Version:        1.9.8
Release:        1%{?dist}
Summary:        Tree generation for povray
License:        GPLv2
Group:          Applications/Multimedia
URL:            http://arbaro.sourceforge.net
Source0:        http://sourceforge.net/projects/arbaro/files/arbaro/%{version}/%{name}_%{us_ver}.zip
Source1:        %{name}.desktop
Source2:        %{name}
Source3:        %{name}-gui

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  java-devel
BuildRequires:  jpackage-utils
Requires:       java
Requires:       jpackage-utils

%description
Arbaro is an implementation of the tree generating algorithm described in
Jason Weber & Joseph Penn: Creation and Rendering of Realistic Trees

%prep
%setup -qc %{name}_%{us_ver}

%build
%{__rm} -f build.xml
%{__rm} -rf src test

%install
rm -rf $RPM_BUILD_ROOT
%{__mkdir_p} $RPM_BUILD_ROOT%{_bindir}
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/applications
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/%{name}
%{__mkdir_p} $RPM_BUILD_ROOT%{_javadir}/%{name}
%{__mkdir_p} $RPM_BUILD_ROOT%{_javadocdir}/%{name}
%{__install} *.jar $RPM_BUILD_ROOT%{_javadir}/%{name}
%{__install} %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/applications
%{__install} %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}
%{__install} %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}
%{__cp} -r doc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}
%{__cp} -r pov $RPM_BUILD_ROOT%{_datadir}/%{name}
%{__cp} -r trees $RPM_BUILD_ROOT%{_datadir}/%{name}

sed -i -e 's#@datadir@#%{_javadir}/%{name}#' $RPM_BUILD_ROOT%{_bindir}/%{name}
sed -i -e 's#@datadir@#%{_javadir}/%{name}#' $RPM_BUILD_ROOT%{_bindir}/%{name}-gui

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}*
%{_javadir}/%{name}
%{_javadocdir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%doc COPYING README

%changelog
* Sat Feb 16 2013 Didier Fabert <didier.fabert@gmail.com> 1.9.8-1
- First Release