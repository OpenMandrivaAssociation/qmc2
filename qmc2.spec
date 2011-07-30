Name:			qmc2
Version:		0.2.b20
Release:		%mkrel 0.svn2840

Summary:	M.A.M.E. Catalog / Launcher II
License:	GPLv2+
Group:		Emulators
URL:		http://sourceforge.net/projects/qmc2/
#alt url	http://qmc2.arcadehits.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
#http://qmc2.svn.sourceforge.net/viewvc/qmc2/trunk/data/opt/SDLMAME/template.xml?revision=2835
Source1:	sdlmame-0.142u4-template.xml
#http://qmc2.svn.sourceforge.net/viewvc/qmc2/trunk/data/opt/SDLMESS/template.xml?revision=2755
Source2:	sdlmess-0.142u3-template.xml
Source10:	qmc2-48.png

BuildRequires:	qt4-devel > 4.5
%if %mdkversion >= 200900
BuildRequires:	phonon-devel
%endif
BuildRequires:	X11-devel
BuildRequires:	SDL-devel
BuildRequires:	rsync
BuildRoot:	%{_tmppath}/%{name}-%{version}

#not requiring non-free
#Requires:	sdlmame
Suggests:	sdlmame
Suggests:	sdlmame-extra-data
Suggests:	sdlmess

Epoch:		1

%description
QMC2 is a Qt4 based front-end for SDLMAME and SDLMESS.

%prep
%setup -q -n %{name}
#updates sdlmame & sdlmess templates
cp -f %{SOURCE1} data/opt/SDLMAME/template.xml
cp -f %{SOURCE2} data/opt/SDLMESS/template.xml

#fix rights on movie.png
chmod 644 data/img/classic/movie.png

%build
# to debug qmc2, add DEBUG=1 and install the -debug package too.
%make \
 QTDIR=%{_prefix}/lib/qt4 \
 PREFIX=%{_prefix} \
 JOYSTICK=1 \
 OPENGL=1 \
 EMULATOR=SDLMESS
mv qmc2-sdlmess qmc2-sdlmess.bak
make clean QTDIR=%{_prefix}/lib/qt4

%make \
 QTDIR=%{_prefix}/lib/qt4 \
 PREFIX=%{_prefix} \
 JOYSTICK=1 \
 OPENGL=1 \
 EMULATOR=SDLMAME

%install
rm -rf %{buildroot}
%makeinstall \
 PREFIX=%{_prefix} \
 DESTDIR=%{buildroot} \
 QTDIR=%{_prefix}/lib/qt4 \
 EMULATOR=SDLMAME

#install qmc2-sdlmess as well
install -m 755 qmc2-sdlmess.bak %{buildroot}/%{_bindir}/qmc2-sdlmess

#icons
install -d -m 755 %{buildroot}/%{_iconsdir}
install -m 644 %{_sourcedir}/qmc2-48.png %{buildroot}/%{_iconsdir}/%{name}.png

#xdg menus
install -d -m 755 %{buildroot}%{_datadir}/applications
cat<<EOF>%{buildroot}%{_datadir}/applications/mandriva-%{name}-sdlmame.desktop
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
cat<<EOF>%{buildroot}%{_datadir}/applications/mandriva-%{name}-sdlmess.desktop
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

rm -f %{buildroot}%{_datadir}/applications/qmc2-sdlmame.desktop

%files
%defattr(-,root,root)
%{_bindir}/runonce
%{_bindir}/%{name}
%{_bindir}/%{name}-sdlmame
%{_bindir}/%{name}-sdlmess
#{_bindir}/romalyzer.pl
%{_datadir}/%{name}
%{_datadir}/applications/mandriva-%{name}-sdlmame.desktop
%{_datadir}/applications/mandriva-%{name}-sdlmess.desktop
%{_iconsdir}/%{name}.png
%config %{_sysconfdir}/%{name}/%{name}.ini

%clean
rm -rf %{buildroot}

