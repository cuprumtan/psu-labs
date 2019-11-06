#!/bin/bash

#start server
tmux new -s "flask-file-server" -d
tmux send-keys -t "flask-file-server" "export FLASK_APP=../file_server/app.py" C-m
tmux send-keys -t "flask-file-server" "python -m flask run --host=0.0.0.0 --port=7071" C-m