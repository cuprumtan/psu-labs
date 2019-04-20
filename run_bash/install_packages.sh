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
	"yum") 	    sudo yum -y install tmux lsof python3 nmap
				sudo pip3 install flask flask.views werkzeug flask_socketio datetime humanize;;
	"pacman" )  sudo pacman -S --noconfirm tmux lsof python3 nmap
				sudo pip3 install flask flask.views werkzeug flask_socketio datetime humanize;;
	"emerge" )  sudo emerge tmux lsof python3 nmap
				sudo pip3 install flask flask.views werkzeug flask_socketio datetime humanize;;
	"zypper" )  sudo zypper install tmux lsof python3 nmap
				sudo pip3 install flask flask.views werkzeu flask_socketio datetime humanize;;
	"apt-get" ) sudo apt-get -y install tmux lsof python3 nmap
				sudo pip3 install flask flask.views werkzeug flask_socketio datetime humanize;;
esac

echo ""
echo "Thank U! Program is ready to run."