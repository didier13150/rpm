Summary:        Linux Security Auditing Tool
Name:           lsat
Version:        0.9.8.2
Release:        1%{?dist}
License:        GPLv2
Group:          Applications/System
URL:            http://usat.sourceforge.net/
Source0:        http://usat.sourceforge.net/code/%{name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:  /usr/bin/pod2man
BuildRequires:  /usr/bin/gzip

%description
Linux Security Auditing Tool (LSAT) is a post install security auditing tool.
It is modular in design, so new features can be added quickly. It checks many
system configurations and local network settings on the system for common
security/configurations errors and for packages that are not needed.

%prep
%setup -qn %{name}-%{version}

%build
%{__mv} changelog/changelog.html changelog.html
%configure
make %{?_smp_mflags}
/usr/bin/pod2man %{name}.pod > %{name}.1
/usr/bin/gzip %{name}.1

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_bindir}
%{__cp} %{name} %{buildroot}%{_bindir}/%{name}
%{__mkdir_p} %{buildroot}%{_mandir}/man1
%{__cp} %{name}.1.gz %{buildroot}%{_mandir}/man1/%{name}.1.gz

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc README README.checkrpm README.exclude README.modules modules.html sample_exclude.txt securitylinks.txt changelog.html
%attr(0755,root,root) %{_bindir}/%{name}
%{_mandir}/man*/%{name}*

%changelog
* Sat May 30 2015 Didier Fabert <didier.fabert@gmail.com> 0.9.8.2-1
- Update from upstream

* Tue May 06 2014 Didier Fabert <didier.fabert@gmail.com> 0.9.8-1
- First Import

