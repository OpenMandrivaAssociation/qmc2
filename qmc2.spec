# sdlmame & sdlmess templates section is commented out because
# templates are up to date at this moment but sometimes we need to
# update them from SVN

Name:		qmc2
Version:	0.36
Release:	%mkrel 1
Epoch:		1
Summary:	M.A.M.E. Catalog / Launcher II
License:	GPLv2+
Group:		Emulators
URL:		http://sourceforge.net/projects/qmc2/
#alt url	http://qmc2.arcadehits.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
#http://qmc2.svn.sourceforge.net/viewvc/qmc2/trunk/data/opt/SDLMAME/template.xml?revision=2835
#Source1:	sdlmame-0.142u4-template.xml
#http://qmc2.svn.sourceforge.net/viewvc/qmc2/trunk/data/opt/SDLMESS/template.xml?revision=2755
#Source2:	sdlmess-0.142u3-template.xml
Source10:	qmc2-48.png
BuildRequires:	qt4-devel >= 4:4.7.0
BuildRequires:	phonon-devel
BuildRequires:	X11-devel
BuildRequires:	SDL-devel
BuildRequires:	rsync

#not requiring non-free
Suggests:	sdlmame
Suggests:	sdlmame-extra-data
Suggests:	sdlmess

%description
QMC2 is a Qt4 based front-end for SDLMAME and SDLMESS.

%prep
%setup -q -n %{name}
#updates sdlmame & sdlmess templates
#cp -f %{SOURCE1} data/opt/SDLMAME/template.xml
#cp -f %{SOURCE2} data/opt/SDLMESS/template.xml

%build
# to debug qmc2, add DEBUG=1 and install the -debug package too.
%make \
 QTDIR=%{_prefix}/lib/qt4 \
 PREFIX=%{_prefix} \
 JOYSTICK=1 \
 OPENGL=1 \
 EMULATOR=SDLMESS
%__mv qmc2-sdlmess qmc2-sdlmess.bak
make clean QTDIR=%{_prefix}/lib/qt4

%make \
 QTDIR=%{_prefix}/lib/qt4 \
 PREFIX=%{_prefix} \
 JOYSTICK=1 \
 OPENGL=1 \
 EMULATOR=SDLMAME

%install
%__rm -rf %{buildroot}
%makeinstall \
 PREFIX=%{_prefix} \
 DESTDIR=%{buildroot} \
 QTDIR=%{_prefix}/lib/qt4 \
 EMULATOR=SDLMAME

#install qmc2-sdlmess as well
%__install -m 755 qmc2-sdlmess.bak %{buildroot}%{_bindir}/qmc2-sdlmess

#icons
%__install -d -m 755 %{buildroot}%{_iconsdir}
%__install -m 644 %{SOURCE10} %{buildroot}%{_iconsdir}/%{name}.png

#xdg menus
%__install -d -m 755 %{buildroot}%{_datadir}/applications

%__cat<<EOF>%{buildroot}%{_datadir}/applications/mandriva-%{name}-sdlmame.desktop
[Desktop Entry]
Encoding=UTF-8
Name=QMC2 (SDL MAME)
Comment=%{summary}
Exec=%{_bindir}/%{name}-sdlmame
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-MoreApplications-Emulators;Emulator;Game;
EOF

%__cat<<EOF>%{buildroot}%{_datadir}/applications/mandriva-%{name}-sdlmess.desktop
[Desktop Entry]
Encoding=UTF-8
Name=QMC2 (SDL MESS)
Comment=%{summary}
Exec=%{_bindir}/%{name}-sdlmess
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-MoreApplications-Emulators;Emulator;Game;
EOF

%__rm -f %{buildroot}%{_datadir}/applications/qmc2-sdlmame.desktop

%clean
%__rm -rf %{buildroot}

%files
%{_bindir}/runonce
%{_bindir}/%{name}
%{_bindir}/%{name}-sdlmame
%{_bindir}/%{name}-sdlmess
%{_datadir}/%{name}
%{_datadir}/applications/mandriva-%{name}-sdlmame.desktop
%{_datadir}/applications/mandriva-%{name}-sdlmess.desktop
%{_iconsdir}/%{name}.png
%config %{_sysconfdir}/%{name}/%{name}.ini


