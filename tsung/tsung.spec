# Avoid installing arch-independent data into arch-dependent directory
# MUST for Erlang packages.
%global debug_package %{nil}

Name:           tsung
Version:        1.6.0
Release:        1%{?dist}
Summary:        A distributed multi-protocol load testing tool
License:        GPLv2
URL:            http://tsung.erlang-projects.org/
Source0:        http://tsung.erlang-projects.org/dist/%{name}-%{version}.tar.gz
BuildRequires:  erlang
Requires:       erlang
Requires:       gnuplot
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
tsung is a distributed load testing tool. It is protocol-independent and can 
currently be used to stress and benchmark HTTP, Jabber/XMPP, PostgreSQL, 
MySQL and LDAP servers.

It simulates user behaviour using an XML description file, reports many 
measurements in real time (statistics can be customized with transactions, 
and graphics generated using gnuplot).

For HTTP, it supports 1.0 and 1.1, has a proxy mode to record sessions, 
supports GET and POST methods, Cookies, and Basic WWW-authentication.
 
It also has support for SSL.

%prep
%setup -qn %{name}
# Fix bogus shebangs.
sed -i 's|/usr/bin/env bash|/bin/bash|' *.sh.in
sed -i 's|/usr/bin/env python|%{__python2}|' src/tsung-plotter/tsplot.py.in
sed -i 's|/usr/bin/env perl|%{__perl}|' src/log2tsung.pl.in

%build
%configure --prefix=/usr
%make_build

%install
%make_install

for i in `ls %{buildroot}%{_libdir}/%{name}/bin | grep .pl$ | cut -d"." -f1`
do
  ln -sf %{_libdir}/%{name}/bin/$i.pl %{buildroot}%{_bindir}/$i
done

# Fix versioned/unversioned docdir
rm -frv %{buildroot}%{_docdir}
rm -frv examples/*.xml.in

%files
%doc CHANGES CONTRIBUTORS COPYING README* TODO
%doc examples/
%{_bindir}/*
%{_datadir}/%{name}/
%{_libdir}/erlang/lib/*
%{_libdir}/%{name}/
%{_mandir}/man1/%{name}*.1*
%{_mandir}/man1/tsplot.1*

%changelog
* Fri Jan 08 2016 Didier Fabert <didier.fabert@gmail.com> - 1.6.0-1
- Update to 1.6.0

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.5.1-5
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.5.1-4
- Perl 5.20 rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 10 2014 Christopher Meng <rpm@cicku.me> - 1.5.1-2
- Include example config files
- Better user experience for perl scripts

* Thu Jul 10 2014 Christopher Meng <rpm@cicku.me> - 1.5.1-1
- Update to 1.5.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Sep 01 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.5.0-3
- Fix versioned/unversioned docdir

* Fri Aug 02 2013 Christopher Meng <rpm@cicku.me> - 1.5.0-2
- Fix wrong syntaxs of files.

* Sat May 25 2013 Christopher Meng <rpm@cicku.me> - 1.5.0-1
- Initial Package.
