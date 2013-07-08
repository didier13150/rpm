%define majorver 1.21
%global wiki_ext_path %{_datadir}/mediawiki/extensions
Name:           mediawiki
Version:        %{majorver}.1
Release:        1%{?dist}
License:        GPLv2+
Group:          Development/Tools
URL:            http://www.mediawiki.org/
Summary:        A wiki engine
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:        http://download.wikimedia.org/mediawiki/%{majorver}/mediawiki-%{version}.tar.gz
Source1:        mediawiki.conf
Source2:        README.RPM
Source3:        mw-createinstance.in
Source4:        mw-updateallinstances.in
Source10:       https://gerrit.wikimedia.org/r/p/mediawiki/extensions/Cite.tgz
Source11:       https://gerrit.wikimedia.org/r/p/mediawiki/extensions/SyntaxHighlight_GeSHi.tgz
Source12:       https://gerrit.wikimedia.org/r/p/mediawiki/extensions/PdfExport.tgz
Source13:       https://gerrit.wikimedia.org/r/p/mediawiki/extensions/Mpdf.tgz
Source14:       https://gerrit.wikimedia.org/r/p/mediawiki/extensions/CategoryTree.tgz
Source15:       https://gerrit.wikimedia.org/r/p/mediawiki/extensions/Math.tgz
Source16:       Linux.tag.php
Source17:       CalcBitrate.js
Source18:       CalcBitrate.php
BuildArch:      noarch
# to make sure the "apache" group is created before mediawiki is installed
Requires(pre):  httpd
Requires:       php-common >= 5, php-xml
Conflicts:      php-common = 5.3.1
Requires:       php-mysql, php-pgsql
Requires:       diffutils, ImageMagick, php-gd

Provides:       mediawiki-math = %{version}-%{release}
Provides:       mediawiki-nomath = %{version}-%{release}
Provides:       mediawiki116 = %{version}-%{release}

Obsoletes:      mediawiki-math < 1.16.5-62
Obsoletes:      mediawiki-nomath < 1.16.5-62
Obsoletes:      mediawiki116 < 1.16.0-9


%description
MediaWiki is the software used for Wikipedia and the other Wikimedia
Foundation websites. Compared to other wikis, it has an excellent
range of features and support for high-traffic websites using multiple
servers

This package supports wiki farms. Read the instructions for creating wiki instances under %{_defaultdocdir}/%{name}-%{version}/README.RPM.
Remember to remove the config dir after completing the configuration.

%package Cite
Requires:       %{name}
Summary:        Cite mediawiki extension
Group:          Development/Tools

%description Cite
Cite is an extension which allows a user to create footnotes. Cite includes
several extensions which can be installed independently and operate
independently of each other.

%package SyntaxHighlight_GeSHi
Requires:       %{name}
Summary:        SyntaxHighlight_GeSHi mediawiki extension
Group:          Development/Tools

%description SyntaxHighlight_GeSHi
The Extension:SyntaxHighlight GeSHi tag displays formatted source code with
the <syntaxhighlight> tag.

This extension also adds coloring according to the code language settings.
Like the <pre> tags and the <poem> tags, the tags shows the coding exactly as
it was typed, preserving white space.

This extension also can create line numbers.

%package PdfExport
Requires:       %{name}
Summary:        PdfExport mediawiki extension
Group:          Development/Tools

%description PdfExport
This extension lets you view wiki pages as PDF.

%package Mpdf
Requires:       %{name}
Summary:        Mpdf mediawiki extension
Group:          Development/Tools

%description Mpdf
This extension lets you export printable version of wiki page as PDF file.
For conversion uses mPDF PHP class

%package CategoryTree
Requires:       %{name}
Summary:        CategoryTree mediawiki extension
Group:          Development/Tools

%description CategoryTree
The CategoryTree extension provides a dynamic view of the wiki's category
structure as a tree. It uses AJAX to load parts of the tree on demand.

%package Math
Requires:       %{name}
Summary:        Math mediawiki extension
Group:          Development/Tools
Requires:       LabPlot

%description Math
Math extension provides support for rendering mathematical formulas on-wiki
via texvc

%package CustomTag
Requires:       %{name}
Summary:        CustomTag mediawiki extension
Group:          Development/Tools

%description CustomTag
CustomTag extension support custom tags to modify display:
<path>, <package>, <app>, <class>

%package CalcBitrate
Requires:       %{name}
Summary:        CalcBitrate mediawiki extension
Group:          Development/Tools

%description CalcBitrate
CalcBitrate extension provides a bitrate calculator with the simple tag
"<calcBitrate/>"

%prep
%setup -q

%build

%install
rm -rf %{buildroot}

# move away the documentation to the final folder.
mkdir -p %{buildroot}%{_defaultdocdir}/%{name}-%{version}
cp -rp COPYING FAQ HISTORY README RELEASE-NOTES* UPGRADE CREDITS INSTALL docs \
  %{buildroot}%{_defaultdocdir}/%{name}-%{version}/

