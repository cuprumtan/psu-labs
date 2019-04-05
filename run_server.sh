#!/bin/bash

#insert path
echo "Which folder will be shared?"
read folder
cd "$folder"

#start server
tmux new -s "python-http-server" -d
tmux send-keys -t "python-http-server" "python3 -m http.server 7070" C-m

#open web
xdg-open http://localhost:7070