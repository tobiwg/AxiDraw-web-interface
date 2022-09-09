from flask import Flask, render_template, Response
from flask_socketio import SocketIO, send, emit
import socket

import numpy as np
import cv2 as cv
port = 5501
cap = cv.VideoCapture(-1, cv.CAP_V4L)

app = Flask(__name__)
socketio = SocketIO(app)


def gen_frames():  
    first = True
    while True:
        success, frame = cap.read()  # read the camera frame
        frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
        if not success:
            break
        else:
            if first:
                gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                edges = cv.Canny(gray, 50, 200)
                contours, hierarchy = cv.findContours(edges.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
                sorted_contours = sorted(contours, key=cv.contourArea, reverse=True)
                largest_item = sorted_contours[0]
                max = np.amax(largest_item[:], axis=0)
                min = np.amin(largest_item, axis=0)
                first = False

            frame = frame[min[0][1]:max[0][1], min[0][0]:max[0][0]]
            ret, buffer = cv.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    #return "Hello! This is the home page <h1>HELLO</h1>"
    return render_template('index.html')

#app.run('10.56.129.2', port=port, debug=False)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))

if __name__ == '__main__':
 	#The way of getting the ip address is dumb but works https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
	print(f"access at http://{s.getsockname()[0]}:{port}")
	socketio.run(app, host='0.0.0.0', debug=True, port=port)


