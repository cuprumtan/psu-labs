from flask import Flask, render_template, Markup
from flask_socketio import SocketIO, emit
import json
import subprocess

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dder98342cuprumtan'
socketio = SocketIO(app)

def bash_get_servers():
    result_array = []
    proc = subprocess.Popen(["nmap -p 7071 192.168.0.* -oG - | grep 7071/open | awk '{print $2}'"], stdout=subprocess.PIPE, shell=True)
    (stdout, err) = proc.communicate()
    reader = stdout.decode('utf-8').splitlines()

    for row in reader:
        result_array.append(row)

    return result_array

@app.route('/')
def index():
    #servers_array = ["192.168.0.5", "192.168.0.6"]
    servers_array = bash_get_servers()
    servers_array = json.dumps(servers_array)
    return render_template('./index.html', servers_array=Markup(servers_array))

def message_recived():
    print('message was received')

@socketio.on('my event')
def handle_my_custom_event(json):
    print('recived my event: ' + str(json))
    socketio.emit('my response', json, callback=message_recived)

if __name__ == '__main__':
    socketio.run(app, debug=True)