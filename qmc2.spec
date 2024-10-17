# sdlmame & sdlmess templates section is commented out because
# templates are up to date at this moment but sometimes we need to
# update them from SVN
%define _disable_lto 1

Summary:	M.A.M.E. Catalog / Launcher II
Name:		qmc2
Version:	0.195
Release:	1
Epoch:		1
License:	GPLv2+
Group:		Emulators
Url:		https://sourceforge.net/projects/qmc2/
#alt url	http://qmc2.arcadehits.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
#http://qmc2.svn.sourceforge.net/viewvc/qmc2/trunk/data/opt/SDLMAME/template.xml?revision=2835
#Source1:	sdlmame-0.142u4-template.xml
#http://qmc2.svn.sourceforge.net/viewvc/qmc2/trunk/data/opt/SDLMESS/template.xml?revision=2755
#Source2:	sdlmess-0.142u3-template.xml
Source10:	qmc2-48.png
BuildRequires:	cmake(ECM)
BuildRequires:	cmake(Qt5Core) cmake(Qt5Gui) cmake(Qt5Xml) cmake(Qt5XmlPatterns) cmake(Qt5WebKit) cmake(Qt5Network) cmake(Qt5Sql) cmake(Qt5Svg) cmake(Qt5Widgets) cmake(Qt5Test) cmake(Qt5WebKitWidgets) cmake(Qt5Multimedia) cmake(Qt5MultimediaWidgets)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(phonon)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	rsync

#not requiring non-free
Suggests:	sdlmame
Suggests:	sdlmame-extra-data
Suggests:	sdlmess

%description
QMC2 is a Qt5 based front-end for SDLMAME and SDLMESS.

%files
%{_bindir}/%{name}
%{_bindir}/%{name}-sdlmame
%{_bindir}/%{name}-arcade
%{_datadir}/%{name}
%{_datadir}/applications/mandriva-%{name}-sdlmame.desktop
%{_datadir}/applications/mandriva-%{name}-arcade.desktop
%{_iconsdir}/%{name}.png
%{_iconsdir}/%{name}-arcade.png
%config %{_sysconfdir}/%{name}/%{name}.ini

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}
#updates sdlmame & sdlmess templates
#cp -f %{SOURCE1} data/opt/SDLMAME/template.xml
#cp -f %{SOURCE2} data/opt/SDLMESS/template.xml

%build

export PATH=%_qt5_bindir:$PATH
# to debug qmc2, add DEBUG=1 and install the -debug package too.
%make \
 QTDIR=%{_qt5_libdir}/qt5 \
 PREFIX=%{_prefix} \
 CXX_FLAGS="%{optflags}" \
 JOYSTICK=1 \
 OPENGL=1 \
 EMULATOR=SDLMAME

%make \
 CXX_FLAGS="%{optflags}" \
 arcade

%install
%makeinstall \
 PREFIX=%{_prefix} \
 DESTDIR=%{buildroot} \
 QTDIR=%{_prefix}/lib/qt4 \
 EMULATOR=SDLMAME

#install qmc2-arcade
install -m 755 arcade/%{name}-arcade %{buildroot}%{_bindir}/%{name}-arcade

#icons
install -d -m 755 %{buildroot}%{_iconsdir}
install -m 644 %{SOURCE10} %{buildroot}%{_iconsdir}/%{name}.png
install -m 644 arcade/images/%{name}-arcade.png %{buildroot}%{_iconsdir}/%{name}-arcade.png

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

cat<<EOF>%{buildroot}%{_datadir}/applications/mandriva-%{name}-arcade.desktop
[Desktop Entry]
Encoding=UTF-8
Name=QMC2 (Arcade)
Comment=%{summary}
Exec=%{_bindir}/%{name}-arcade
Icon=%{name}-arcade.png
Terminal=false
Type=Application
Categories=X-MandrivaLinux-MoreApplications-Emulators;Emulator;Game;
EOF

rm -f %{buildroot}%{_datadir}/applications/qmc2-sdlmame.desktop

