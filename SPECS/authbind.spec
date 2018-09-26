Summary:		Allow non-root users to open restricted ports
Name: 			authbind
Version: 		2.1.2
Release:		1%{?dist}
License: 		GPLv2
Group: 			Development/Tools
Source0:                http://ftp.debian.org/debian/pool/main/a/authbind/%{name}_%{version}.tar.gz
Patch0:			%{name}-%{version}-install.patch

%description
Authbind allows the system administrator to permit specific users and groups access to bind to TCP and UDP ports below 1024

%prep
%setup -q -n %{name}
# Clean up installation to use DESTDIR and not install as root
%patch0 -b .install
# Set prefix to use rpmmacro
sed -i.prefix 's|/usr/local|%{_prefix}|g' Makefile 
# Set libdir to use rpmmacro, not hardcoded /usr/local
sed -i.libdir 's|$(prefix)/lib/|$(prefix)/%{_lib}/|g' Makefile 
# Set etc_dir to use rpmmacro, not hardcoded /etc/authbind
sed -i.etcdirr 's|/etc/authbind/|%{_sysconfdir}/authbind|g' Makefile 
echo %{_sysconfdir}

%build
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sysconfdir}/authbind/byport
mkdir -p %{buildroot}%{_sysconfdir}/authbind/byaddr
mkdir -p %{buildroot}%{_sysconfdir}/authbind/byuid
make install DESTDIR=%{buildroot}
make install_man DESTDIR=%{buildroot}

%files
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/authbind
%attr(4755,root,root) %{_prefix}/%{_lib}/authbind/helper
%{_prefix}/%{_lib}/authbind/libauthbind.so.1
%{_prefix}/%{_lib}/authbind/libauthbind.so.1.0

%dir %{_sysconfdir}/authbind/byport
%dir %{_sysconfdir}/authbind/byaddr
%dir %{_sysconfdir}/authbind/byuid

%doc %attr(0444,root,root) %{_mandir}/man1/authbind.1*
%doc %attr(0444,root,root) %{_mandir}/man8/authbind-helper.8*

%changelog
* Sat Apr 15 2017 Billy Chan <shing@shing.cloud> - 2.1.2
- new release

* Sat Apr 18 2015 Nico Kadel-Garcia <nkadel@gmail.com> - 2.1.1
- Import from https://tootedom/authbind-centos-rpm configs
- Patch Makefile to not use 'install -o root -g root'
- Patch Makefile to use 'DESTDIR',
- Tweak Makefile in setup to use _prefix, _lib, and _sysconfdir values,
  avoids hardcoded /usr/local/, /usr/lib, and /etc
- Use .1* and .8* for man files, because of .gz autocompression
- Set byport, byaddr, and byuid as directories only
  
