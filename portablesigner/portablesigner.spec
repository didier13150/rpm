Name:           portablesigner
Version:        2.0
Release:        1%{?dist}
Summary:        Signing PDF files with X.509 certificates
License:        GPLv2
Group:          Applications/Security
URL:            http://arbaro.sourceforge.net
Source0:        http://sourceforge.net/projects/portablesigner/files/portablesigner/2.0-Release/PortableSigner-Generic-2.0.38c0573.zip
Source1:        portablesigner

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  java-devel
BuildRequires:  jpackage-utils
Requires:       java
Requires:       jpackage-utils

%description
PortableSigner is a signing program for PDF files with X.509 certificates).

%prep
%setup -qc %{name}_%{version}

%build
cat << EOF > portablesigner.desktop
[Desktop Entry]
Version=1.0
Terminal=false
Exec=%{name}
Icon=%{_datadir}/pixmap/%{name}.png
Type=Application
Categories=Office;Utility;Application
StartupNotify=false
Name=PortableSigner
Name[de]=PortableSigner PDF signieren
Name[en_GB]=PortableSigner sign PDF files
Name[en]=PortableSigner sign PDF files
Comment=Digital sign PDF files with X.509 certificates
Comment[de]=Digitales signieren von PDF Dateien mit X.509 Zertifikaten
Comment[en_GB]=Digital sign PDF files with X.509 certificates
Comment[en]=Digital sign PDF files with X.509 certificates
EOF
%{__mv} linux/Readme.txt Readme.txt

%install
rm -rf $RPM_BUILD_ROOT
%{__mkdir_p} $RPM_BUILD_ROOT%{_bindir}
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/applications
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/pixmaps
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/%{name}
%{__mkdir_p} $RPM_BUILD_ROOT%{_javadir}/%{name}
%{__cp} -r *.jar lib $RPM_BUILD_ROOT%{_javadir}/%{name}
%{__cp} %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}

%{__install} linux/PortableSignerLogo.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/%{name}.png
%{__install} portablesigner.desktop $RPM_BUILD_ROOT%{_datadir}/applications/
sed -e 's#@datadir@#%{_javadir}/%{name}#' \
    $RPM_BUILD_ROOT%{_bindir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_javadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%doc Readme.txt

%changelog
* Fri May 23 2014 Didier Fabert <didier.fabert@gmail.com> 2.0-1
- First Release
