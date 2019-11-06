#!/bin/bash

#kill server
kill -9 $(lsof -t -i:7070)

#kill session
tmux kill-session -t "flask-chat-server" 
