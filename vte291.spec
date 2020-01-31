%global apiver 2.91

%global fribidi_version 1.0.0
%global glib2_version 2.40.0
%global gnutls_version 3.2.7
%global gtk3_version 3.19.5
%global pango_version 1.22.0
%global pcre2_version 10.21

Name:           vte291
Version:        0.58.3
Release:        2%{?dist}
Summary:        Terminal emulator library

License:        LGPLv2+
URL:            http://www.gnome.org/
Source0:        http://download.gnome.org/sources/vte/0.58/vte-%{version}.tar.xz

# https://bugzilla.gnome.org/show_bug.cgi?id=711059
# https://bugzilla.redhat.com/show_bug.cgi?id=1103380
Patch100:       vte291-cntnr-precmd-preexec-scroll.patch

BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  pkgconfig(fribidi) >= %{fribidi_version}
BuildRequires:  pkgconfig(gio-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gnutls) >= %{gnutls_version}
BuildRequires:  pkgconfig(gobject-2.0) >= %{glib2_version}
BuildRequires:  gobject-introspection-devel
BuildRequires:  gperf
BuildRequires:  gtk-doc
BuildRequires:  meson
BuildRequires:  pkgconfig(gtk+-3.0) >= %{gtk3_version}
BuildRequires:  pkgconfig(libpcre2-8) >= %{pcre2_version}
BuildRequires:  pkgconfig(pango) >= %{pango_version}
BuildRequires:  vala

Requires:       fribidi >= %{fribidi_version}
Requires:       glib2 >= %{glib2_version}
Requires:       gnutls%{?_isa} >= %{gnutls_version}
Requires:       gtk3%{?_isa} >= %{gtk3_version}
Requires:       pango >= %{pango_version}
Requires:       pcre2%{?_isa} >= %{pcre2_version}
Requires:       vte-profile

Conflicts:      gnome-terminal < 3.20.1-2

%description
VTE is a library implementing a terminal emulator widget for GTK+. VTE
is mainly used in gnome-terminal, but can also be used to embed a
console/terminal in games, editors, IDEs, etc.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

# vte-profile is deliberately not noarch to avoid having to obsolete a noarch
# subpackage in the future when we get rid of the vte3 / vte291 split. Yum is
# notoriously bad when handling noarch obsoletes and insists on installing both
# of the multilib packages (i686 + x86_64) as the replacement.
%package -n     vte-profile
Summary:        Profile script for VTE terminal emulator library
License:        GPLv3+
# vte.sh was previously part of the vte3 package
Conflicts:      vte3 < 0.36.1-3

%description -n vte-profile
The vte-profile package contains a profile.d script for the VTE terminal
emulator library.

%prep
%setup -q -n vte-%{version}
%patch100 -p1 -b .cntnr-precmd-preexec-scroll

%build
# Avoid overriding vte's own -fno-exceptions
# https://gitlab.gnome.org/GNOME/gnome-build-meta/issues/207
%global optflags %(echo %{optflags} | sed 's/-fexceptions //')

%meson --buildtype=plain -Ddocs=true
%meson_build

%install
%meson_install

%find_lang vte-%{apiver}

%files -f vte-%{apiver}.lang
%license COPYING.GPL3
%doc NEWS
%{_libdir}/libvte-%{apiver}.so.0*
%{_libdir}/girepository-1.0/

%files devel
%{_bindir}/vte-%{apiver}
%{_includedir}/vte-%{apiver}/
%{_libdir}/libvte-%{apiver}.so
%{_libdir}/pkgconfig/vte-%{apiver}.pc
%{_datadir}/gir-1.0/
%doc %{_datadir}/gtk-doc/
%{_datadir}/vala/

%files -n vte-profile
%{_sysconfdir}/profile.d/vte.sh

%changelog
* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.58.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 27 2019 Kalev Lember <klember@redhat.com> - 0.58.3-1
- Update to 0.58.3
- Avoid overriding vte's own -fno-exceptions

* Mon Oct 14 2019 Kalev Lember <klember@redhat.com> - 0.58.2-1
- Update to 0.58.2

* Mon Oct 07 2019 Kalev Lember <klember@redhat.com> - 0.58.1-1
- Update to 0.58.1

