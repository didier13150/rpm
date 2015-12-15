Name:          nagstamon
Version:       2.0.0.alpha1
Release:       1%{?dist}
Summary:       Nagios status monitor for desktop
Group:         Applications/Productivity

License:       GPLv2+
URL:           http://nagstamon.ifw-dresden.de/
Source0:       http://sourceforge.net/projects/nagstamon/files/nagstamon/nagstamon%20%{version}/%{name}_%{version}.tar.gz
Patch0:        nagstamon-enable-qt.patch

BuildArch:     noarch
BuildRequires: python3-qt5-devel
BuildRequires: python3-devel  
BuildRequires: desktop-file-utils
BuildRequires: Distutils
Requires:      python3-qt5
Requires:      python3-setuptools
Requires:      python3-keyring
Requires:      python3-SecretStorage
Requires:      python3-crypto
Requires:      python3-beautifulsoup4
#Requires:      python3-xlib
Requires:      mesa-vdpau-drivers

%description
Nagstamon is a Nagios status monitor for the desktop. It connects to multiple
Nagios, Icinga, Opsview, Centreon, Op5 Monitor/Ninja and Check_MK Multisite
monitoring servers and resides in systray or as a floating statusbar at the
desktop showing a brief summary of critical, warning, unknown, unreachable and
down hosts and services and pops up a detailed status overview when moving the
mouse pointer over it. Connecting to displayed hosts and services is easily
established by context menu via SSH, RDP and VNC. Users can be notified by
sound. Hosts and services can be filtered by category and regular expressions.

%prep
%setup -qn Nagstamon
%patch0 -p1

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install --skip-build --root %{buildroot}

#Fix 'non-executable-script' error
chmod +x %{buildroot}%{python3_sitelib}/Nagstamon/Servers/Multisite.py

#Provide directory to install icon for desktop file
mkdir -p %{buildroot}%{_datadir}/pixmaps

#Copy icon to pixmaps directory
cp Nagstamon/resources/%{name}.svg %{buildroot}%{_datadir}/pixmaps/%{name}.svg

#Remove execute bit from icon
chmod -x %{buildroot}%{_datadir}/pixmaps/%{name}.svg

#Remove the file extension for convenience
mv %{buildroot}%{_bindir}/%{name}-qt.py %{buildroot}%{_bindir}/%{name}

desktop-file-install --dir %{buildroot}/%{_datadir}/applications\
                     --delete-original\
                     --set-icon=%{name}.svg\
                     %{buildroot}%{python3_sitelib}/Nagstamon/resources/%{name}.desktop

%files
%doc ChangeLog COPYRIGHT LICENSE
%{_datadir}/pixmaps/%{name}.svg
%{_datadir}/applications/%{name}.desktop
%{python3_sitelib}/Nagstamon/
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{python3_sitelib}/%{name}*.egg-info

%changelog
* Fri Dec 11 2015 Didier Fabert <didier.fabert@gmail.com> 2.0.0.alpha1
- Update from git upstream

* Wed Jun 25 2014 Didier Fabert <didier.fabert@gmail.com> 1.0.1-1
- Update from git upstream

* Wed Jun 25 2014 Didier Fabert <didier.fabert@gmail.com> 1.0-0.rc1
- Update from git upstream

* Wed Dec 18 2013 Didier Fabert <didier.fabert@gmail.com> 0.9.11-0.2.head
- Update from git upstream

* Tue Apr 30 2013 Nikita Klimov <nk@jaur.su> 0.9.9-8
- Added gnome-python2-libegg to 'Requires' for fix incorrect display in tray

* Fri Apr 05 2013 Nikita Klimov <nk@jaur.su> 0.9.9-7
- Removed patch to fix FSF address, wait while upstream fix it yourself

* Fri Apr 05 2013 Nikita Klimov <nk@jaur.su> 0.9.9-6
- Added patch to fix FSF address in setup.py

* Tue Apr 02 2013 Nikita Klimov <nk@jaur.su> 0.9.9-5
- Fix icon file mode bits

* Mon Apr 01 2013 Nikita Klimov <nk@jaur.su> 0.9.9-4
- Replace python-devel to python2-devel in BuldRequires
- Copy desktop icon to pixmaps directory

* Mon Apr 01 2013 Nikita Klimov <nk@jaur.su> 0.9.9-3
- Remove embedded BeautifulSoup
- Add python-BeautifulSoup as Requires 
- Fix typo in files section

* Sun Mar 31 2013 Nikita Klimov <nk@jaur.su> 0.9.9-2
- Change license from GPLv2 to GPLv2+
- Added comments to install section
- Hard-coded paths replaced to macros

* Tue Mar 26 2013 Nikita Klimov <nk@jaur.su> 0.9.9-1
- Initial version of the package
