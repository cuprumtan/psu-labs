#!/bin/bash

#get package manager
declare -A osInfo;
osInfo[/etc/redhat-release]=yum
osInfo[/etc/arch-release]=pacman
osInfo[/etc/gentoo-release]=emerge
osInfo[/etc/SuSE-release]=zypper
osInfo[/etc/debian_version]=apt-get

for f in ${!osInfo[@]}
do
    if [[ -f $f ]];then
        manager=${osInfo[$f]}
    fi
done

#install packages
echo "Program needs some packages, please, give us a little root:"
echo ""
echo "Start upgrading packages..."
echo ""

case "$manager" in
	"yum") 	   sudo yum -y install tmux lsof python3 nmap;;
	"pacman" )  sudo pacman -S --noconfirm tmux lsof python3 nmap;;
	"emerge" )  sudo emerge tmux lsof python3 nmap;;
	"zypper" )  sudo zypper install tmux lsof python3 nmap;;
	"apt-get" ) sudo apt-get -y install tmux lsof python3 nmap;;
esac

echo ""
echo "Thank U! Program is ready to run."