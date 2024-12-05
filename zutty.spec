# set to nil when packaging a release, 
# or the long commit tag for the specific git branch
%global commit_tag %{nil}

# set with the commit date only if commit_tag not nil 
# git version (i.e. master) in format date +Ymd
%if "%{commit_tag}" != "%{nil}"
%global commit_date %(git show -s --date=format:'%Y%m%d' %{commit_tag})
%endif

%global icon_sizes 16x16 32x32 48x48 64x64 96x96 128x128

Name:           zutty
Version:        0.16
Release:        1
Summary:        Terminal program with GLES renderer and low latency
License:        GPL-3.0-or-later
Group:          System/X11/Terminals
URL:            https://tomscii.sig7.se/%{name}/

# author does not version the folder or compressed file, so this must be done manually
Source0:        %{name}-%{version}.tar.xz
Source1:        FAQ.md

BuildRequires:  pkgconfig(xmu)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(libglvnd)
BuildRequires:  pkgconfig
BuildRequires:  waf

%description
An X terminal emulator rendering through OpenGL ES shaders.
It has good input latency and VTxxx emulation over most other
terminals, ranging second after xterm (as of 2022).
It uses FreeType, but does not support fontconfig, thus won't find
fonts by their usual names. (See FAQ for details.)

%prep
%autosetup -n %{name}-%{version}
cp -a %{S:1} .

%build
CXXFLAGS="%{?optflags}" \
LDFLAGS="%{?build_ldflags}" \
./waf configure --prefix="%{_prefix}" --no-werror --check-cxx-compiler=clang++
./waf

%install
./waf install --destdir=%{buildroot}
%(for i in %{icon_sizes};
    do
        install -p -D icons/zutty_$i.png %{buildroot}%{_datadir}/icons/$i/apps/zutty_$i.png
done)
install -p -D icons/zutty.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/zutty.svg
install -p -D icons/zutty.desktop %{buildroot}%{_datadir}/applications/zutty.desktop


%files
%{_datadir}/applications/zutty.desktop
%(for i in %{icon_sizes};
    do
        %{_datadir}/icons/hicolor/$i/apps/zutty_$i.png
done)
%{_datadir}/icons/hicolor/scalable/apps/zutty.svg
%{_bindir}/zutty
%doc FAQ.md
%license LICENSE
