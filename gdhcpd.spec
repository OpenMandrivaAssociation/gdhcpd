Summary:	GDHCPD -- A GTK+ administation tool for the ISC DHCPD server
Name:		gdhcpd
Version:	0.3.1
Release:	%mkrel 2
License:	GPL
Group:		System/Configuration/Networking
URL:		http://www.gadmintools.org/
Source0:	http://mange.dynalias.org/linux/gdhcpd/%{name}-%{version}.tar.bz2
Source1:	%{name}.pam-0.77.bz2
Source2:	%{name}.pam.bz2
BuildRequires:	gtk+2-devel
BuildRequires:	ImageMagick
Requires:	dhcp-server >= 3.0.1
Requires:	usermode-consoleonly
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
GDHCPD is a fast and easy to use GTK+ administration tool for the
ISC DHCPD server.

%prep

%setup -q

# fix conditional pam config file
%if %{mdkversion} < 200610
bzcat %{SOURCE1} > %{name}.pam
%else
bzcat %{SOURCE2} > %{name}.pam
%endif

%build

%configure2_5x

perl -pi -e 's|^#define DHCPD_BINARY .*|#define DHCPD_BINARY \"%{_sbindir}/dhcpd\"|g' config.h
perl -pi -e 's|^#define DHCPD_CONF .*|#define DHCPD_CONF \"%{_sysconfdir}/dhcpd.conf\"|g' config.h
perl -pi -e 's|^#define LEASE_FILE .*|#define LEASE_FILE \"%{_localstatedir}/dhcp/dhcpd.leases\"|g' config.h

%make

%install
rm -rf %{buildroot}

%makeinstall INSTALL_USER=`id -un` INSTALL_GROUP=`id -gn`

# pam auth
install -d %{buildroot}%{_sysconfdir}/pam.d/
install -d %{buildroot}%{_sysconfdir}/security/console.apps

install -m 644 %{name}.pam %{buildroot}%{_sysconfdir}/pam.d/%{name}
install -m 644 etc/security/console.apps/%{name} %{buildroot}%{_sysconfdir}/security/console.apps/%{name}

# locales
%find_lang %name

# Mandrake Icons
install -d %{buildroot}%{_iconsdir}
install -d %{buildroot}%{_miconsdir}
install -d %{buildroot}%{_liconsdir}
convert -geometry 48x48 pixmaps/gdhcpd.png %{buildroot}%{_liconsdir}/%{name}.png
convert -geometry 32x32 pixmaps/gdhcpd.png %{buildroot}%{_iconsdir}/%{name}.png
convert -geometry 16x16 pixmaps/gdhcpd.png %{buildroot}%{_miconsdir}/%{name}.png

# Mandrake Menus
install -d %{buildroot}/%{_menudir}
cat > %{buildroot}%{_menudir}/%{name} <<EOF
?package(%{name}): \
 command="%{_sbindir}/%{name}" \
 title="GDHCPD" \
 longtitle="ISC DHCPD server administration tool" \
 needs="x11" \
 icon="%{name}.png" \
 section="Configuration/Networking" \
 xdg="true" 
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=GDHCPD
Comment=%{summary}
Exec=%{_sbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-System-Configuration-Networking;Settings;Network;
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

%post
%update_menus

%postun
%clean_menus

%clean
rm -rf %{buildroot}

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
%{_datadir}/pixmaps/%{name}/%{name}.png
%{_menudir}/%{name}
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png