# now copy the rest to the buildroot.
mkdir -p %{buildroot}%{_datadir}/mediawiki
cp -a * %{buildroot}%{_datadir}/mediawiki/

# remove unneeded parts
rm -fr %{buildroot}%{_datadir}/mediawiki/{t,test,tests}
rm -fr %{buildroot}%{_datadir}/mediawiki/includes/zhtable
find %{buildroot}%{_datadir}/mediawiki/ \
  \( -name .htaccess -or -name \*.cmi \) \
  | xargs -r rm

# fix permissions
find %{buildroot}%{_datadir}/mediawiki -name \*.pl | xargs -r chmod +x

# remove version control/patch files
find %{buildroot} -name .svnignore | xargs -r rm
find %{buildroot} -name \*.commoncode | xargs -r rm

# placeholder for a default instance
mkdir -p %{buildroot}%{_localstatedir}/www/wiki

mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d/
install -p -m 0644 %{SOURCE1} \
  %{buildroot}%{_sysconfdir}/httpd/conf.d/mediawiki.conf

# tools for keeping mediawiki instances current
mkdir -p %{buildroot}%{_sbindir}
sed -e's,@datadir@,%{_datadir},g' -e's,@sysconfdir@,%{_sysconfdir},g' \
  < %{SOURCE3} > %{buildroot}%{_sbindir}/mw-createinstance
sed -e's,@datadir@,%{_datadir},g' -e's,@sysconfdir@,%{_sysconfdir},g' \
  < %{SOURCE4} > %{buildroot}%{_sbindir}/mw-updateallinstances
chmod 0755 %{buildroot}%{_sbindir}/mw-*
mkdir %{buildroot}%{_sysconfdir}/mediawiki
echo /var/www/wiki > %{buildroot}%{_sysconfdir}/mediawiki/instances

# Extract extensions
tar -xzf %{SOURCE10} -C %{buildroot}%{wiki_ext_path}/
tar -xzf %{SOURCE11} -C %{buildroot}%{wiki_ext_path}/
tar -xzf %{SOURCE12} -C %{buildroot}%{wiki_ext_path}/
tar -xzf %{SOURCE13} -C %{buildroot}%{wiki_ext_path}/
tar -xzf %{SOURCE14} -C %{buildroot}%{wiki_ext_path}/
tar -xzf %{SOURCE15} -C %{buildroot}%{wiki_ext_path}/
%{__mkdir_p} %{buildroot}%{wiki_ext_path}/CalcBitrate
%{__mkdir_p} %{buildroot}%{wiki_ext_path}/CustomTag
%{__cp} %{SOURCE16} %{buildroot}%{wiki_ext_path}/CustomTag/
%{__cp} %{SOURCE17} %{buildroot}%{wiki_ext_path}/CalcBitrate/
%{__cp} %{SOURCE18} %{buildroot}%{wiki_ext_path}/CalcBitrate/

%post
%{_sbindir}/mw-updateallinstances >> /var/log/mediawiki-updates.log 2>&1 || :

%clean
rm -rf %{buildroot}

%files
%doc COPYING FAQ HISTORY README RELEASE-NOTES-1.21 UPGRADE CREDITS INSTALL docs
%{_datadir}/mediawiki
%attr(-,apache,apache) %{_datadir}/mediawiki/mw-config
%{_localstatedir}/www/wiki
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mediawiki.conf
%dir %{_sysconfdir}/mediawiki
%config(noreplace) %{_sysconfdir}/mediawiki/instances
%{_sbindir}/mw-createinstance
%{_sbindir}/mw-updateallinstances
%exclude %{wiki_ext_path}/Cite
%exclude %{wiki_ext_path}/SyntaxHighlight_GeSHi
%exclude %{wiki_ext_path}/PdfExport
%exclude %{wiki_ext_path}/Mpdf
%exclude %{wiki_ext_path}/CategoryTree
%exclude %{wiki_ext_path}/Math
%exclude %{wiki_ext_path}/CalcBitrate
%exclude %{wiki_ext_path}/CustomTag

#Cite SyntaxHighlight_GeSHi PdfExport Mpdf CategoryTree Math
%files Cite
%{wiki_ext_path}/Cite

%files SyntaxHighlight_GeSHi
%{wiki_ext_path}/SyntaxHighlight_GeSHi

%files PdfExport
%{wiki_ext_path}/PdfExport

%files Mpdf
%{wiki_ext_path}/Mpdf

%files CategoryTree
%{wiki_ext_path}/CategoryTree

%files Math
%{wiki_ext_path}/Math

%files CalcBitrate
%{wiki_ext_path}/CalcBitrate

%files CustomTag
%{wiki_ext_path}/CustomTag


%changelog
* Mon Jun 03 2013 Michael Cronenworth <mike@cchtml.com> - 1.21.1-1
- New upstream release.

* Tue May 28 2013 Michael Cronenworth <mike@cchtml.com> - 1.21.0-1
- New upstream release.

* Tue May 07 2013 Michael Cronenworth <mike@cchtml.com> - 1.20.5-1
- New upstream release.
- Obsolete mediawiki116 package.