* Fri Oct 04 2019 Adam Williamson <awilliam@redhat.com> - 0.58.0-2
- Backport fix for crash due to out of bounds cursor position (#1756567)

* Mon Sep 09 2019 Kalev Lember <klember@redhat.com> - 0.58.0-1
- Update to 0.58.0

* Mon Aug 12 2019 Kalev Lember <klember@redhat.com> - 0.57.90-1
- Update to 0.57.90

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.57.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 02 2019 Debarshi Ray <rishi@fedoraproject.org> - 0.57.3-1
- Update to 0.57.3
- Rebase downstream patches

* Wed Jun 19 2019 Debarshi Ray <rishi@fedoraproject.org> - 0.57.0-2
- Support tracking the active container inside the terminal

* Tue Jun 18 2019 Debarshi Ray <rishi@fedoraproject.org> - 0.57.0-1
- Update to 0.57.0
- Switch to the Meson build system
- Rebase downstream patches

* Tue May 07 2019 Kalev Lember <klember@redhat.com> - 0.56.3-1
- Update to 0.56.3

* Mon May 06 2019 Kalev Lember <klember@redhat.com> - 0.56.2-1
- Update to 0.56.2

* Tue Apr 09 2019 Kalev Lember <klember@redhat.com> - 0.56.1-1
- Update to 0.56.1

* Tue Apr 02 2019 Debarshi Ray <rishi@fedoraproject.org> - 0.56.0-2
- Add signals proxying an interactive shell's precmd and preexec hooks.

* Mon Mar 11 2019 Kalev Lember <klember@redhat.com> - 0.56.0-1
- Update to 0.56.0

* Mon Mar 04 2019 Kalev Lember <klember@redhat.com> - 0.55.92-1
- Update to 0.55.92

* Tue Feb 19 2019 Kalev Lember <klember@redhat.com> - 0.55.90-2
- Rebuilt against fixed atk (#1626575)

* Tue Feb 19 2019 Kalev Lember <klember@redhat.com> - 0.55.90-1
- Update to 0.55.90

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.54.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 12 2018 Kalev Lember <klember@redhat.com> - 0.54.3-1
- Update to 0.54.3

* Fri Oct 26 2018 Kalev Lember <klember@redhat.com> - 0.54.2-1
- Update to 0.54.2

* Mon Oct 08 2018 Debarshi Ray <rishi@fedoraproject.org> - 0.54.1-4
- Removal of utmp logging makes the utmp group unnecessary

* Fri Oct 05 2018 Debarshi Ray <rishi@fedoraproject.org> - 0.54.1-3
- Tweak the escape sequence emission to unbreak the parsing

* Fri Oct 05 2018 Debarshi Ray <rishi@fedoraproject.org> - 0.54.1-2
- Tighten the dependencies a bit

* Fri Oct 05 2018 Debarshi Ray <rishi@fedoraproject.org> - 0.54.1-1
- Update to 0.54.1

* Thu Oct 04 2018 Debarshi Ray <rishi@fedoraproject.org> - 0.54.0-1
- Update to 0.54.0

* Thu Oct 04 2018 Debarshi Ray <rishi@fedoraproject.org> - 0.53.92-1
- Update to 0.53.92

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.53.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Kalev Lember <klember@redhat.com> - 0.53.0-2
- Require systemd, not initscripts for the utmp group (#1592403)

* Mon Jun 04 2018 Debarshi Ray <rishi@fedoraproject.org> - 0.53.0-1
- Update to 0.53.0

* Mon May 21 2018 Kalev Lember <klember@redhat.com> - 0.52.2-1
- Update to 0.52.2

* Mon Apr 09 2018 Kalev Lember <klember@redhat.com> - 0.52.1-1
- Update to 0.52.1

* Tue Apr 03 2018 Kalev Lember <klember@redhat.com> - 0.52.0-1
- Update to 0.52.0
- Remove ldconfig scriptlets

* Wed Mar 28 2018 Debarshi Ray <rishi@fedoraproject.org> - 0.51.90-1
- Update to 0.51.90

* Wed Mar 28 2018 Debarshi Ray <rishi@fedoraproject.org> - 0.51.3-1
- Update to 0.51.3
- Rebase downstream patches

* Thu Feb 08 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.50.2-3
- Switch to %%ldconfig_scriptlets

* Thu Nov 02 2017 Kalev Lember <klember@redhat.com> - 0.50.2-2
- Rebuild

* Wed Nov 01 2017 Debarshi Ray <rishi@fedoraproject.org> - 0.50.2-1
- Update to 0.50.2

* Thu Oct 05 2017 Debarshi Ray <rishi@fedoraproject.org> - 0.50.1-1
- Update to 0.50.1
- Rebase downstream patches

* Thu Sep 14 2017 Kalev Lember <klember@redhat.com> - 0.50.0-1
- Update to 0.50.0
- Rebase downstream patches

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.48.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.48.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 10 2017 Kalev Lember <klember@redhat.com> - 0.48.3-1
- Update to 0.48.3

* Wed Apr 12 2017 Kalev Lember <klember@redhat.com> - 0.48.2-1
- Update to 0.48.2
- Rebase downstream patches

* Wed Mar 22 2017 Kalev Lember <klember@redhat.com> - 0.48.1-1
- Update to 0.48.1

* Fri Feb 24 2017 Debarshi Ray <rishi@fedoraproject.org> - 0.47.90-1
- Update to 0.47.90
- Rebase downstream patches

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.46.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 08 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.46.1-1
- Update to 0.46.1
- Rebase downstream patches

* Thu Sep 22 2016 Kalev Lember <klember@redhat.com> - 0.46.0-2
- BR vala instead of obsolete vala-tools subpackage

* Mon Sep 19 2016 Kalev Lember <klember@redhat.com> - 0.46.0-1
- Update to 0.46.0

* Wed Sep 14 2016 Kalev Lember <klember@redhat.com> - 0.45.92-1
- Update to 0.45.92

* Thu Aug 18 2016 Kalev Lember <klember@redhat.com> - 0.45.90-1
- Update to 0.45.90
- Rebase downstream patches

* Fri Jul 01 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.44.2-2
- Add a property to configure the scroll speed

* Tue May 10 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.44.2-1
- Update to 0.44.2
- Rebase downstream patches and undo unintentional ABI break

* Mon Apr 11 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.44.1-1
- Update to 0.44.1

* Tue Mar 22 2016 Kalev Lember <klember@redhat.com> - 0.44.0-1
- Update to 0.44.0

* Tue Mar 15 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.43.92-1
- Update to 0.43.92

* Tue Mar 01 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.43.91-1
- Update to 0.43.91
- Remove BuildRequires on pkgconfig(libpcre2-8)

* Tue Mar 01 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.43.90-1
- Update to 0.43.90

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.43.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 29 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.43.2-1
- Update to 0.43.2

* Fri Jan 29 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.43.1-1
- Update to 0.43.1
- Drop upstreamed patch

* Fri Jan 29 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.43.0-1
- Update to 0.43.0
- Add BuildRequires on pkgconfig(libpcre2-8)
- Disable -Wnonnull

* Thu Jan 28 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.42.3-1
- Update to 0.42.3
- Backport upstream patch to fix disappearing lines (GNOME #761097)

* Wed Oct 14 2015 Kalev Lember <klember@redhat.com> - 0.42.1-1
- Update to 0.42.1

* Tue Sep 22 2015 Kalev Lember <klember@redhat.com> - 0.42.0-1
- Update to 0.42.0
- Use license macro for COPYING

* Mon Sep 14 2015 Debarshi Ray <rishi@fedoraproject.org> - 0.41.90-1
- Update to 0.41.90
- Rebased downstream patches after the migration to C++
- gnome-pty-helper has been removed

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.40.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 12 2015 Debarshi Ray <rishi@fedoraproject.org> - 0.40.2-1
- Update to 0.40.2

* Tue Mar 24 2015 Debarshi Ray <rishi@fedoraproject.org> - 0.40.0-1
- Update to 0.40.0

* Thu Mar 19 2015 Debarshi Ray <rishi@fedoraproject.org> - 0.39.92-1
- Update to 0.39.92

* Tue Feb 17 2015 Debarshi Ray <rishi@fedoraproject.org> - 0.39.90-1
- Update to 0.39.90
- Add command-notify patches

* Fri Dec 19 2014 Richard Hughes <rhughes@redhat.com> - 0.39.1-1
- Update to 0.39.1

* Mon Dec 01 2014 Debarshi Ray <rishi@fedoraproject.org> - 0.39.0-2
- Backport upstream patch to fix zombie shells (GNOME #740929)

* Tue Nov 25 2014 Kalev Lember <kalevlember@gmail.com> - 0.39.0-1
- Update to 0.39.0

* Mon Nov 10 2014 Kalev Lember <kalevlember@gmail.com> - 0.38.2-1
- Update to 0.38.2

* Mon Oct 13 2014 Kalev Lember <kalevlember@gmail.com> - 0.38.1-1
- Update to 0.38.1

* Sun Sep 14 2014 Kalev Lember <kalevlember@gmail.com> - 0.38.0-1
- Update to 0.38.0

* Mon Aug 18 2014 Kalev Lember <kalevlember@gmail.com> - 0.37.90-1
- Update to 0.37.90

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.37.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.37.2-2
- Rebuilt for gobject-introspection 1.41.4

* Tue Jun 24 2014 Richard Hughes <rhughes@redhat.com> - 0.37.2-1
- Update to 0.37.2

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.37.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 0.37.1-1
- Update to 0.37.1

* Wed May 07 2014 Kalev Lember <kalevlember@gmail.com> - 0.37.0-2
- Split out a vte-profile subpackage that can be used with both vte291 / vte3

* Tue May 06 2014 Kalev Lember <kalevlember@gmail.com> - 0.37.0-1
- Initial Fedora package, based on previous vte3 0.36 packaging
