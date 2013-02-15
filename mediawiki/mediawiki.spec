%define majorver 1.20
Name:           mediawiki
Version:        %{majorver}.2
Release:        1%{?dist}
License:        GPLv2+
Group:          Development/Tools
URL:            http://www.mediawiki.org/
Summary:        A wiki engine
Source0:        http://download.wikimedia.org/mediawiki/%{majorver}/mediawiki-%{version}.tar.gz
Source1:        mediawiki.conf
Source10:       Cite.tgz
Source11:       SyntaxHighlight_GeSHi.tgz
Source12:       PdfExport.tgz
Source13:       Mpdf.tgz
Source14:       CategoryTree.tgz
Source15:       Math.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
# to make sure the "apache" group is created before mediawiki is installed
Requires(pre):  httpd
Requires:       php-common >= 5, php-xml
Conflicts:      php-common = 5.3.1
Requires:       php-mysql, php-pgsql
Requires:       diffutils, ImageMagick, php-gd

%description
MediaWiki is the software used for Wikipedia and the other Wikimedia
Foundation websites. Compared to other wikis, it has an excellent
range of features and support for high-traffic websites using multiple
servers

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

%prep
%setup -q

%build

%install
rm -rf %{buildroot}

# move away the documentation to the final folder.
mkdir -p %{buildroot}%{_defaultdocdir}/%{name}-%{version}
mv -f COPYING FAQ HISTORY README RELEASE-NOTES* UPGRADE CREDITS INSTALL docs \
  %{buildroot}%{_defaultdocdir}/%{name}-%{version}/

# now copy the rest to the buildroot.
mkdir -p %{buildroot}%{_localstatedir}/www/wiki
cp -a * %{buildroot}%{_localstatedir}/www/wiki

# remove unneeded parts
rm -fr %{buildroot}%{_localstatedir}/www/wiki/{t,test,tests}
rm -fr %{buildroot}%{_localstatedir}/www/wiki/includes/zhtable
find %{buildroot}%{_localstatedir}/www/wiki/ \
  \( -name .htaccess -or -name \*.cmi \) \
  | xargs -r rm

# fix permissions
chmod +x %{buildroot}%{_localstatedir}/www/wiki/bin/*
find %{buildroot}%{_localstatedir}/www/wiki -name \*.pl | xargs -r chmod +x

# remove version control/patch files
find %{buildroot} -name .svnignore | xargs -r rm
find %{buildroot} -name \*.commoncode | xargs -r rm

mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d/
install -p -m 0644 %{SOURCE1} \
  %{buildroot}%{_sysconfdir}/httpd/conf.d/mediawiki.conf

# Extract extensions
tar -xzf %{SOURCE10} -C %{buildroot}%{_localstatedir}/www/wiki/extensions/
tar -xzf %{SOURCE11} -C %{buildroot}%{_localstatedir}/www/wiki/extensions/
tar -xzf %{SOURCE12} -C %{buildroot}%{_localstatedir}/www/wiki/extensions/
tar -xzf %{SOURCE13} -C %{buildroot}%{_localstatedir}/www/wiki/extensions/
tar -xzf %{SOURCE14} -C %{buildroot}%{_localstatedir}/www/wiki/extensions/
tar -xzf %{SOURCE15} -C %{buildroot}%{_localstatedir}/www/wiki/extensions/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_defaultdocdir}/%{name}-%{version}
%{_localstatedir}/www/wiki
%attr(-,apache,apache) %dir %{_localstatedir}/www/wiki/mw-config
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mediawiki.conf
%exclude %{_localstatedir}/www/wiki/extensions/Cite
%exclude %{_localstatedir}/www/wiki/extensions/SyntaxHighlight_GeSHi
%exclude %{_localstatedir}/www/wiki/extensions/PdfExport
%exclude %{_localstatedir}/www/wiki/extensions/Mpdf
%exclude %{_localstatedir}/www/wiki/extensions/CategoryTree
%exclude %{_localstatedir}/www/wiki/extensions/Math

#Cite SyntaxHighlight_GeSHi PdfExport Mpdf CategoryTree Math
%files Cite
%{_localstatedir}/www/wiki/extensions/Cite

%files SyntaxHighlight_GeSHi
%{_localstatedir}/www/wiki/extensions/SyntaxHighlight_GeSHi

%files PdfExport
%{_localstatedir}/www/wiki/extensions/PdfExport


%files Mpdf
%{_localstatedir}/www/wiki/extensions/Mpdf


%files CategoryTree
%{_localstatedir}/www/wiki/extensions/CategoryTree


%files Math
%{_localstatedir}/www/wiki/extensions/Math

%changelog
* Fri Feb 15 2013 Didier Fabert <didier.fabert@gmail.com> - 1.20.2-1
- Update to 1.20.2
- No farm release

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16.5-61
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16.5-60
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

* Tue Feb 17 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.10.3-37
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

