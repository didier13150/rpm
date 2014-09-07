%define perlname YAML-AppConfig
Name:           perl-YAML-AppConfig
Version:        0.19
Release:        1%{?dist}
Summary:        Manage configuration files with YAML and variable references
License:        GPL or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/YAML-AppConfig
Source0:        http://search.cpan.org/CPAN/authors/id/X/XA/XAERXESS/%{perlname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  perl(Test::More)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Moose)
BuildRequires:  perl-YAML-Syck

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
YAML::AppConfig extends the work done in Config::YAML and YAML::ConfigFile to
allow more flexible configuration files.

Your configuration is stored in YAML and then parsed and presented to you via
YAML::AppConfig. Settings can be referenced using get and set methods and
settings can refer to one another by using variables of the form $foo, much
in the style of AppConfig

%prep
%setup -qn %{perlname}-%{version}


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
%doc Changes MANIFEST README.md
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Tue Jul 01 2014 Didier Fabert <didier.fabert@gmail.com> 0.19-1
- Initial import

