#!/bin/bash

# print your ip addr

myaddr=$(ip route get 1.2.3.4 | awk '{print $7}')
echo "$myaddr"