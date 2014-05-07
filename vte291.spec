%global apiver 2.91

Name:           vte291
Version:        0.37.0
Release:        1%{?dist}
Summary:        Terminal emulator library

License:        LGPLv2+
URL:            http://www.gnome.org/
Source0:        http://download.gnome.org/sources/vte/0.37/vte-%{version}.tar.xz
# https://bugzilla.gnome.org/show_bug.cgi?id=688456
Patch2:         0001-widget-Only-show-the-cursor-on-motion-if-moved.patch

BuildRequires:  gettext
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk3-devel
BuildRequires:  intltool
BuildRequires:  ncurses-devel
BuildRequires:  vala-tools

# initscripts creates the utmp group
Requires:       initscripts

%description
VTE is a library implementing a terminal emulator widget for GTK+. VTE
is mainly used in gnome-terminal, but can also be used to embed a
console/terminal in games, editors, IDEs, etc.

VTE supports Unicode and character set conversion, as well as emulating
any terminal known to the system's terminfo database.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n vte-%{version}
%patch2 -p1 -b .motion

%build
CFLAGS="%optflags -fPIE -DPIE" \
CXXFLAGS="$CFLAGS" \
LDFLAGS="$LDFLAGS -Wl,-z,relro -Wl,-z,now -pie" \
%configure \
        --disable-static \
        --with-gtk=3.0 \
        --libexecdir=%{_libdir}/vte-%{apiver} \
        --disable-gtk-doc \
        --enable-introspection
make %{?_smp_mflags} V=1

%install
%make_install

# Rename the profile script for parallel installability
mv $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/vte.sh \
   $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/vte-%{apiver}.sh

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang vte-%{apiver}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f vte-%{apiver}.lang
%doc COPYING NEWS README
%{_sysconfdir}/profile.d/vte-%{apiver}.sh
%{_libdir}/libvte-%{apiver}.so.0*
%dir %{_libdir}/vte-%{apiver}
%attr(2711,root,utmp) %{_libdir}/vte-%{apiver}/gnome-pty-helper
%{_libdir}/girepository-1.0/

%files devel
%{_bindir}/vte-%{apiver}
%{_includedir}/vte-%{apiver}/
%{_libdir}/libvte-%{apiver}.so
%{_libdir}/pkgconfig/vte-%{apiver}.pc
%{_datadir}/gir-1.0/
%doc %{_datadir}/gtk-doc/
%{_datadir}/vala/

%changelog
* Tue May 06 2014 Kalev Lember <kalevlember@gmail.com> - 0.37.0-1
- Initial Fedora package, based on previous vte3 0.36 packaging
