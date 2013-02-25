Name:           povray-include-extra
Version:        1.0.0
Release:        1%{?dist}
Summary:        Extra povray include files
License:        GPLv2
Group:          Applications/Multimedia
URL:            http://www.oyonale.com
Source0:        http://www.oyonale.com/downloads/scifi_demo.zip
Source1:        http://www.oyonale.com/downloads/maketree.zip
Source2:        http://www.oyonale.com/downloads/field.pov
Source3:        http://www.oyonale.com/downloads/makesnow.inc
Source4:        http://www.oyonale.com/downloads/makesnow2.inc
Source5:        http://www.oyonale.com/downloads/lostbus.pov
Source6:        http://www.oyonale.com/downloads/pipeset.pov
Source7:        http://www.oyonale.com/downloads/madpipe.zip
Source8:        http://www.imagico.de/pov/water/waves03.zip
Source9:        http://baillp.free.fr/Data/feather.inc
Source10:       http://www.reocities.com/SiliconValley/Lakes/1434/download/tilegen.zip
Source11:       http://www.reocities.com/SiliconValley/Lakes/1434/download/pcm.zip
Source12:       http://www.reocities.com/SiliconValley/Lakes/1434/download/city.zip
Source13:       http://www.reocities.com/SiliconValley/Lakes/1434/download/spray.zip
Source14:       http://www.reocities.com/SiliconValley/Lakes/1434/download/explode.zip
Source15:       http://www.reocities.com/SiliconValley/Lakes/1434/download/galaxy.zip
Source16:       http://www.reocities.com/SiliconValley/Lakes/1434/download/lnsefcts.zip
Source17:       http://www.reocities.com/SiliconValley/Lakes/1434/download/clockmod.zip
Source18:       http://www.reocities.com/SiliconValley/Lakes/1434/download/bend.zip
Source19:       http://www.imagico.de/pov/iw/isowood03.zip
Source20:       http://runevision.com/3d/include/cd.zip
Source21:       http://runevision.com/3d/include/grasstex.zip
Source22:       http://runevision.com/3d/include/ikn.zip
Source23:       http://www.getinfo.net/douge/mayafur.zip
Source24:       http://www.getinfo.net/douge/mayafur15.zip
Source25:       http://www.nolights.de/downloads/parsys.zip
Source26:       http://brannigan.emporia.edu/courses/2004/cs220f04/hand38/eyeball.inc
Source27:       http://brannigan.emporia.edu/courses/2004/cs220f04/hand38/eyeball.pov
Source28:       http://www.f-lohmueller.de/pov_tut/down/pov_objects1.zip
Source29:       http://www.f-lohmueller.de/pov_tut/modelling/dwn/RT_System.zip
Source30:       http://www.f-lohmueller.de/pov_tut/down/shapes_lo.inc
Source31:       http://runevision.com/3d/include/mouth.zip
Source32:       http://news.povray.org/povray.binaries.scene-files/attachment/%3C3d06c6c4%40news.povray.org%3E/starship_enterprise_v1.00.zip?ttop=346850&toff=650
Source33:       http://brannigan.emporia.edu/courses/2008/cs220f08/hand63/ncc1701.zip
Source34:       http://www.dylanbeattie.net/starwars/download/stdest.zip
Source35:       http://www.dylanbeattie.net/starwars/download/tie_def.zip
Source36:       http://www.dylanbeattie.net/starwars/download/tie_i.zip
Source37:       http://www.dylanbeattie.net/starwars/download/tie_f.zip
Source38:       http://www.dylanbeattie.net/starwars/download/shuttle.zip
Source39:       http://www.dylanbeattie.net/starwars/download/tie_d.zip
Source40:       http://www.dylanbeattie.net/starwars/download/falcon_wip.zip
Source41:       http://www.dylanbeattie.net/starwars/download/ewing.zip
Source42:       http://www.dylanbeattie.net/starwars/download/pilot.zip
Source43:       http://www.dylanbeattie.net/starwars/download/awing.zip
Source44:       http://www.dylanbeattie.net/starwars/download/ywing.zip
Source45:       http://www.dylanbeattie.net/starwars/download/ccrv.zip
Source46:       http://www.dylanbeattie.net/starwars/download/xwing.zip
Source47:       http://www.dylanbeattie.net/starwars/download/bwing.zip
Source48:       http://www.dylanbeattie.net/starwars/download/c_city.zip
Source49:       http://tofbouf.free.fr/download/fern.zip
Source50:       http://tofbouf.free.fr/download/explose.zip
Source51:       http://objects.povworld.org/binaries/earth.pov
Source52:       http://objects.povworld.org/binaries/columns.zip
Source53:       http://objects.povworld.org/binaries/lighthouse.zip
Source54:       http://objects.povworld.org/binaries/waterfall.pov
Source55:       http://objects.povworld.org/binaries/tintinrocket.zip
Source56:       http://objects.povworld.org/binaries/boat.pov
Source57:       http://objects.povworld.org/binaries/sunboat.pov
Source58:       http://runevision.com/3d/include/particles/particle101.zip
Source59:       http://runevision.com/3d/include/electric.zip
Source60:       http://runevision.com/3d/include/illusion.zip
Source61:       http://www.travelnotes.de/rays/seaplane/b317.include
Source62:       http://www.travelnotes.de/rays/seaplane/palms.include
Source63:       http://www.f-lohmueller.de/pov_tut/objects/plants/Palm_1.inc
Source64:       http://www.f-lohmueller.de/pov_tut/objects/plants/Palm_2.inc
Source65:       http://www.f-lohmueller.de/pov_tut/objects/plants/Palm_1quadro.inc
Source66:       http://www.f-lohmueller.de/pov_tut/objects/plants/Reeds_0.inc
Source67:       http://downloads.sourceforge.net/project/jpatch/jpatch/JPatch%200.4%20PREVIEW%201/jpatch0_4preview1.zip


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       povray

%description
Extra povray include files

%prep
%setup -qn %{name}

%build

%install
rm -rf $RPM_BUILD_ROOT
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)

%changelog
* Mon Dec 17 2012 Didier Fabert <didier.fabert@gmail.com> 1.10-1
- First Release