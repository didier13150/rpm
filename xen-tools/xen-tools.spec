Name:           xen-tools
Version:        4.3.1
Release:        1%{?dist}
Summary:        Perl scripts to manage Xen
License:        GPLv2
Group:          Development/Libraries
URL:            http://xen-tools.org/
Source0:        http://xen-tools.org/software/xen-tools/xen-tools-4.3.1.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  perl, perl-podlators
BuildArch:      noarch
AutoReqProv:    0

Requires:       perl(Pod::Usage)
Requires:       perl(Getopt::Long)
Requires:       perl(File::Copy)
Requires:       perl(File::Slurp)
Requires:       perl(File::Temp)
Requires:       perl(File::Path)
Requires:       perl(Text::Template)
Requires:       perl(Digest::MD5)

%description
xen-tools is a collection of simple perl scripts which allow you to easily
create new guest Xen domains upon your Debian GNU/Linux host.

Once installed and configured you can create a new Xen instance in a matter
of minutes. Each new Xen domain will be complete with:
 All networking details setup, with either multiple static IP addresses or DHCP.
 An installation of OpenSSH.
 An arbitrary set of partitions.

Your new instance will be completed by having the user accounts from your
guest system copied over, and you may optionally boot the image as soon as it
has been created.

%prep
%setup -qn %{name}-%{version}

%build
make %{?_smp_mflags}
mkdir -p man
pushd bin
for i in *-*[!y]
do
  # Replace non-ascii character on author's firstname (quick and dirty)
  sed -i -e 's/[S|s]téphane/Stephane/g' $i
  pod2man --release=${version} --official --section=8 $i ../man/$i.8
