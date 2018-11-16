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
