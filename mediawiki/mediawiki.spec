%define majorver 1.26
%global wiki_path %{_datadir}/mediawiki
%global wiki_ext_path %{wiki_path}/extensions
%global remove_bundle 0
%if 0%{?fedora} >= 23
%global remove_bundle 1
%endif
Name:      mediawiki
Version:   %{majorver}.1
Release:   2%{?dist}
License:   GPLv2+
Group:     Development/Tools
URL:       http://www.mediawiki.org/
Summary:   A wiki engine
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:   http://download.wikimedia.org/mediawiki/%{majorver}/%{name}-%{version}.tar.gz
Source1:   mediawiki.conf
Source2:   README.RPM
Source3:   mw-createinstance.in
Source4:   mw-updateallinstances.in
BuildArch: noarch

BuildRequires: djvulibre
BuildRequires: php-cli
BuildRequires: php-gd
BuildRequires: php-intl
BuildRequires: php-pdo
BuildRequires: php-pecl-xhprof
BuildRequires: php-phpunit-PHPUnit
BuildRequires: php-theseer-autoload
BuildRequires: php-composer(cssjanus/cssjanus) >= 1.1.1
#BuildRequires: php-composer(leafo/lessphp) >= 0.5.0
BuildRequires: php-composer(liuggio/statsd-php-client) >= 1.0.12
BuildRequires: php-composer(mediawiki/at-ease) >= 1.1.0
BuildRequires: php-composer(monolog/monolog) >= 1.14.0
BuildRequires: php-composer(oojs/oojs-ui) >= 0.11.3
BuildRequires: php-composer(psr/log) >= 1.0.0
BuildRequires: php-composer(wikimedia/assert) >= 0.2.2
BuildRequires: php-composer(wikimedia/avro) >= 1.7.7
BuildRequires: php-composer(wikimedia/cdb) >= 1.0.1
BuildRequires: php-composer(wikimedia/ip-set) >= 0
BuildRequires: php-composer(wikimedia/utfnormal) >= 1.0.2
BuildRequires: php-composer(zordius/lightncandy) >= 0.22

Requires: httpd
Requires: php(httpd)
Requires: php(language) >= 5.3.3
Requires: php-gd
Requires: php-pecl-jsonc
Requires: php-xml
Requires: diffutils, ImageMagick
Requires: php-composer(cssjanus/cssjanus) >= 1.1.1
#Requires: php-composer(leafo/lessphp) >= 0.5.0
Requires: php-composer(liuggio/statsd-php-client) >= 1.0.12
Requires: php-composer(mediawiki/at-ease) >= 1.1.0
Requires: php-composer(monolog/monolog) >= 1.14.0
Requires: php-composer(oojs/oojs-ui) >= 0.11.3
Requires: php-composer(psr/log) >= 1.0.0
Requires: php-composer(symfony/process) >= 2.5.0
Requires: php-composer(wikimedia/assert) >= 0.2.2
Requires: php-composer(wikimedia/avro) >= 1.7.7
Requires: php-composer(wikimedia/cdb) >= 1.0.1
Requires: php-composer(wikimedia/ip-set) >= 0
Requires: php-composer(wikimedia/utfnormal) >= 1.0.2
Requires: php-composer(zordius/lightncandy) >= 0.22
Requires: php-mysql, php-pgsql

# Update script call command-line php
Requires(post): php-cli

Provides:       mediawiki-math = %{version}-%{release}
Provides:       mediawiki-nomath = %{version}-%{release}
Provides:       mediawiki116 = %{version}-%{release}
Provides:       mediawiki-Cite = %{version}-%{release}
Provides:       mediawiki-ConfirmEdit = %{version}-%{release}
Provides:       mediawiki-Gadgets = %{version}-%{release}
Provides:       mediawiki-ImageMap = %{version}-%{release}
Provides:       mediawiki-InputBox = %{version}-%{release}
Provides:       mediawiki-Interwiki = %{version}-%{release}
Provides:       mediawiki-LocalisationUpdate = %{version}-%{release}
Provides:       mediawiki-Nuke = %{version}-%{release}
Provides:       mediawiki-ParserFunctions = %{version}-%{release}
Provides:       mediawiki-Poem = %{version}-%{release}
Provides:       mediawiki-Renameuser = %{version}-%{release}
Provides:       mediawiki-SpamBlacklist = %{version}-%{release}
Provides:       mediawiki-SyntaxHighlight_GeSHi = %{version}-%{release}
Provides:       mediawiki-TitleBlacklist = %{version}-%{release}
Provides:       mediawiki-Vector = %{version}-%{release}
Provides:       mediawiki-WikiEditor = %{version}-%{release}
Provides:       mediawiki-CiteThisPage = %{version}-%{release}
Provides:       mediawiki-PdfHandler = %{version}-%{release}

