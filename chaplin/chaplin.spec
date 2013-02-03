Name:           chaplin
Version:        1.10
Release:        1%{?dist}
Summary:        A dvd chapter tool for Linux
License:        GPLv2
Group:          Sound and Video
URL:            http://www.lallafa.de/bp/chaplin.html
Source0:        %{name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libdvdread-devel
Requires:       libdvdread, vcdimager, transcode

%description
The tool parses a DVD disc or image and extracts the exact duration for each
chapter of a given title. Then the total list of chapters is split into a
user-selectable number of subsets. Each subset should have approximately
the same duration.

This is a very useful approach for multi-cd rips. You no longer simply split
the movie in the middle of the frame count but you choose two sets of chapters
for both parts which both have (almost) the same length. Then the disc-break
is not at a rather random point (concering the story telling of the movie)
but at the end of a dvd-chapter.

The chapter timings and the split sets are also very useful for chapter
navigation (even on a single disc). The normal output mode of chaplin thus
prints the chapter's relative beginning time and the duration in a wide number
of formats, ranging from seconds, frame counts to timestamps.

For S/VCD mastering chaplin can also produce vcdimager XML files for each disc.
There a complete sequence structure with chapter entry points is defined.
Also the full navigation setup for chapter hopping is provided. Additionally
you can add chapter menus and automatically create the necessary menu pages
out of thumbnails extracted directly from the DVD. 

%package genmenu
Requires:       %{name}
Summary:        Port-knocking server
Group:          Sound and Video
Requires:       ImageMagick, mjpegtools
BuildArch:      noarch

%description genmenu
The chaplin-genmenu script creates the chapter menu still image MPG files that
are referenced in the S/VCD chapter menus

%prep
%setup -qn %{name}

%build
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%{__mkdir_p} $RPM_BUILD_ROOT%{_bindir}
cp chaplin $RPM_BUILD_ROOT%{_bindir}
cp chaplin-genmenu $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/chaplin

%files genmenu
%defattr(-,root,root,-)
%{_bindir}/chaplin-genmenu

%changelog
* Mon Dec 17 2012 Didier Fabert <didier.fabert@gmail.com> 1.10-1
- First Release