%define kpatch_dnf_ver	0.4

Name:		kpatch
Version:	0.9.7
Release:	2%{?dist}
Summary:	Dynamic kernel patch manager

Group:		System Environment/Kernel
License:	GPLv2
URL:		https://github.com/dynup/kpatch
Source0:	https://github.com/dynup/kpatch/archive/v%{version}.tar.gz
Source1:	kpatch-dnf-v%{kpatch_dnf_ver}.tar.gz

# RHEL-only
Patch0:		0001-contrib-disable-upstart-kpatch.conf-install.patch
Patch1:		0002-kpatch-clarify-unload-unsupport.patch
Patch2:		0003-do-not-rm-selinux-rpm-owned-directory.patch

# Upstream backports
#Patch100:	0100-xxx.patch

# kpatch-dnf backports
#Patch200:	0200-xxx.patch

Requires:	bash kmod binutils
Recommends:	kpatch-dnf

BuildArch:	noarch


%description
kpatch is a live kernel patch module manager.  It allows the user to manage
a collection of binary kernel patch modules which can be used to dynamically
patch the kernel without rebooting.


%package -n kpatch-dnf
Summary:	kpatch-patch manager plugin for DNF
Version:	%{version}_%{kpatch_dnf_ver}
BuildRequires:	python3-devel python3-dnf
Requires:	python3-dnf python3-hawkey
Provides:	kpatch-dnf

%description -n kpatch-dnf
kpatch-dnf is a DNF plugin that manages subscription to kpatch-patch updates.
When enabled, kernel packages are automatically subscribed to corresponding
kpatch-patch packages updates.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%setup -D -T -a 1
cd kpatch-dnf-%{kpatch_dnf_ver}
cd ..

%build
make -C man

make -C kpatch-dnf-%{kpatch_dnf_ver}

%install
make install PREFIX=/usr DESTDIR=%{buildroot} -C kpatch
make install PREFIX=/usr DESTDIR=%{buildroot} -C man
make install PREFIX=/usr DESTDIR=%{buildroot} -C contrib
mkdir -p %{buildroot}/%{_sharedstatedir}/kpatch
rm -f %{buildroot}/usr/share/man/man1/kpatch-build.1.gz

make install PREFIX=/usr DESTDIR=%{buildroot} PYTHONSITES=%{python3_sitelib} -C kpatch-dnf-%{kpatch_dnf_ver}

%files
%{_sbindir}/kpatch
%{_usr}/lib/systemd/system/kpatch.service
%{_sharedstatedir}/kpatch
%doc %{_mandir}/man1/kpatch.1.gz

%files -n kpatch-dnf
%{python3_sitelib}/dnf-plugins/kpatch.py
%{python3_sitelib}/dnf-plugins/__pycache__
%config(noreplace) %{_sysconfdir}/dnf/plugins/kpatch.conf
%doc %{_mandir}/man8/dnf.kpatch.8.gz

%post -n kpatch-dnf
echo "To enable automatic kpatch-patch subscription, run:"
echo -e "\t$ dnf kpatch auto"

