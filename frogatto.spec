Name:		frogatto
Version:	1.2
Release:	2
Summary:	Frogatto & Friends classic adventure game
License:	GPLv3+
Group:		Games/Arcade
URL:		http://www.frogatto.com/
# 1.2 is available at https://github.com/frogatto/frogatto/tarball/1.2 only
Source:		http://www.frogatto.com/files/%{name}-%{name}-%{version}-0-g07a33cd.tar.gz
Source1:	frogatto
Source2:	frogatto.desktop
Source3:	frogatto.xpm
Source4:	frogatto.6
Patch1:		frogatto-1.0-asneeded.patch
BuildRequires:	boost-devel
BuildRequires:	gcc-c++
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:	SDL_ttf-devel
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	ccache
BuildRequires:	glibc-devel

Requires: %{name}-gamedata = %{version}

%description
Frogatto & Friends is a old-school 2d platformer game, starring a certain
quixotic frog.

%package	gamedata
Summary:	Game data for frogatto
License:	distributable
Group:		Games/Arcade
# We split game data to separate package to make it noarch and thus save
# bandwidth and space on distribution media.
BuildArch:	noarch

%description	gamedata
Game data for frogatto.

%prep
%setup -q -n %{name}-%{name}-64c84bf
sed -i -e 's#BINARY_FILE=.*#BINARY_FILE=%{_libdir}/frogatto/game#g' %{SOURCE1}

%build
%make

%install
install -d %{buildroot}%{_datadir}/frogatto
install -pDm 755 game %{buildroot}%{_libdir}/frogatto/game
cp -a images data music sounds %{buildroot}%{_datadir}/frogatto

install -pDm 755 %{SOURCE1} %{buildroot}%{_gamesbindir}/frogatto
install -pDm 644 %{SOURCE2} %{buildroot}%{_datadir}/applications/frogatto.desktop
install -pDm 644 %{SOURCE3} %{buildroot}%{_datadir}/pixmaps/frogatto.xpm
install -pDm 644 %{SOURCE4} %{buildroot}%{_mandir}/man6/frogatto.6

%files
%{_gamesbindir}/*
%{_libdir}/%{name}/
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%{_mandir}/man6/*

%files gamedata
%doc LICENSE
%{_datadir}/%{name}