%changelog
* Wed May 23 2012 Andrey Bondrov <abondrov@mandriva.org> 1:0.36-1
+ Revision: 800176
- New version 0.36

* Wed Feb 08 2012 Andrey Bondrov <abondrov@mandriva.org> 1:0.35-1
+ Revision: 771908
- New version 0.35, update BuildRequires, spec cleanup

* Sat Jul 30 2011 Andrey Bondrov <abondrov@mandriva.org> 1:0.2.b20-0.svn2840
+ Revision: 692377
- imported package qmc2


* Tue Jul 19 2011 Andrey Bondrov <bondrov@math.dvgu.ru> 1:0.2.b20-0.svn2840mdv2011.0
- Import from MIB

* Mon May 30 2011 Andrey Bondrov <bondrov@math.dvgu.ru> 1:0.2.b20-0.svn2840mib2010.2
- 0.2.b20 (pre, SVN 2840)
- Update to proper templates (sdlmame 0.142u4 and sdlmess 0.142u3)

* Thu Dec  2 2010 Guillaume Bedot <littletux@zarb.org> 1:0.2.b17-1plf2011.0
- 0.2.b17
- Update to latest templates

* Mon May 17 2010 Guillaume Bedot <littletux@zarb.org> 1:0.2.b15-1plf2010.1
- 0.2.b15 (template for mame 0.138)

* Tue Mar 23 2010 Guillaume Bedot <littletux@zarb.org> 0.2.b14-1plf2010.1
- 0.2.b14 (templates for mame/mess 0.137)

* Sun Jan 10 2010 Guillaume Bedot <littletux@zarb.org> 1:0.2.b13-1plf2010.1
- 0.2.b13

* Fri Sep 11 2009 Guillaume Bedot <littletux@zarb.org> 1:0.2.b11-1plf2010.0
- 0.2.b11

* Sun Sep  6 2009 Guillaume Bedot <littletux@zarb.org> 1:0.2.b10-1plf2010.0
- 0.2.b10
- sdlmess 0.133 templates

* Fri Jun 12 2009 Guillaume Bedot <littletux@zarb.org> 1:0.2.b9-1plf2010.0
- 0.2.b9 (sdlmess template 0.131 update becomes useless)
- update build requirements

* Mon May 18 2009 Guillaume Bedot <littletux@zarb.org> 1:0.2.b8-2plf2010.0
- new template for sdlmess 0.131

* Mon Apr 27 2009 Guillaume Bedot <littletux@zarb.org> 1:0.2.b8-1plf2009.1
- 0.2.b8

* Mon Apr 20 2009 Guillaume Bedot <littletux@zarb.org> 1:0.2.b7-1plf2009.1
- 0.2.b7

* Thu Jan  8 2009 Guillaume Bedot <littletux@zarb.org> 1:0.2.b6-1plf2009.1
- 0.2.b6
- add sdlmess, opengl support

* Tue Oct 21 2008 Guillaume Bedot <littletux@zarb.org> 1:0.2.b5-1plf2009.1
- 0.2.b5
- fix build requires, qt dir

* Sat Aug 16 2008 Guillaume Bedot <littletux@zarb.org> 1:0.2.b3-1plf2009.0
- 0.2.b3
- no debug
- drop old menu
- experimental joystick support

* Wed Feb  6 2008 Guillaume Bedot <littletux@zarb.org> 1:0.1-1plf2008.1
- 0.1

* Mon Jan 28 2008 Guillaume Bedot <littletux@zarb.org> 0.1.b11-1plf2008.1
- 0.1.b11

* Sun Jul 29 2007 Guillaume Bedot <littletux@zarb.org> 0.1.b10-1plf2008.0
- New release

* Tue May 15 2007 Guillaume Bedot <littletux@zarb.org> 0.1.b9-1plf2008.0
- First package for PLF
