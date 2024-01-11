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

# Upstream backports (inactive -- for future reference)
#Patch100:	0100-xxx.patch

# kpatch-dnf backports (inactive -- for future reference)
#Patch200:	0200-foo-bar-etcetera.patch

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
# Use this to apply upstream patches to kpatch
#%patch100 -p1

%setup -D -T -a 1

# Use this to apply patches to kpatch-dnf (inactive)
#cd kpatch-dnf-%{kpatch_dnf_ver}
#%patch200 -p1
#cd ..

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
- augment kpatch-dnf package versioning to satisfy build (rhbz#2121212)

* Wed Nov 09 2022 Yannick Cote <ycote@redhat.com> 0.9.7-1
- rebase kpatch user utility code to v0.9.7 (rhbz#2121212)

* Fri Jun 10 2022 Yannick Cote <ycote@redhat.com> 0.9.4-3
- Do not rm selinux rpm owned directory (rhbz#2053413)

* Thu Jan 27 2022 Yannick Cote <ycote@redhat.com> 0.9.4-2
- Add /usr/lib/kpatch to install and files list to appease SELinux (rhbz#2030004)

* Wed Sep 29 2021 Artem Savkov <asavkov@redhat.com> - 0.9.4-1
- Rebase to 0.9.4

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 0.9.3-3
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Thu Jun 10 2021 Joe Lawrence <joe.lawrence@redhat.com> - 0.9.3-2
- Rebase to latest upstream (via backport patch)

* Tue May 18 2021 Joel Savitz <jsavitz@redhat.com> - 0.9.3-1
- Rebase to latest upstream

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 0.9.2-5
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Fri Mar 05 2021 Joe Lawrence <joe.lawrence@redhat.com> 0.9.2-4
- Fix kpatch-dnf package description typos (rhbz#1934292)

* Mon Jan 04 2021 Julien Thierry <jthierry@redhat.com> 0.9.2-2
- Remove kpatch-dnf dependency on python3 (rhbz#1912457)

* Wed Dec 2 2020 Joe Lawrence <joe.lawrence@redhat.com> 0.9.2-1
- initial kpatch utility build for rhel-9.0.0 (rhbz#1901593)
