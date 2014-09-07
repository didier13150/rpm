Name:           ttygif
Version:        1.0.8
Release:        1%{?dist}
Summary:        Make GIF from recorded tty
License:        MIT
URL:            https://github.com/icholy/ttygif
Source0:        ttygif.tar.gz
BuildRequires:  libbsd-devel

%description
ttygif converts a ttyrec file into gif files. It's a stripped down version
of ttyplay which calls import on every frame.

%prep
%setup -qn %{name}-%{version}
find . -name '*_osx*' -delete

%build
make %{?_smp_mflags}

%install
%{__mkdir_p} %{buildroot}%{_bindir}
%{__install} -pm755 ttygif %{buildroot}%{_bindir}
%{__install} -pm755 concat.sh %{buildroot}%{_bindir}/ttygif-concat.sh

%files
%doc README.md
%{_bindir}/ttygif
%{_bindir}/ttygif-concat.sh

%changelog
* Sun Sep 07 2014 Didier Fabert <didier.fabert@gmail.com> - 1.0.8-1
- Initial package
