#!/bin/bash

#start chat
tmux new -s "flask-chat-server" -d
tmux send-keys -t "flask-chat-server" "export FLASK_APP=../chat_server/app.py" C-m
tmux send-keys -t "flask-chat-server" "python -m flask run --host=0.0.0.0 --port=7070" C-m