Obsoletes:      mediawiki-math < 1.16.5-62
Obsoletes:      mediawiki-nomath < 1.16.5-62
Obsoletes:      mediawiki116 < 1.16.0-9
Obsoletes:      mediawiki-Cite < %{version}-%{release}
Obsoletes:      mediawiki-ConfirmEdit < %{version}-%{release}
Obsoletes:      mediawiki-Gadgets < %{version}-%{release}
Obsoletes:      mediawiki-ImageMap < %{version}-%{release}
Obsoletes:      mediawiki-InputBox < %{version}-%{release}
Obsoletes:      mediawiki-Interwiki < %{version}-%{release}
Obsoletes:      mediawiki-LocalisationUpdate < %{version}-%{release}
Obsoletes:      mediawiki-Nuke < %{version}-%{release}
Obsoletes:      mediawiki-ParserFunctions < %{version}-%{release}
Obsoletes:      mediawiki-Poem < %{version}-%{release}
Obsoletes:      mediawiki-Renameuser < %{version}-%{release}
Obsoletes:      mediawiki-SpamBlacklist < %{version}-%{release}
Obsoletes:      mediawiki-SyntaxHighlight_GeSHi < %{version}-%{release}
Obsoletes:      mediawiki-TitleBlacklist < %{version}-%{release}
Obsoletes:      mediawiki-Vector < %{version}-%{release}
Obsoletes:      mediawiki-WikiEditor < %{version}-%{release}
Obsoletes:      mediawiki-CiteThisPage < %{version}-%{release}
Obsoletes:      mediawiki-PdfHandler < %{version}-%{release}

%description
MediaWiki is the software used for Wikipedia and the other Wikimedia
Foundation websites. Compared to other wikis, it has an excellent
range of features and support for high-traffic websites using multiple
servers

This package supports wiki farms. Read the instructions for creating wiki
instances under %{_defaultdocdir}/%{name}-%{version}/README.RPM.
Remember to remove the config dir after completing the configuration.