done
popd
for i in man/*.8
do
  gzip --force -9 $i
done

%install
%{__rm} -rf %{buildroot}

#etc
%{__mkdir_p} %{buildroot}%{_sysconfdir}/bash_completion.d
%{__mkdir_p} %{buildroot}%{_sysconfdir}/xen-tools/skel
%{__mkdir_p} %{buildroot}%{_sysconfdir}/xen-tools/role.d
%{__mkdir_p} %{buildroot}%{_sysconfdir}/xen-tools/partitions.d
%{__install} -m0644 etc/xen-tools.conf %{buildroot}%{_sysconfdir}/xen-tools/
%{__install} -m0644 etc/xm.tmpl %{buildroot}%{_sysconfdir}/xen-tools/
%{__install} -m0644 etc/xm-nfs.tmpl %{buildroot}%{_sysconfdir}/xen-tools/
%{__install} -m0644 partitions/*-* %{buildroot}%{_sysconfdir}/xen-tools/partitions.d/
%{__install} -m0644 misc/xen-tools %{buildroot}%{_sysconfdir}/bash_completion.d/
#if [ -d ${prefix}/etc/xen-tools/hook.d ]; then mv ${prefix}/etc/xen-tools/hook.d/  ${prefix}/etc/xen-tools/hook.d.obsolete ; fi

#bin
%{__mkdir_p} %{buildroot}%{_bindir}
%{__install} -m0755 bin/xen-create-image %{buildroot}%{_bindir}/
%{__install} -m0755 bin/xen-create-nfs %{buildroot}%{_bindir}/
%{__install} -m0755 bin/xt-customize-image %{buildroot}%{_bindir}/
%{__install} -m0755 bin/xt-install-image %{buildroot}%{_bindir}/
%{__install} -m0755 bin/xt-create-xen-config %{buildroot}%{_bindir}/
%{__install} -m0755 bin/xen-delete-image %{buildroot}%{_bindir}/
%{__install} -m0755 bin/xen-list-images %{buildroot}%{_bindir}/
%{__install} -m0755 bin/xen-update-image %{buildroot}%{_bindir}/
%{__install} -m0755 bin/xt-guess-suite-and-mirror %{buildroot}%{_bindir}/

#hooks
%{__cp} roles/* %{buildroot}%{_sysconfdir}/xen-tools/role.d/
%{__mkdir_p} %{buildroot}%{_prefix}/lib/xen-tools/centos-4.d
%{__mkdir_p} %{buildroot}%{_prefix}/lib/xen-tools/centos-5.d
%{__mkdir_p} %{buildroot}%{_prefix}/lib/xen-tools/centos-6.d
%{__mkdir_p} %{buildroot}%{_prefix}/lib/xen-tools/fedora-core-6.d
%{__mkdir_p} %{buildroot}%{_prefix}/lib/xen-tools/
%{__cp} -R hooks/centos-4/*-* %{buildroot}%{_prefix}/lib/xen-tools/centos-4.d/
%{__cp} -R hooks/centos-5/*-* %{buildroot}%{_prefix}/lib/xen-tools/centos-5.d/
%{__cp} -R hooks/centos-6/*-* %{buildroot}%{_prefix}/lib/xen-tools/centos-6.d/
%{__cp} -R hooks/fedora-core-6/*-* %{buildroot}%{_prefix}/lib/xen-tools/fedora-core-6.d/
pushd %{buildroot}%{_prefix}/lib/xen-tools/
for i in {4,5} {7..20}
do
  ln -s fedora-core-6.d fedora-core-$i.d
done
popd
%{__mkdir_p} %{buildroot}%{_prefix}/lib/xen-tools/debian.d
%{__cp} -R hooks/debian/*-* %{buildroot}%{_prefix}/lib/xen-tools/debian.d/
pushd %{buildroot}%{_prefix}/lib/xen-tools/
for i in sarge etch lenny squeeze wheezy sid testing stable
do
  ln -s debian.d $i.d
done
popd
%{__mkdir_p} %{buildroot}%{_prefix}/lib/xen-tools/gentoo.d
%{__cp} -R hooks/gentoo/*-* %{buildroot}%{_prefix}/lib/xen-tools/gentoo.d/
%{__mkdir_p} %{buildroot}%{_prefix}/lib/xen-tools/dapper.d
%{__cp} -R hooks/dapper/*-* %{buildroot}%{_prefix}/lib/xen-tools/dapper.d/
%{__mkdir_p} %{buildroot}%{_prefix}/lib/xen-tools/edgy.d
%{__cp} -R hooks/dapper/*-* %{buildroot}%{_prefix}/lib/xen-tools/edgy.d/
pushd %{buildroot}%{_prefix}/lib/xen-tools/
for i in feisty gutsy hardy
do
  ln -s edgy.d $i.d
done
popd
%{__mkdir_p} %{buildroot}%{_prefix}/lib/xen-tools/intrepid.d
%{__cp} -R hooks/dapper/*-* %{buildroot}%{_prefix}/lib/xen-tools/intrepid.d/
pushd %{buildroot}%{_prefix}/lib/xen-tools/
for i in jaunty
do
  ln -s intrepid.d $i.d
done
popd
%{__mkdir_p} %{buildroot}%{_prefix}/lib/xen-tools/karmic.d
%{__cp} -R hooks/karmic/*-* %{buildroot}%{_prefix}/lib/xen-tools/karmic.d/
pushd %{buildroot}%{_prefix}/lib/xen-tools/
for i in lucid maverick natty oneiric precise quantal
do
  ln -s karmic.d $i.d
done
popd
%{__install} -m0644 hooks/common.sh %{buildroot}%{_prefix}/lib/xen-tools/
%{__cp} -R hooks/common %{buildroot}%{_prefix}/lib/xen-tools/

#libraries
%{__mkdir_p} %{buildroot}%{perl_vendorlib}/Xen/Tools
%{__cp} ./lib/Xen/*.pm %{buildroot}%{perl_vendorlib}/Xen/
%{__cp} ./lib/Xen/Tools/*.pm %{buildroot}%{perl_vendorlib}/Xen/Tools/

#manpages
%{__mkdir_p} %{buildroot}%{_mandir}/man8
%{__cp} man/*.8.gz %{buildroot}%{_mandir}/man8/


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS BUGS ChangeLog KNOWN_BUGS NEWS README SUPPORT TODO
%{_sysconfdir}/bash_completion.d/xen-tools
%{_sysconfdir}/xen-tools
%{_bindir}/xen-*
%{_bindir}/xt-*
%{_prefix}/lib/xen-tools
%{_mandir}/man8
%{perl_vendorlib}/Xen

%changelog
* Fri Oct 11 2013 Didier Fabert <didier.fabert@gmail.com> 4.3.1-1
- First Release