* Wed Apr 17 2013 Michael Cronenworth <mike@cchtml.com> - 1.20.4-1
- New upstream release.

* Thu Apr 11 2013 Michael Cronenworth <mike@cchtml.com> - 1.20.3-3
- Update mw-* scripts. (#926899)

* Tue Mar 12 2013 Michael Cronenworth <mike@cchtml.com> - 1.20.3-2
- Update mw-createinstance for new access points.

* Mon Mar  4 2013 Michael Cronenworth <mike@cchtml.com> - 1.20.3-1
- New upstream release.

* Thu Feb 28 2013 Michael Cronenworth <mike@cchtml.com> - 1.20.2-2
- Fix upgrade path.

* Wed Feb 27 2013 Michael Cronenworth <mike@cchtml.com> - 1.19.3-1
- New upstream release.

* Fri Feb 15 2013 Didier Fabert <didier.fabert@gmail.com> - 1.20.2-1
- Update to 1.20.2
- No farm release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16.5-62
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16.5-61
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun May  8 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.16.5-59
- Update to 1.16.5.

* Fri Apr 22 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.16.4-58
- texvc was being accidentially wiped out before packaging it.

* Sat Apr 16 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.16.4-57
- Update to 1.16.4.

* Sun Apr  3 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.16.2-56
- Update to 1.16.2.
- Fixes RH bugs #614065, #644325, #682281, #662402
- Enable suggestions while typing in search boxes by default.
- Add some basic mediawiki management scripts.

* Fri Sep 10 2010 Nick Bebout <nb@fedoraproject.org> - 1.15.4-55
- Mark mediawiki.conf as config(noreplace) (RH bug #614396).

* Mon Jul  5 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.15.4-54
- Update to 1.5.14 (Fixes CVE-2010-1647 CVE-2010-1648).
- Change BR php to php-common (RH bug #549822).

* Wed Apr  7 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.15.3-53
- Update to 1.15.3 (Fixes login CSRF vulnerability).

* Wed Mar 31 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.15.2-51
- Update to 1.15.2 (Fixes CSS validation issue and data leakage
  vulnerability).

* Fri Jul 24 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.15.1-50
- Add a README.RPM and a sample apache mediawiki.conf file.

* Thu Jul 23 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.15.1-49
- All (runtime) dependencies from mediawiki need to move to
  mediawiki-nomath.

* Mon Jul 13 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.15.1-48
- Update to 1.15.1 (Fixes XSS vulnerability).

* Sat Jul 11 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.15.0-47
- Fix api.php breakage.

* Sat Jun 13 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.15.0-46
- Update to 1.15.0.

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Sat Feb 28 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.14.0-45
- Update to 1.14.0.

* Sun Feb 22 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.13.4-44
- Split package up, so some users can decide to not install math
  support (results in smaller installs), see RH bug #485447.

* Wed Feb 18 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.13.4-43
- Update to 1.13.4, closes RH bug #485728.

* Tue Dec 23 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.13.3-42
- Update to 1.13.3, closes RH bug #476621 (CVE-2008-5249,
  CVE-2008-5250, CVE-2008-5252 and CVE-2008-5687, CVE-2008-5688)

* Sun Oct  5 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.13.2-41
- Update to 1.13.2.

* Sun Aug 24 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.13.0-40
- Use consistently Patch0 and %%patch0.

* Sat Aug 16 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.13.0-39
- Update to 1.13.0.

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.10.4-40
- fix license tag

* Tue Mar  4 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.10.4-38
- Update to 1.10.4.

* Sun Feb 17 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.10.3-37
- Update to 1.10.3.
- Fixes CVE-2008-0460 (bug #430286).

* Wed May  9 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.10.0-35
- Update to 1.10.0.

* Thu Feb 22 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.9.3-34
- Update to 1.9.4.

* Mon Feb  5 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.9.2-33
- Update to 1.9.2.

* Fri Feb  2 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.9.1-32
- Fix permissions.
- Remove some parts not needed at runtime anymore.

* Thu Feb  1 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.9.1-31
- Update to 1.9.1.

* Sat Oct 14 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.8.2-28
- Update to 1.8.2.

* Wed Oct 11 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.8.1-27
- Update to 1.8.1.
- Update to 1.8.0.

* Mon Jul 10 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.7.1.

* Wed Jun  7 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.6.7.

* Fri May 26 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.6.6.

* Thu Apr 13 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.6.3.

* Sat Apr  8 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.6.2.

* Fri Apr  7 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.6.1.

* Mon Apr  3 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.5.8.

* Thu Mar  2 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.5.7.

* Thu Jan 19 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.5.6.

* Fri Jan  6 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.5.5.

* Sun Dec  4 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.5.3.

* Fri Nov  4 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.5.2.

* Mon Oct 31 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.5.1.

* Thu Oct  6 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.5.0.

* Fri Sep  2 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.5rc4.

* Sun Jul 31 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.5beta4.

* Fri Jul  8 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.5beta3.

* Tue Jul  5 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.5beta2.

* Sun Jul  3 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Initial build.

