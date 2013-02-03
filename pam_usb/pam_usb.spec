%define author aluzzardi
%define githash 6a30dff
%define gitletter g
%define gitrelease 25

Name:          pam_usb
Version:       0.5.0
Release:       %{gitrelease}%{?dist}
License:       GPLv2+
Summary:       Hardware authentication for USB Flash Drives
URL:           http://pamusb.org
Source:        https://github.com/aluzzardi/pam_usb/tarball/master/%{author}-%{name}-%{version}-%{gitrelease}-%{gitletter}%{githash}.tar.gz
Group:         Applications/Security
BuildRoot:     %{_tmppath}/%{name}-%{version}-root
BuildRequires: gcc-c++, libxml2-devel, pam-devel, udisks-devel, pmount, dbus-devel
Requires:      libxml2, pam, udisks, pmount, dbus

%description
pam_usb provides hardware authentication for Linux using ordinary USB Flash
Drives. It works with any application supporting PAM, such as _su_ and 
login managers (_GDM_, _KDM_).

%prep
%setup -qn %{author}-%{name}-%{githash}

%build 
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_libdir}/security
make DESTDIR=%{buildroot} install
mv %{buildroot}/lib/security/* %{buildroot}%{_libdir}/security/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/pamusb.conf
%{_libdir}/security/pam_usb.so
%{_bindir}/pamusb-agent
%{_bindir}/pamusb-check
%{_bindir}/pamusb-conf
%{_docdir}/pamusb/CONFIGURATION.md
%{_mandir}/man1/pamusb-agent.1.gz
%{_mandir}/man1/pamusb-check.1.gz
%{_mandir}/man1/pamusb-conf.1.gz
%doc COPYING ChangeLog README.md


%changelog
* Wed Dec 12 2012 Didier Fabert <didier.fabert@gmail.com> 0.5.0-25
- First release
