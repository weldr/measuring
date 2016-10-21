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
rootpw --iscrypted $6$lREpjvaz5i1qQgjW$xbkCrWakaEmwwv5kKN7UmIQzFWu16GFISHcJ44VgtCklo.gdSyAF847UAVtgO8vRlzxMcpPRd2V2pzDqwPOoi1
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
@^gnome-desktop-environment
@base
@core
@desktop-debugging
@dial-up
@directory-client
@fonts
@gnome-desktop
@guest-desktop-agents
@input-methods
@internet-browser
@java-platform
@multimedia
@network-file-system-client
@networkmanager-submodules
@print-client
@x11
kexec-tools

%end

%addon com_redhat_kdump --enable --reserve-mb='auto'

%end
