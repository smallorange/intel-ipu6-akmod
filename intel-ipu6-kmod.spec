%if 0%{?fedora}
%global buildforkernels akmod
%global debug_package %{nil}
%endif

%global prjname intel-ipu6

Name:           %{prjname}-kmod
Summary:        Kernel module (kmod) for %{prjname}
Version:        0.0.1
Release:        3%{?dist}
License:        GPLv2+

URL:            https://github.com/smallorange
Source0:        ${url}/ivsc-driver/releases/download/%{version}/ivsc-driver-%{version}.tar.xz
Source1:        ${url}/ipu6-drivers/releases/download/%{version}/ipu6-drivers-%{version}.tar.xz

# Patches
# iVSC 
Patch0:         0001-mfd-ljca-Fix-BUG-sleeping-function-called-from-inval.patch
Patch1:         0002-i2c-ljca-Call-acpi_dev_clear_dependencies.patch

# IPU6
Patch10:        0001-Makefile-Disable-Wtype-limits-warnings.patch
Patch11:        0002-ipu6-ipu_isys-psys_init-Fix-error-propagation.patch
Patch12:        0003-ipu6-ipu_pci_probe-Fix-crash-on-ipu_psys_init-failur.patch  
Patch13:        0004-ipu6-ipu_pci_probe-Fix-Runtime-PM-usage-count-underf.patch
Patch14:        0005-ipu-bus-Split-ipu_bus_add_device-into-initialize-add.patch
Patch15:        0006-ipu-bus-Fix-ipu_bus_device-memory-management.patch


BuildRequires:  gcc
BuildRequires:  elfutils-libelf-devel
BuildRequires:  kmodtool  
%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{prjname} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
This enables intel IPU6 image processor. 

This package contains the kmod module for %{prjname}.


%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu} --repo rpmfusion --kmodname %{prjname} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -a 1
(cd ivsc-driver-%{version}
%patch0 -p1
%patch1 -p1
cd ../ipu6-drivers-%{version}
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
)

cp -Rp ivsc-driver-%{version}/backport-include ipu6-drivers-%{version}/
cp -Rp ivsc-driver-%{version}/drivers ipu6-drivers-%{version}/
cp -Rp ivsc-driver-%{version}/include ipu6-drivers-%{version}/

for kernel_version  in %{?kernel_versions} ; do
  cp -a ipu6-drivers-%{version}/ _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version  in %{?kernel_versions} ; do
  make V=1 %{?_smp_mflags} -C ${kernel_version##*___} M=${PWD}/_kmod_build_${kernel_version%%___*} modules
done

%install
for kernel_version in %{?kernel_versions}; do
 mkdir -p %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 install -D -m 755 _kmod_build_${kernel_version%%___*}/drivers/media/i2c/hi556.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/drivers/media/i2c/hi556.ko
 install -D -m 755 _kmod_build_${kernel_version%%___*}/drivers/media/i2c/hm11b1.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/drivers/media/i2c/hm11b1.ko
 install -D -m 755 _kmod_build_${kernel_version%%___*}/drivers/media/i2c/hm2170.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/drivers/media/i2c/hm2170.ko
 install -D -m 755 _kmod_build_${kernel_version%%___*}/drivers/media/i2c/ov01a10.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/drivers/media/i2c/ov01a10.ko
 install -D -m 755 _kmod_build_${kernel_version%%___*}/drivers/media/i2c/ov01a1s.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/drivers/media/i2c/ov01a1s.ko
 install -D -m 755 _kmod_build_${kernel_version%%___*}/drivers/media/i2c/ov02c10.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/drivers/media/i2c/ov02c10.ko
 install -D -m 755 _kmod_build_${kernel_version%%___*}/drivers/media/i2c/ov2740.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/drivers/media/i2c/ov2740.ko
 install -D -m 755 _kmod_build_${kernel_version%%___*}/drivers/media/pci/intel/ipu6/intel-ipu6-isys.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/drivers/media/pci/intel/ipu6/intel-ipu6-isys.ko
 install -D -m 755 _kmod_build_${kernel_version%%___*}/drivers/media/pci/intel/ipu6/intel-ipu6-psys.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/drivers/media/pci/intel/ipu6/intel-ipu6-psys.ko
 install -D -m 755 _kmod_build_${kernel_version%%___*}/drivers/media/pci/intel/ipu6/intel-ipu6.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/drivers/media/pci/intel/ipu6/intel-ipu6.ko
 install -D -m 755 _kmod_build_${kernel_version%%___*}/gpio-ljca.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/gpio-ljca.ko
 install -D -m 755 _kmod_build_${kernel_version%%___*}/i2c-ljca.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/i2c-ljca.ko
 install -D -m 755 _kmod_build_${kernel_version%%___*}/intel_vsc.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/intel_vsc.ko
 install -D -m 755 _kmod_build_${kernel_version%%___*}/ljca.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/ljca.ko
 install -D -m 755 _kmod_build_${kernel_version%%___*}/mei-vsc.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/mei-vsc.ko
 install -D -m 755 _kmod_build_${kernel_version%%___*}/mei_ace.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/mei_ace.ko
 install -D -m 755 _kmod_build_${kernel_version%%___*}/mei_ace_debug.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/mei_ace_debug.ko
 install -D -m 755 _kmod_build_${kernel_version%%___*}/mei_csi.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/mei_csi.ko
 install -D -m 755 _kmod_build_${kernel_version%%___*}/mei_pse.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/mei_pse.ko
 install -D -m 755 _kmod_build_${kernel_version%%___*}/spi-ljca.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/spi-ljca.ko
 chmod a+x %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/*.ko
done
%{?akmod_install}


%changelog
* Wed Oct 26 2022 Kate Hsuan <hpa@redhat.com> - 0.0.1
- First release