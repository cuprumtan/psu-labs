#!/bin/bash

#get yout IP-mask
myaddr=$(ip route get 1.2.3.4 | awk '{print $7}')
myaddr=$(echo "$myaddr"| awk 'BEGIN{FS=OFS="."} NF--')
myaddr="$myaddr.*"

#use nmap to search open 7070 ports
conn=$(nmap -p7070 $myaddr -oG - | grep 7070/open | awk '{print $2}')

#create connection url
conn="http://$conn:7070"

#open server
xdg-open "$conn"