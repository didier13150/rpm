%define us_ver %(echo %{version} | sed -e 's/\\\./_/g')
Name:           hfc
Version:        1.9.8
Release:        1%{?dist}
Summary:        Grass covered areas in POV-Ray
License:        GPLv2
Group:          Applications/Multimedia
URL:            http://www.wozzeck.net/images/hfcomp/gazon-en.html
Source0:        http://www.wozzeck.net/images/hfcomp/hfc.jar
Source1:        %{name}.desktop
Source2:        %{name}

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  java-devel
BuildRequires:  jpackage-utils
Requires:       java
Requires:       jpackage-utils
Requires:       java3d


%description
Arbaro is an implementation of the tree generating algorithm described in
Jason Weber & Joseph Penn: Creation and Rendering of Realistic Trees

%prep

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
%{__install} %{SOURCE0} $RPM_BUILD_ROOT%{_javadir}/%{name}
%{__install} %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/applications
%{__install} %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}

sed -i -e 's#@datadir@#%{_javadir}/%{name}#' $RPM_BUILD_ROOT%{_bindir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_javadir}/%{name}
%{_javadocdir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop

%changelog
* Sat Feb 16 2013 Didier Fabert <didier.fabert@gmail.com> 1.9.8-1
- First Release