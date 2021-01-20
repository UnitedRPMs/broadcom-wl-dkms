# This spec file is based on other projects and spec files (for compatiblity) PKGBUILDs, Sources available from
# https://aur.archlinux.org/packages/broadcom-wl-dkms-248
# https://github.com/rpmfusion/wl-kmod/blob/master/wl-kmod.spec (Some patches)
# https://madb.mageia.org/package/show/application/0/name/dkms-broadcom-wl
# http://xmodulo.com/build-kernel-module-dkms-linux.html (great guide about how to make modules with dkms)


%define debug_package %{nil}
%define oname	hybrid-v35
%define dwver	6_30_223_271
%define kname	wl
%global	realname broadcom-wl 

Summary:	Proprietary driver for Broadcom wireless adapters
Name:		broadcom-wl-dkms
Version:	6.30.223.271
Release:	12%{?dist}
Source0:	https://docs.broadcom.com/docs-and-downloads/docs/linux_sta/%{oname}-nodebug-pcoem-%{dwver}.tar.gz
Source1:	https://docs.broadcom.com/docs-and-downloads/docs/linux_sta/%{oname}_64-nodebug-pcoem-%{dwver}.tar.gz
Source2:	broadcom-wl-dkms.conf
Source3:	dkms.conf.in
Provides:	kmod(%{kname}.ko) = %{version}
Requires:	dkms
Requires:	kernel-devel
Conflicts:	wl-kmod broadcom-wl

Patch0:		license.patch
Patch1:		011-linux59.patch
Patch2:		wl-kmod-002_kernel_3.18_null_pointer.patch
Patch3:		wl-kmod-003_gcc_4.9_remove_TIME_DATE_macros.patch
Patch4:		wl-kmod-004_kernel_4.3_rdtscl_to_rdtsc.patch
Patch5:		wl-kmod-005_kernel_4.7_IEEE80211_BAND_to_NL80211_BAND.patch
Patch6:		wl-kmod-006_gcc_6_fix_indentation_warnings.patch
Patch7:		wl-kmod-007_kernel_4.8_add_cfg80211_scan_info_struct.patch
Patch8:		wl-kmod-008_fix_kernel_warnings.patch
Patch9:		wl-kmod-010_kernel_4.12_add_cfg80211_roam_info_struct.patch
Patch10:	wl-kmod-011_kernel_4.14_new_kernel_read_function_prototype.patch
Patch11:	008-linux415.patch
Patch12:	wl-kmod-016_fix_unsupported_mesh_point.patch
Patch13:	wl-kmod-017_kernel_5.6_adaptations.patch
Patch14:	wl-kmod-009_kernel_4.11_remove_last_rx_in_net_device_struct.patch

# Blob is under a custom license (see LICENSE.txt), everything else
# is GPLv2 - AdamW 2008/12
License:	Freeware and GPLv2 with exception
Group:		System/Kernel and hardware
URL:		http://www.broadcom.com/support/802.11/linux_sta.php

%description
This package contains the proprietary driver for Broadcom wireless
adapters provided by Broadcom. If installed, it will be used for
these cards in preference to the third-party open source driver that
requires manual installation of firmware, or ndiswrapper.

%prep
%ifarch x86_64
%setup -T -c -a1 %{oname} 
%else
%setup -T -c -a0 %{oname} 
%endif

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1


  sed -e "s/@PACKAGE_VERSION@/%{version}/" %{S:3} > dkms.conf

  sed -i -e "/BRCM_WLAN_IFNAME/s:eth:wlan:" src/wl/sys/wl_linux.c

  sed -i '/GE_49 :=/s|:= .*|:= 1|' Makefile
  

%build

%install
rm -rf %{buildroot}
pkgname=%{name}
dest=%{buildroot}/usr/src/${pkgname/-dkms/}-%{version}

  mkdir -p ${dest}
  cp -RL src lib Makefile dkms.conf ${dest}
  chmod a-x ${dest}/lib/LICENSE.txt # Ships with executable bits set

  mkdir -p %{buildroot}/usr/share/licenses/%{name}
  ln -rs ${dest}/lib/LICENSE.txt %{buildroot}/usr/share/licenses/%{name}/LICENSE

  install -D -m 644 %{S:2} %{buildroot}/etc/modprobe.d/broadcom-wl-dkms.conf

%post 

# rmmod can fail
/sbin/rmmod %{kname} >/dev/null 2>&1 ||:
set -x
/usr/sbin/dkms remove -m %{realname} -v %{version} -q --all || :
# now kdms install
/usr/sbin/dkms add -m %{realname} -v %{version} 
/usr/sbin/dkms build -m %{realname} -v %{version} 
/usr/sbin/dkms install -m %{realname} -v %{version} -q --force

%preun 
# rmmod can fail
/sbin/rmmod %{kname} >/dev/null 2>&1 ||:
set -x
/usr/sbin/dkms remove -m %{realname} -v %{version} -q --all || :

%clean
rm -rf %{buildroot}

%files 
%doc lib/LICENSE.txt
%{_datadir}/licenses/broadcom-wl-dkms/LICENSE
%dir %{_usr}/src/%{realname}-%{version}
%{_usr}/src/%{realname}-%{version}/*
%config %{_sysconfdir}/modprobe.d/%{name}.conf

%changelog

* Sun Jan 17 2021 - Unitedrpms Project <unitedrpms AT protonmail DOT com> 6.30.223.271-12
- Compatibility for kernel 5.10

* Wed Nov 11 2020 - Unitedrpms Project <unitedrpms AT protonmail DOT com> 6.30.223.271-11
- Compatibility for kernel 5.9 

* Fri Mar 20 2020 - Unitedrpms Project <unitedrpms AT protonmail DOT com> 6.30.223.271-10
- Compatibility for kernel 5.6 thanks to Glenn

* Mon Oct 14 2019 - Unitedrpms Project <unitedrpms AT protonmail DOT com> 6.30.223.271-9
- Modernized

* Sat Jun 01 2019 - Unitedrpms Project <unitedrpms AT protonmail DOT com> 6.30.223.271-7
- Added patch for the new wpa_supplicant
- Fixes for kernel 5.1

* Tue Jan 30 2018 - Unitedrpms Project <unitedrpms AT protonmail DOT com> 6.30.223.271-6
- Added patch for kernel >= 4.15 

* Wed Nov 29 2017 - Unitedrpms Project <unitedrpms AT protonmail DOT com> 6.30.223.271-5
- Added patch for kernel >= 4.14 

* Mon Aug 14 2017 - Unitedrpms Project <unitedrpms AT protonmail DOT com> 6.30.223.271-4
- Changes for an easy update

* Thu Jul 06 2017 - Unitedrpms Project <unitedrpms AT protonmail DOT com> 6.30.223.271-3
- Rework patch for kernel >= 4.12 - thanks to Tim Thomas

* Mon Jun 05 2017 - Unitedrpms Project <unitedrpms AT protonmail DOT com> 6.30.223.271-2
- Added patch for kernel >= 4.12 - add cfg80211_roam_info struct in wl_bss_roaming_done function

* Tue Apr 11 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  6.30.223.271-1
- Initial build
