#!/bin/bash

#kill server
kill -9 $(lsof -t -i:7071)

#kill session
tmux kill-session -t "flask-file-server"