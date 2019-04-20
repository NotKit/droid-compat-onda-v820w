# The real device details.
%define device v820w
%define device_codename v820w

# The device details of the actual HW adaptation we rely upon
%define adaptation_device tbj
%define adaptation_device_codename tbj
#define adaptation_device f5321
#define adaptation_device_codename kugo

# Various settings
%define patch_kernel 0

%define divert_flash_partition_device_info 1
%define custom_flash_partition_device_info_path "/usr/lib/droid-compat/flash-partition/device-info"

%include droid-compat-device/droid-compat-device.inc

%post droid-hal
for diversion in $(cat %{divert_base_path}/droid-hal.manifest); do
	action="copy"
	rpm-divert add \
		droid-compat-%{rpm_device}-droid-hal \
		${diversion} \
		/var/lib/diversions/${diversion}.diverted \
		--action ${action} \
		--replacement %{divert_base_path}/${diversion}
done

rpm-divert apply --package droid-compat-%{rpm_device}-droid-hal --create-directory

%preun droid-hal
if [ $1 -eq 0 ]; then
	# As on RPM-based systems the installation scriptlets of the upgrade
	# are executed _before_ removing the old version (thus executing this
	# postun scriplet at the end of the transaction), we are going to
	# unapply the diversions only on package removals.
	rpm-divert unapply --package droid-compat-%{rpm_device}-droid-hal

	for diversion in $(cat %{divert_base_path}/droid-hal.manifest); do
		rpm-divert remove \
			droid-compat-%{rpm_device}-droid-hal \
			${diversion}
	done
fi

%triggerin droid-hal -- droid-hal-%{rpm_adaptation_device}
if [ $2 -gt 1 ]; then
	# On upgrades, unapply the triggers so that when rpm will put the
	# upgraded files back in will not overwrite the diversion symlinks
	rpm-divert unapply --package droid-compat-%{rpm_device}-droid-hal
fi

%triggerun droid-hal -- droid-hal-%{rpm_adaptation_device}
if [ $1 -gt 0 ] && [ $2 -gt 0 ]; then
	# Now that the upgrade files are in their place, it is time to re-apply
	# the diversions
	rpm-divert apply --package droid-compat-%{rpm_device}-droid-hal --create-directory
fi
