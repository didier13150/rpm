%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7
%global with_systemd 1
%else
%global with_systemd 0
%endif
%define author   ether
%define paduser  etherpad
%define padgroup etherpad

Name:             etherpad-lite
Version:          1.3.0
Release:          1%{?dist}
License:          ASL 2.0
Summary:          Online editor providing collaborative editing in really real-time
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
URL:              http://etherpad.org/
Source0:          https://github.com/%{author}/%{name}/archive/%{version}.tar.gz
Source1:          %{name}.init
Source2:          %{name}.service
Source3:          etherpad-lite.sysconfig
Source4:          settings.json
Group:            Applications/Internet
BuildRoot:        %{_tmppath}/%{name}-%{version}-root
BuildRequires:    openssl-devel
BuildRequires:    mysql-devel
BuildRequires:    postgresql-devel
BuildRequires:    make
BuildRequires:    gcc-c++
BuildRequires:    python
BuildRequires:    gzip
BuildRequires:    git-core
BuildRequires:    curl
BuildRequires:    gcc-c++
BuildRequires:    nodejs
BuildRequires:    npm
%if %{with_systemd}
BuildRequires:    systemd
%endif
Requires:         git-core
Requires:         curl
Requires:         python
Requires:         nodejs
Requires:         npm
%if %{with_systemd}
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
# For triggerun
Requires(post):   systemd-sysv
%else
Requires:         initscripts
Requires:         libevent
Requires(post):   /sbin/chkconfig
Requires(preun):  /sbin/chkconfig, /sbin/service
Requires(postun): /sbin/service
%endif

%description
Etherpad allows you to edit documents collaboratively in real-time, much like a
live multi player editor that runs in your browser. Write articles, press 
releases, to-do lists, etc. together with your friends, fellow students or 
colleagues, all working on the same document at the same time.

%package apidoc
Group:            Documentation
Summary:          %{name} API docs
Requires:         %{name} = %{version}-%{release}

%description apidoc
API documentation for etherpad-lite

%prep
%setup -qn %{name}-%{version}

%build 
make %{?_smp_mflags}
bin/installDeps.sh
%{__rm} -f start.bat

%install
rm -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_sysconfdir}/%{name}
%{__mkdir_p} %{buildroot}%{_sysconfdir}/sysconfig
%{__mkdir_p} %{buildroot}%{_docdir}/%{name}/apidoc
%{__mkdir_p} %{buildroot}%{_localstatedir}/lib/%{name}
%{__mkdir_p} %{buildroot}%{_localstatedir}/log/%{name}
for dir in bin doc src tests tools node_modules out var
do
    %{__cp} -r ${dir} %{buildroot}%{_localstatedir}/lib/%{name}/
done
%{__cp} %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%{__cp} %{SOURCE4} %{buildroot}%{_sysconfdir}/%{name}/settings.json
pushd %{buildroot}%{_localstatedir}/lib/%{name}
ln -s %{_sysconfdir}/%{name}/settings.json
popd
%{__cp} -r out/doc/* %{buildroot}%{_docdir}/%{name}/
%if %{with_systemd}
# Unit file
%{__mkdir_p} %{buildroot}%{_unitdir}
install -Dp -m0644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service
%else
# Init script
%{__mkdir_p} %{buildroot}%{_initrddir}
install -Dp -m0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
%endif
touch %{_localstatedir}/log/%{name}/%{name}.log

%clean
rm -rf %{buildroot}

%pre
if ! /usr/bin/id %{paduser} &>/dev/null; then
    /usr/sbin/useradd -r -d %{_localstatedir}/lib/%{name} -s /bin/nologin -c "Etherpad user" %{paduser} || \
        echo "Unexpected error when adding user \"pad\"."
fi
if ! /usr/bin/getent group %{padgroup} &>/dev/null; then
    /usr/sbin/groupadd %{padgroup} &>/dev/null || \
        echo "Unexpected error when adding group \"%{padgroup}\"."
fi

%postun
%if 0%{?systemd_postun_with_restart:1}
%systemd_postun_with_restart %{name}.service
%else
%if %{with_systemd}
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ]; then
# Package upgrade, not uninstall
    /bin/systemctl try-restart %{name}.service >/dev/null 2>&1 || :
fi
%else
if [ "$1" -ge 1 ]; then
    /sbin/service %{name} restart > /dev/null 2>&1
fi
exit 0
%endif
%endif
if [ $1 -eq 0 ]; then
    if [ /usr/bin/id %{paduser} &>/dev/null ]; then
        /usr/sbin/userdel %{paduser} || echo "User \"%{paduser}\" could not be deleted."
    fi
    if ! /usr/bin/getent group %{padgroup} &>/dev/null; then
        /usr/sbin/groupdel %{padgroup} || echo "Group \"%{padgroup}\" could not be deleted."
    fi
fi

%post
%if 0%{?systemd_post:1}
%systemd_post %{name}.service
%else
if [ $1 = 1 ]; then
# Initial installation
%if %{with_systemd}
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
%else
    /sbin/chkconfig --add %{name}
%endif
fi
%endif

%preun
%if 0%{?systemd_preun:1}
%systemd_preun %{name}.service
%else
if [ "$1" = 0 ] ; then
# Package removal, not upgrade
%if %{with_systemd}
    /bin/systemctl --no-reload disable %{name}.service >/dev/null 2>&1 || :
    /bin/systemctl stop %{name}.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name} stop > /dev/null 2>&1
    /sbin/chkconfig --del %{name}
%endif
fi
exit 0
%endif

%triggerun -- %{name}
%if %{with_systemd}
if [ -f /etc/rc.d/init.d/%{name} ]; then
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply memcached
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save %{name} >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del %{name} >/dev/null 2>&1 || :
/bin/systemctl try-restart %{name}.service >/dev/null 2>&1 || :
fi
%endif

%files
%defattr(-,root,root)
%doc CHANGELOG.md CONTRIBUTING.md README.md
%config(noreplace) %{_sysconfdir}/%{name}/settings.json
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_docdir}/%{name}
%exclude %{_docdir}/%{name}/api
%defattr(-,%{paduser},%{padgroup})
%{_localstatedir}/lib/%{name}
%{_localstatedir}/log/%{name}

%if %{with_systemd}
%{_unitdir}/%{name}.service
%else
%attr(0755,root,root) %{_initrddir}/%{name}
%endif

%files apidoc
%defattr(-,root,root)
%{_docdir}/%{name}/api

%changelog
* Thu Feb 06 2014 Didier Fabert <didier.fabert@gmail.com> 1.3.0-1
- First release
