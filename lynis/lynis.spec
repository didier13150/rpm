Name:           lynis
Version:        1.5.0
Release:        1%{?dist}
Summary:        Security and system auditing tool
License:        GPLv3
URL:            http://cisofy.com/lynis/
Source0:        http://cisofy.com/files/%{name}-%{version}.tar.gz
Patch0:         lynis-grub-sha-password.patch
Patch1:         lynis-legal-banner-add-string.patch
BuildArch:      noarch
Requires:       audit
Requires:       e2fsprogs
Requires:       module-init-tools

%description
Lynis is an auditing and hardening tool for Unix/Linux and you might even call
it a compliance tool. It scans the system and installed software. Then it 
performs many individual security control checks. It determines the hardening 
state of the machine, detects security issues and provides suggestions to 
improve the security defense of the system.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
# Empty build.

%install
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
install -pm644 default.prf %{buildroot}%{_sysconfdir}/%{name}

mkdir -p %{buildroot}%{_bindir}
install -pm755 lynis %{buildroot}%{_bindir}

mkdir -p %{buildroot}%{_mandir}/man8
install -pm644 lynis.8 %{buildroot}%{_mandir}/man8

mkdir -p  %{buildroot}%{_datadir}/%{name}/include/
# Forced by upstream. Otherwise these scripts can't be executed.
install -pm600 include/* %{buildroot}%{_datadir}/%{name}/include/

mkdir -p  %{buildroot}%{_datadir}/%{name}/plugins/
install -pm644 plugins/* %{buildroot}%{_datadir}/%{name}/plugins/

mkdir -p %{buildroot}%{_datadir}/%{name}/db/
install -pm644 db/* %{buildroot}%{_datadir}/%{name}/db/

mkdir -p %{buildroot}%{_localstatedir}/log/
touch %{buildroot}%{_localstatedir}/log/lynis.log
touch %{buildroot}%{_localstatedir}/log/lynis-report.dat

%files
%doc CHANGELOG FAQ LICENSE README
%{_bindir}/lynis
%{_datadir}/%{name}
%{_mandir}/man8/lynis.8*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/default.prf
%ghost %{_localstatedir}/log/lynis.log
%ghost %{_localstatedir}/log/lynis-report.dat

%changelog
* Sun Apr 13 2014 Didier Fabert <didier.fabert@gmail.com> - 1.5.0-1
- Update to 1.5.0

* Fri Feb 21 2014 Christopher Meng <rpm@cicku.me> - 1.4.2-1
- Update to 1.4.2

* Wed Feb 19 2014 Christopher Meng <rpm@cicku.me> - 1.4.1-1
- Update to 1.4.1

* Fri Feb 07 2014 Christopher Meng <rpm@cicku.me> - 1.4.0-1
- Update to 1.4.0

* Fri Jan 10 2014 Christopher Meng <rpm@cicku.me> - 1.3.9-1
- Update to 1.3.9

* Sat Dec 28 2013 Christopher Meng <rpm@cicku.me> - 1.3.8-1
- Update to 1.3.8

* Thu Dec 12 2013 Christopher Meng <rpm@cicku.me> - 1.3.7-1
- Update to 1.3.7

* Wed Dec 04 2013 Christopher Meng <rpm@cicku.me> - 1.3.6-1
- Update to 1.3.6

* Tue Nov 26 2013 Christopher Meng <rpm@cicku.me> - 1.3.5-1
- Update to 1.3.5

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 30 2010 Rakesh Pandit <rakesh@fedoraproject.org> - 1.2.9-1
- Updated to 1.2.9

* Fri Dec 04 2009 Rakesh Pandit <rakesh@fedoraproject.org> - 1.2.7-1
- Updated to 1.2.7

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 08 2009 Rakesh Pandit <rakesh@fedoraproject.org> - 1.2.6-2
- fixed requires tag

* Sun Apr 12 2009 Rakesh Pandit <rakesh@fedoraporject.org> - 1.2.6-1
- Updated to 1.2.6: CHANHELOG for details

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Nov 07 2008 Rakesh Pandit <rakesh@fedoraproject.org> - 1.2.1-3
- cleaned %%files

* Fri Nov 07 2008 Rakesh Pandit <rakesh@fedoraproject.org> - 1.2.1-2
- macros consistency - fixed hard code path

* Fri Oct 31 2008 Rakesh Pandit <rakesh@fedoraproject.org> - 1.2.1-1
- Initial package