%prep
%setup -q
%if %{remove_bundle}
# Remove bundled PHP libraries in order to use system versions
rm -rf vendor/composer/*php
rm -rf vendor/composer/*json
rm -rf vendor/composer/LICENSE
rm -rf vendor/cssjanus
rm -rf vendor/liuggio
rm -rf vendor/mediawiki/at-ease
rm -rf vendor/monolog
rm -rf vendor/oojs
#rm -rf vendor/oyejorge
rm -rf vendor/psr
rm -rf vendor/wikimedia/assert
rm -rf vendor/wikimedia/avro
rm -rf vendor/wikimedia/cdb
rm -rf vendor/wikimedia/composer-merge-plugin
rm -rf vendor/wikimedia/ip-set
rm -rf vendor/wikimedia/utfnormal
rm -rf vendor/zordius
ln -s %{_datadir}/php/cssjanus vendor/cssjanus-shared
ln -s %{_datadir}/php/Liuggio vendor/liuggio-shared
ln -s %{_datadir}/php/MediaWiki vendor/mediawiki/at-ease-shared
ln -s %{_datadir}/php/Monolog vendor/monolog-shared
ln -s %{_datadir}/php/OOUI vendor/oojs-shared
#ln -s %{_datadir}/php/lessphp vendor/oyejorge-shared
ln -s %{_datadir}/php/Psr vendor/psr-shared
ln -s %{_datadir}/php/Wikimedia vendor/wikimedia/assert-shared
ln -s %{_datadir}/php/avro vendor/wikimedia/avro-shared
ln -s %{_datadir}/php/Cdb vendor/wikimedia/cdb-shared
ln -s %{_datadir}/php/IPSet vendor/wikimedia/ip-set-shared
ln -s %{_datadir}/php/UtfNormal vendor/wikimedia/utfnormal-shared
ln -s %{_datadir}/php/zordius vendor/zordius-shared
%endif

%build
%if %{remove_bundle}
phpab --follow --output vendor/autoload.php vendor
echo "require dirname(dirname(__FILE__)) . '/vendor/mediawiki/at-ease-shared/at-ease/Functions.php';" >> vendor/autoload.php
%endif


%install
rm -rf %{buildroot}

# copy additional documentation
cp -p %{SOURCE2} .

# now copy the rest to the buildroot.
mkdir -p %{buildroot}%{_datadir}/mediawiki
cp -a * %{buildroot}%{_datadir}/mediawiki/

# remove unneeded parts
rm -fr %{buildroot}%{_datadir}/mediawiki/{t,test,tests}
rm -fr %{buildroot}%{_datadir}/mediawiki/includes/zhtable
find %{buildroot}%{_datadir}/mediawiki/ \
  \( -name .htaccess -or -name \*.cmi \) \
  -delete

# fix permissions
find %{buildroot}%{_datadir}/mediawiki -name \*.pl | xargs -r chmod +x
find %{buildroot}%{_datadir}/mediawiki -name \*.py | xargs -r chmod +x
chmod +x %{buildroot}%{_datadir}/mediawiki/maintenance/hiphop/run-server
chmod +x %{buildroot}%{_datadir}/mediawiki/maintenance/storage/make-blobs
chmod +x %{buildroot}%{_datadir}/mediawiki/includes/limit.sh
chmod +x %{buildroot}%{_datadir}/mediawiki/extensions/ConfirmEdit/captcha.py

# remove version control/patch files
find %{buildroot} -name .svnignore -delete
find %{buildroot} -name \*.commoncode -delete
find %{buildroot} -name .gitreview -delete
find %{buildroot} -name .gitignore -delete
find %{buildroot} -name .gitmodules -delete
find %{buildroot} -name .jshintignore -delete
find %{buildroot} -name .jshintrc -delete

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

# Remove vcs directories
find %{buildroot}%{wiki_path} -type d -name '.git*' -exec rm -rf {} \; || :

%check
# Database tests currently fail on the 1.26 release series
php maintenance/install.php \
    --dbtype sqlite \
    --dbname mediawiki-test \
    --dbpath /tmp \
    --pass test123 \
    Test test
cd tests/phpunit
make databaseless


%post
%{_sbindir}/mw-updateallinstances >> /var/log/mediawiki-updates.log 2>&1 || :

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING FAQ HISTORY README README.RPM RELEASE-NOTES* UPGRADE CREDITS docs
%{_datadir}/mediawiki
%attr(-,apache,apache) %{_datadir}/mediawiki/mw-config
%{_localstatedir}/www/wiki
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mediawiki.conf
%dir %{_sysconfdir}/mediawiki
%config(noreplace) %{_sysconfdir}/mediawiki/instances
%{_sbindir}/mw-createinstance
%{_sbindir}/mw-updateallinstances


%changelog
* Mon Jan 11 2016 Didier Fabert <didier.fabert@gmail.com> - 1.26.2-2
- Move sub-packages to specific packages.

* Mon Jan 11 2016 Didier Fabert <didier.fabert@gmail.com> - 1.26.2-1
- New upstream release.

* Thu Jun 04 2015 Didier Fabert <didier.fabert@gmail.com> - 1.25.1-2
- Add missing vendor directory for mediawiki

* Wed May 27 2015 Didier Fabert <didier.fabert@gmail.com> - 1.25.1-1
- New upstream release.

* Thu Apr 16 2015 Didier Fabert <didier.fabert@gmail.com> - 1.24.2-1
- New upstream release.

* Mon Jan 19 2015 Didier Fabert <didier.fabert@gmail.com> - 1.24.1-1
- New upstream release.

* Mon Dec 15 2014 Didier Fabert <didier.fabert@gmail.com> - 1.24.0-1
- New upstream release.

* Tue Sep 09 2014 Didier Fabert <didier.fabert@gmail.com> - 1.23.3-1
- New upstream release.
- Add Widgets extension

* Thu Jun 26 2014 Didier Fabert <didier.fabert@gmail.com> - 1.23.1-1
- New upstream release.

* Fri Jun 13 2014 Didier Fabert <didier.fabert@gmail.com> - 1.23.0-1
- New upstream release.

* Fri May 16 2014 Didier Fabert <didier.fabert@gmail.com> - 1.23.0rc0-0.2
- Add ConfirmAccount extension

* Fri May 16 2014 Didier Fabert <didier.fabert@gmail.com> - 1.23.0rc0-0.1
- New upstream release.
- Add BetaFeatures extension

* Thu May 15 2014 Didier Fabert <didier.fabert@gmail.com> - 1.22.6-2
- Add MultimediaViewer extension
- Add CommonsMetadata extension

* Fri Apr 25 2014 Didier Fabert <didier.fabert@gmail.com> - 1.22.6-1
- New upstream release.

* Thu Apr 03 2014 Didier Fabert <didier.fabert@gmail.com> - 1.22.5-1
- New upstream release.

* Fri Feb 28 2014 Didier Fabert <didier.fabert@gmail.com> - 1.22.3-1
- New upstream release.

* Fri Feb 28 2014 Didier Fabert <didier.fabert@gmail.com> - 1.22.2-2
- Minor changes on mw-createinstance script
- Add php-cli for dependency

* Thu Feb 27 2014 Didier Fabert <didier.fabert@gmail.com> - 1.22.2-1
- New upstream release.
- Remove maintenance hiphop directory (needs hiphop virtual machine)

* Tue Jan 21 2014 Didier Fabert <didier.fabert@gmail.com> - 1.22.1-1
- New upstream release.

* Mon Dec 09 2013 Didier Fabert <didier.fabert@gmail.com> - 1.21.3-3
- Add NoTitle extension

* Tue Dec 03 2013 Didier Fabert <didier.fabert@gmail.com> - 1.21.3-1
- New upstream release.

* Sun Nov 03 2013 Didier Fabert <didier.fabert@gmail.com> - 1.21.2-2
- New upstream release.

* Sat Aug 31 2013 Didier Fabert <didier.fabert@gmail.com> - 1.21.1-4
- Add RandomImage and IncludeArticle extension

* Mon Jul 22 2013 Didier Fabert <didier.fabert@gmail.com> - 1.21.1-3
- Fix Obsoletes by Michael Cronenworth <mike@cchtml.com>
- Add several extensions

* Tue Jul 09 2013 Michael Cronenworth <mike@cchtml.com> - 1.21.1-2
- Provide/Obsolete now included extensions (#967811)

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

