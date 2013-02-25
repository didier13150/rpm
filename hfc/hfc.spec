Name:           hfc
Version:        1.9.8
Release:        1%{?dist}
Summary:        Grass covered areas in POV-Ray
License:        GPLv2
Group:          Applications/Multimedia
URL:            http://www.wozzeck.net/images/hfcomp/gazon-en.html
Source0:        http://www.wozzeck.net/images/hfcomp/%{name}.jar
Source1:        %{name}.desktop
Source2:        %{name}
Source3:        %{name}.html
Source4:        herbe.css
Source5:        scrinechotte.png
Source6:        demo.jpg

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  java-devel
BuildRequires:  jpackage-utils
Requires:       java
Requires:       jpackage-utils
Requires:       java3d


%description
The principle used in this software is to extend the principle of
Gille Tran's macros, to cover any height field.

%prep

%build
%{__cp} %{SOURCE3} .
%{__cp} %{SOURCE4} .
%{__cp} %{SOURCE5} .
%{__cp} %{SOURCE6} .

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
%doc hfc.html herbe.css scrinechotte.png demo.jpg

%changelog
* Sat Feb 16 2013 Didier Fabert <didier.fabert@gmail.com> 1.9.8-1
- First Release