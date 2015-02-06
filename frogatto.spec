%global commit a7ef3bfa0c32df4852bf057fab969c1a080edf4d
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:		frogatto
Version:	1.3.3
Release:	3
Summary:	Frogatto & Friends classic adventure game
License:	GPLv3+
Group:		Games/Arcade
URL:		http://www.frogatto.com/
Source:		https://github.com/frogatto/frogatto/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
Source1:	frogatto
Source2:	frogatto.desktop
Source3:	frogatto.pod
# Patch Makefile not to link lSDLmain
Patch0:         %{name}-1.2-Makefile.patch
# Boost no longer has separate non mt and -mt variants of its libs
Patch1:         %{name}-1.3-no-boost-mt.patch
# Use FreeFont instead of the Ubuntu Font Family
Patch2:         %{name}-1.3-fonts.patch

BuildRequires:  boost-devel
BuildRequires:  gcc-c++
BuildRequires:  SDL-devel
BuildRequires:  SDL_image-devel
BuildRequires:  SDL_mixer-devel
BuildRequires:  SDL_ttf-devel
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(glew)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  ccache
BuildRequires:  glibc-devel
BuildRequires:  perl
BuildRequires:  libicns-utils
BuildRequires:  desktop-file-utils

Requires:       hicolor-icon-theme
Requires:       fonts-ttf-freefont

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
%setup -qn %{name}-%{commit}
%patch0 -p1
%patch1 -p1
%patch2 -p1

sed -i -e 's#BINARY_FILE=.*#BINARY_FILE=%{_libdir}/frogatto/game#g' %{SOURCE1}

# Fix locale file path
sed -i 's!"./locale/"!"%{_datadir}/locale/"!' src/i18n.cpp

%build
%make

%install
# Install wrapper script
install -d %{buildroot}%{_gamesbindir}
install -pDm 755 %{SOURCE1} %{buildroot}%{_gamesbindir}/frogatto

# Install game and data
install -d %{buildroot}%{_libdir}/%{name}
install -m 755 -p game %{buildroot}%{_libdir}/%{name}
install -d %{buildroot}%{_datadir}/%{name}/modules/%{name}
cp -pr data images music *.cfg %{buildroot}%{_datadir}/%{name}
pushd modules/%{name}
cp -pr data images music sounds *.cfg \
  %{buildroot}%{_datadir}/%{name}/modules/%{name}
# Install translations
  cp -pr locale %{buildroot}%{_datadir}
popd

# Install desktop file
install -d %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  %{SOURCE2}

# Extract Mac OS X icons
icns2png -x modules/%{name}/images/os/mac/icon.icns

# Install icons
for i in 16 32 128 256; do
  install -d -m 755 %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
  install -m 644 icon_${i}x${i}x32.png \
    %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/%{name}.png
done

# Install man page
install -d %{buildroot}%{_mandir}/man6
pod2man --section=6 \
  -center="RPM Fusion contributed man pages" \
  -release="%{name} %{version}" \
  -date="July 13th, 2010" \
   %{SOURCE3} > %{buildroot}%{_mandir}/man6/%{name}.6

%find_lang %{name}

%files -f %{name}.lang
%{_gamesbindir}/*
%{_libdir}/%{name}/
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_mandir}/man6/*

%files gamedata
%doc LICENSE modules/%{name}/CHANGELOG
%{_datadir}/%{name}


