Name:           ttyrec
Version:        1.0.8
Release:        1%{?dist}
Summary:        Record tty
License:        BSD
URL:            http://0xcc.net/ttyrec/
Source0:        http://0xcc.net/ttyrec/%{name}-%{version}.tar.gz
Patch0:         ttyrec-out-of-pty.patch
BuildRequires:  libbsd-devel

%description
ttyrec is a tty recorder. Recorded data can be played back with the included
ttyplay command. ttyrec is just a derivative of script command for recording
timing information with microsecond accuracy as well.

%prep
%setup -qn %{name}-%{version}
%patch0 -p1

%build
make %{?_smp_mflags}

%install
%{__mkdir_p} %{buildroot}%{_bindir}
%{__install} -pm755 ttyplay %{buildroot}%{_bindir}
%{__install} -pm755 ttyrec %{buildroot}%{_bindir}
%{__install} -pm755 ttytime %{buildroot}%{_bindir}

%{__mkdir_p} %{buildroot}%{_mandir}/man1
%{__install} -pm644 ttyplay.1 %{buildroot}%{_mandir}/man1
%{__install} -pm644 ttyrec.1 %{buildroot}%{_mandir}/man1
%{__install} -pm644 ttytime.1 %{buildroot}%{_mandir}/man1

%files
%doc README
%{_bindir}/ttyplay
%{_bindir}/ttyrec
%{_bindir}/ttytime
%{_mandir}/man1/ttyplay.1*
%{_mandir}/man1/ttyrec.1*
%{_mandir}/man1/ttytime.1*

%changelog
* Sun Sep 07 2014 Didier Fabert <didier.fabert@gmail.com> - 1.0.8-1
- Initial package