%changelog
* Wed Nov 16 2022 Yannick Cote <ycote@redhat.com> 0.9.7-2
- augment kpatch-dnf package versioning to satisfy build (rhbz#2121211)

* Wed Nov 09 2022 Yannick Cote <ycote@redhat.com> 0.9.7-1
- rebase kpatch user utility code to v0.9.7 (rhbz#2121211)

* Fri Jun 10 2022 Yannick Cote <ycote@redhat.com> 0.9.4-3
- Do not rm selinux rpm owned directory (rhbz#2065609)

* Fri Jan 14 2022 Yannick Cote <ycote@redhat.com> 0.9.4-2
- Add /usr/lib/kpatch to install and files list to appease SELinux (rhbz#2022123)

* Thu Sep 23 2021 Artem Savkov <asavkov@redhat.com> 0.9.4-1
- Update kpatch utility to 0.9.4 and kpatch-dnf to 0.4 (rhbz#2006841)

* Mon Mar 15 2021 Artem Savkov <asavkov@redhat.com> 0.9.2-5
- Cleanup /var/lib/kpatch directory on uninstall (rhbz#1930108)

* Thu Mar 11 2021 Joe Lawrence <joe.lawrence@redhat.com> 0.9.2-4
- Fix kpatch-dnf package description typos (rhbz#1934293)

* Mon Jan 04 2021 Julien Thierry <jthierry@redhat.com> 0.9.2-3
- Remove kpatch-dnf dependency on python3 (rhbz#1912224)

* Fri Nov 20 2020 Julien Thierry <jthierry@redhat.com> 0.9.2-2
- Fix unload issue under stress (rhbz#1883238)
- Fix dnf-kpatch man file permissions (rhbz#1899341)
- Do not replace dnf kpatch configuration file when reinstalling (rhbz#1898191)

* Thu Sep 24 2020 Julien Thierry <jthierry@redhat.com> 0.9.2-1
- Add kpatch-dnf subpackage (rhbz#1798711)

* Thu Sep 24 2020 Julien Thierry <jthierry@redhat.com> 0.9.2-1
- update to 0.9.2 (rhbz#1877857)

* Tue Oct 22 2019 Yannick Cote <ycote@redhat.com> 0.6.1-6
- fix patch loading issue caused by recent kernel rebase (rhbz#1754679)

* Wed Aug 28 2019 Joe Lawrence <joe.lawrence@redhat.com> 0.6.1-5
- kpatch: clarify that "kpatch unload" isn't supported (rhbz#1746461)

* Sun Jun 23 2019 Joe Lawrence <joe.lawrence@redhat.com> 0.6.1-4
- kpatch script: don't fail if module already loaded+enabled (rhbz#1719305)

* Wed Jun 12 2019 Joe Lawrence <joe.lawrence@redhat.com> 0.6.1-3
- kpatch: patches shouldn't be unloaded on system shutdown (rhbz#1719305)

* Wed Jun 5 2019 Josh Poimboeuf <jpoimboe@redhat.com> 0.6.1-2
- CI gating test (rhbz#1717417)

* Tue Aug 14 2018 Joe Lawrence <joe.lawrence@redhat.com> 0.6.1-1
- update to 0.6.1 (rhbz#1615880)

* Mon Aug 13 2018 Troy Dawson <tdawson@redhat.com> - 0.4.0-4
- Release Bumped for el8 Mass Rebuild

* Thu Nov 16 2017 Joe Lawrence <joe.lawrence@redhat.com> 0.4.0-3
- kpatch: better livepatch module support (rhbz#1504066)

* Wed Oct 18 2017 Josh Poimboeuf <jpoimboe@redhat.com> 0.4.0-2
- fix backwards compatibility with RHEL 7.3 patches (rhbz#1497735)

* Mon Mar 13 2017 Josh Poimboeuf <jpoimboe@redhat.com> 0.4.0-1
- update to 0.4.0 (rhbz#1427642)

* Wed Jun 15 2016 Josh Poimboeuf <jpoimboe@redhat.com> 0.3.2-1
- update to 0.3.2 (rhbz#1282508)

* Wed Nov 18 2015 Josh Poimboeuf <jpoimboe@redhat.com> 0.3.1-1
- update to 0.3.1 (rhbz#1282508)

* Tue Sep 16 2014 Seth Jennings <sjenning@redhat.com> 0.1.10-4
- fix dracut dependencies (rhbz#1170369)

* Tue Sep 16 2014 Seth Jennings <sjenning@redhat.com> 0.1.10-3
- support re-enabling forced modules (rhbz#1140268)

* Thu Sep 11 2014 Seth Jennings <sjenning@redhat.com> 0.1.10-2
- support modprobe format names (rhbz#1133045)

* Thu Jul 31 2014 Josh Poimboeuf <jpoimboe@redhat.com> 0.1.10-1
- update to kpatch 0.1.10

* Wed Jul 23 2014 Josh Poimboeuf <jpoimboe@redhat.com> 0.1.9-1
- update to kpatch 0.1.9

* Tue Jul 15 2014 Josh Poimboeuf <jpoimboe@redhat.com> 0.1.8-1
- update to kpatch 0.1.8

* Wed May 21 2014 Josh Poimboeuf <jpoimboe@redhat.com> 0.1.2-1
- update to kpatch 0.1.2

* Mon May 19 2014 Josh Poimboeuf <jpoimboe@redhat.com> 0.1.1-2
- fix initramfs core module path

* Mon May 19 2014 Josh Poimboeuf <jpoimboe@redhat.com> 0.1.1-1
- rebase to kpatch 0.1.1

* Fri May 9 2014 Josh Poimboeuf <jpoimboe@redhat.com> 0.1.0-2
- modprobe core module

* Tue May 6 2014 Josh Poimboeuf <jpoimboe@redhat.com> 0.1.0-1
- Initial kpatch release 0.1.0

* Thu Jan 30 2014 Josh Poimboeuf <jpoimboe@redhat.com> 0.0-1
- Initial build
