#version=DEVEL
# System authorization information
auth --enableshadow --passalgo=sha512
repo --name="Server-HighAvailability" --baseurl=file:///run/install/repo/addons/HighAvailability
repo --name="Server-ResilientStorage" --baseurl=file:///run/install/repo/addons/ResilientStorage
# Use CDROM installation media
cdrom
# Use graphical install
graphical
# Run the Setup Agent on first boot
firstboot --enable
ignoredisk --only-use=sda
# Keyboard layouts
keyboard --vckeymap=us --xlayouts='us'
# System language
lang en_US.UTF-8

# Network information
network  --bootproto=dhcp --device=enp0s2 --onboot=off --ipv6=auto
network  --hostname=localhost.localdomain

# Root password
rootpw --iscrypted $6$rYrGQ/4IalSzI7iw$lLSUUpeXyyYF7UezwA64PoqFTUfGJ4hMCY/RzL5F2vHx3.CovHeiUkGyrUrHYWxXvTyYw2eGEg14pueDPv29e0
# System timezone
timezone America/New_York --isUtc
# System bootloader configuration
bootloader --append=" crashkernel=auto" --location=mbr --boot-drive=sda
autopart --type=lvm
# Partition clearing information
clearpart --all --initlabel --drives=sda

%packages
@^web-server-environment
@base
@core
@web-server
kexec-tools

%end

%addon com_redhat_kdump --enable --reserve-mb='auto'

%end
