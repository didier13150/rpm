%define perlname Parse-RPM-Spec
Name:           perl-Parse-RPM-Spec
Version:        0.08
Release:        1%{?dist}
Summary:        Perl module which models RPM spec files
License:        GPL or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Parse-RPM-Spec/
Source0:        http://search.cpan.org/CPAN/authors/id/D/DA/DAVECROSS/%{perlname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  perl(Test::More)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Moose)

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Parse::RPM::Spec is a Perl module which models RPM spec files.

%prep
%setup -qn %{perlname}-%{version}
chmod -x Changes README


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Tue Jun 18 2013 Didier Fabert <didier.fabert@gmail.com> 0.08-1
- Initial import

