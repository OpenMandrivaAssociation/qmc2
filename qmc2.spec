# sdlmame & sdlmess templates section is commented out because
# templates are up to date at this moment but sometimes we need to
# update them from SVN

Name:		qmc2
Version:	0.35
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
%defattr(-,root,root)
%{_bindir}/runonce
%{_bindir}/%{name}
%{_bindir}/%{name}-sdlmame
%{_bindir}/%{name}-sdlmess
%{_datadir}/%{name}
%{_datadir}/applications/mandriva-%{name}-sdlmame.desktop
%{_datadir}/applications/mandriva-%{name}-sdlmess.desktop
%{_iconsdir}/%{name}.png
%config %{_sysconfdir}/%{name}/%{name}.ini
