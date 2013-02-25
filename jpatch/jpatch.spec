%define us_ver %(echo %{version} | sed -e 's/\\\./_/g')
%define preview 1
Name:           jpatch
Version:        0.4
Release:        1%{?dist}
Summary:        Spline based 3D modeling tool
License:        GPLv2
Group:          Applications/Multimedia
URL:            http://www.jpatch.com
Source0:        http://downloads.sourceforge.net/project/jpatch/jpatch/JPatch%200.4%20PREVIEW%201/%{name}%{us_ver}preview%{preview}.zip
Source1:        %{name}.desktop
Source2:        %{name}

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  java-devel
BuildRequires:  jpackage-utils
Requires:       java
Requires:       jpackage-utils
Requires:       java3d

%description
JPatch is a spline based 3D modeling tool (a patch modeler). It can be used
to create 3D models for POV-Ray or RenderMan compatible renderers
(e.g. Aqsis).

The current version (JPatch 0.4) supports modeling and some very basic
animation features.
%prep
%setup -qn %{name}%{version}p%{preview}

%build
%{__rm} -f build.xml
%{__rm} -rf src test

%install
rm -rf $RPM_BUILD_ROOT
%{__mkdir_p} $RPM_BUILD_ROOT%{_bindir}
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/applications
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/%{name}
%{__mkdir_p} $RPM_BUILD_ROOT%{_javadir}/%{name}
%{__install} %{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}
%{__install} %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/applications
%{__install} %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}
%{__cp} -r demo $RPM_BUILD_ROOT%{_datadir}/%{name}
%{__cp} -r textures $RPM_BUILD_ROOT%{_datadir}/%{name}

sed -i -e 's#@datadir@#%{_javadir}/%{name}#' $RPM_BUILD_ROOT%{_bindir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_javadir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%doc LICENSE.TXT README.TXT

%changelog
* Sat Feb 16 2013 Didier Fabert <didier.fabert@gmail.com> 1.9.8-1
- First Release