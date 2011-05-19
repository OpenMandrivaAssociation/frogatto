
Name: frogatto
Version: 1.1
Release: %mkrel 1
Summary: Frogatto & Friends classic adventure game
License: GPLv3+
Group: Games/Arcade
URL: http://www.frogatto.com/
Source: http://www.frogatto.com/files/frogatto-%version.tar.bz2
Source1: frogatto
Source2: frogatto.desktop
Source3: frogatto.xpm
Source4: frogatto.6
Patch1: frogatto-1.0-asneeded.patch


# Automatically added by buildreq on Thu Aug 26 2010
BuildRequires: boost-devel gcc-c++ libSDL_image-devel libSDL_mixer-devel libSDL_ttf-devel libglew-devel libpng-devel ccache glibc-devel


Requires: %name-gamedata = %version

%description
Frogatto & Friends is a old-school 2d platformer game, starring a certain
quixotic frog.

%package gamedata
Summary: Game data for frogatto
License: distributable
Group: Games/Arcade
# We split game data to separate package to make it noarch and thus save
# bandwidth and space on distribution media.
BuildArch: noarch

%description gamedata
Game data for frogatto.

%prep
%setup
# %patch1 -p1
#subst 's/ccache //' Makefile

%build
%make

%install
install -d %buildroot%_datadir/frogatto
install -pDm 755 game %buildroot%_libdir/frogatto/game
cp -a images data music sounds %buildroot%_datadir/frogatto

install -pDm 755 %_sourcedir/frogatto %buildroot%_gamesbindir/frogatto
install -pDm 644 %_sourcedir/frogatto.desktop %buildroot%_desktopdir/frogatto.desktop
install -pDm 644 %_sourcedir/frogatto.xpm %buildroot%{_pixmaps}/frogatto.xpm
install -pDm 644 %_sourcedir/frogatto.6 %buildroot%{_mandir}/man6/frogatto.6

%files
%_gamesbindir/*
%_libdir/frogatto/
%_desktopdir/*
# %{_pixmaps}/*
%{_mandir}/man6/*

%files gamedata
%doc LICENSE
%_datadir/frogatto

