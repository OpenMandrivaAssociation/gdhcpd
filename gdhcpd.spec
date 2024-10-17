Summary:	A GTK+ administation tool for the ISC DHCPD server
Name:		gdhcpd
Version:	0.3.2
Release:	9
License:	GPLv2+
Group:		System/Configuration/Networking
URL:		https://www.gadmintools.org/
Source0:	http://mange.dynalias.org/linux/gdhcpd/%{name}-%{version}.tar.bz2
Source1:	%{name}.pam-0.77.bz2
Source2:	%{name}.pam.bz2
BuildRequires:	gtk+2-devel
BuildRequires:	imagemagick
Requires:	dhcp-server >= 3.0.1
Requires:	usermode-consoleonly

%description
GDHCPD is a fast and easy to use GTK+ administration tool for the
ISC DHCPD server.

%prep

%setup -q

bzcat %{SOURCE2} > %{name}.pam

%build

%configure2_5x

perl -pi -e 's|^#define DHCPD_BINARY .*|#define DHCPD_BINARY \"%{_sbindir}/dhcpd\"|g' config.h
perl -pi -e 's|^#define DHCPD_CONF .*|#define DHCPD_CONF \"%{_sysconfdir}/dhcpd.conf\"|g' config.h
perl -pi -e 's|^#define LEASE_FILE .*|#define LEASE_FILE \"%{_localstatedir}/lib/dhcp/dhcpd.leases\"|g' config.h

%make

%install
%makeinstall INSTALL_USER=`id -un` INSTALL_GROUP=`id -gn`

# pam auth
install -d %{buildroot}%{_sysconfdir}/pam.d/
install -d %{buildroot}%{_sysconfdir}/security/console.apps

install -m 644 %{name}.pam %{buildroot}%{_sysconfdir}/pam.d/%{name}
install -m 644 etc/security/console.apps/%{name} %{buildroot}%{_sysconfdir}/security/console.apps/%{name}

# locales
%find_lang %name

# Mandriva Icons
install -d %{buildroot}%{_iconsdir}
install -d %{buildroot}%{_miconsdir}
install -d %{buildroot}%{_liconsdir}
convert -geometry 48x48 pixmaps/gdhcpd.png %{buildroot}%{_liconsdir}/%{name}.png
convert -geometry 32x32 pixmaps/gdhcpd.png %{buildroot}%{_iconsdir}/%{name}.png
convert -geometry 16x16 pixmaps/gdhcpd.png %{buildroot}%{_miconsdir}/%{name}.png

# Mandriva Menus
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=GDHCPD
Comment=%{summary}
Exec=%{_sbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Settings;Network;GTK;
EOF

# Prepare usermode entry
mv %{buildroot}%{_sbindir}/gdhcpd %{buildroot}%{_sbindir}/gdhcpd.real
ln -s %{_bindir}/consolehelper %{buildroot}%{_sbindir}/gdhcpd

mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
cat > %{buildroot}%{_sysconfdir}/security/console.apps/%{name} <<_EOF_
USER=root
PROGRAM=%{_sbindir}/gdhcpd.real
SESSION=true
FALLBACK=false
_EOF_

rm -rf %{buildroot}%{_datadir}/doc/%{name}

%files -f %{name}.lang
%defattr(-,root,root,0755)
%doc COPYING AUTHORS ChangeLog
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}
%{_sbindir}/%{name}
%{_sbindir}/%{name}.real
%{_datadir}/applications/mandriva-%{name}.desktop
%{_datadir}/pixmaps/*.png
%{_datadir}/pixmaps/%{name}/*.png
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png


%changelog
* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 0.3.2-7mdv2011.0
+ Revision: 618444
- the mass rebuild of 2010.0 packages

* Wed Sep 09 2009 Thierry Vignaud <tv@mandriva.org> 0.3.2-6mdv2010.0
+ Revision: 435960
- rebuild
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Fri Dec 14 2007 Thierry Vignaud <tv@mandriva.org> 0.3.2-3mdv2008.1
+ Revision: 119754
- fix summary

* Fri Dec 14 2007 Funda Wang <fwang@mandriva.org> 0.3.2-2mdv2008.1
+ Revision: 119612
- drop old menu

  + Thierry Vignaud <tv@mandriva.org>
    - s/Mandrake/Mandriva/

* Tue Jul 17 2007 Jérôme Soyer <saispo@mandriva.org> 0.3.2-1mdv2008.0
+ Revision: 53105
- New release 0.3.2


* Fri Mar 16 2007 Nicolas Lécureuil <neoclust@mandriva.org> 0.3.1-2mdv2007.1
+ Revision: 145071
- Fix menu file

* Wed Jan 03 2007 Emmanuel Andry <eandry@mandriva.org> 0.3.1-1mdv2007.1
+ Revision: 103922
- New version 0.3.1
  xdg menu
- Import gdhcpd

* Fri Mar 31 2006 Oden Eriksson <oeriksson@mandriva.com> 0.2.9-1mdk
- 0.2.9 (Minor feature enhancements)

* Sun Mar 05 2006 Oden Eriksson <oeriksson@mandriva.com> 0.2.8-2mdk
- fix url
- make it backportable for older pam (S1,S2)
- fix correct path to the leases file

* Tue Jun 07 2005 Oden Eriksson <oeriksson@mandriva.com> 0.2.8-1mdk
- 0.2.8
- drop P0, use spec file hacks instead...

* Wed Apr 13 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.2.7-1mdk
- 0.2.7

* Fri Mar 18 2005 Austin Acton <austin@mandrake.org> 0.2.4-1mdk
- New release 0.2.4

* Tue Feb 15 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.2.3-1mdk
- 0.2.3

* Mon Jan 17 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.2.2-1mdk
- 0.2.2

* Sat Jan 08 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.2.1-1mdk
- 0.2.1

* Fri Dec 31 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.2.0-2mdk
- fix one rpmlint error

* Fri Dec 31 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.2.0-1mdk
- initial mandrake package, used the gproftpd spec file as a start
- added P0

