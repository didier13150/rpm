Name:           libcouchbase
Version:        2.5.0
Release:        1%{?dist}
Summary:        C client library for Couchbase
License:        ASL 2.0
Group:          Applications/Databases
URL:            http://www.couchbase.com
Source0:        http://packages.couchbase.com/clients/c/%{name}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  cmake
BuildRequires:  libuv-devel
BuildRequires:  openssl-devel
BuildRequires:  libev-devel

%description
It communicates with the couchbase cluster and speaks the relevant protocols
necessary to connect to the cluster and execute data operations.

%package devel
Summary:        Files for development of couchbase applications
Group:          Applications/Databases
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains the libraries and header files that are needed for
developing couchbase client applications.

%prep
%setup -qn %{name}-%{version}

%build
cmake . \
        -DCMAKE_INSTALL_PREFIX="%{_prefix}" \
        -DCMAKE_BUILD_TYPE=RelWithDebInfo \
        -DLIB_INSTALL_DIR=%{_libdir} \
        -DBUILD_SHARED_LIBS=ON

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
ls %{buildroot}%{_libdir}/*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc CONTRIBUTING.md README.markdown RELEASE_NOTES.markdown
%{_bindir}/cbc*
%{_mandir}/man*/cbc*
%{_libdir}/%{name}.so.2*
%{_libdir}/%{name}_libuv.so
%{_libdir}/%{name}_libev.so

%files devel
%{_includedir}/%{name}
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/%{name}.so

%changelog
* Wed May 20 2015 Didier Fabert <didier.fabert@gmail.com> 2.5.0-1
- First Release
