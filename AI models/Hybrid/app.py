from __future__ import print_function

from datetime import time

from flask import Flask, render_template, send_from_directory, request
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_url_path='')
socketio = SocketIO(app)

adminDetails = {"name": "admin", "id": "0"}
setarr = set([])

@app.route('/')
def main():
    return render_template('hybrid.html')


@app.route('/display/')
def display():
    return render_template('display.html')


@app.route("/complaints")
def addC():
    id = str(request.args.get('stud'))
    setarr.add(id)
    print(setarr)
    return "SUCCESS";

@app.route("/get")
def send():
    return str(setarr);

@socketio.on("predictionData")
def prediction(predictionData):
    if adminDetails['id'] != 0:
        socketio.emit('studentPrediction', {'data': predictionData}, adminDetails['id'])

@socketio.on("admin")
def Admin(data):
    adminDetails['name'] = (data['data']['name'])
    adminDetails['id'] = request.sid

if __name__ == "__main__":
    app.run(debug=True)
