#version=DEVEL
# System authorization information
auth --enableshadow --passalgo=sha512
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
rootpw --iscrypted $6$oZtcG0NcRbS7ZcZ7$FREGN6wLsHmpvPpwQVgHh26Bt7D7EujMVnOvEVWemvjpTNbP2eFq67yhcYe6hBaUJ1GUKvQRRrDwVrx7dQ5LE0
# System timezone
timezone America/New_York --isUtc
# X Window System configuration information
xconfig  --startxonboot
# System bootloader configuration
bootloader --append=" crashkernel=auto" --location=mbr --boot-drive=sda
autopart --type=lvm
# Partition clearing information
clearpart --all --initlabel --drives=sda

%packages
@^developer-workstation-environment
@base
@core
@debugging
@desktop-debugging
@development
@dial-up
@directory-client
@fonts
@gnome-apps
@gnome-desktop
@guest-desktop-agents
@input-methods
@internet-applications
@internet-browser
@java-platform
@multimedia
@network-file-system-client
@performance
@perl-runtime
@print-client
@ruby-runtime
@virtualization-client
@virtualization-hypervisor
@virtualization-tools
@web-server
@x11
kexec-tools

%end

%addon com_redhat_kdump --enable --reserve-mb='auto'

%end
