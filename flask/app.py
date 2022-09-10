from flask import Flask, render_template, Response
from flask_socketio import SocketIO, send, emit
import socket
import numpy as np
import cv2 
import sys
import time
port = 5500
webCam = False
app = Flask(__name__)
socketio = SocketIO(app)

if not webCam:
    print("Trying to open the Webcam.")
    cap = cv2.VideoCapture(-1)
    webCam = True
    if cap is None or not cap.isOpened():
        raise("No camera")
    
else:
    print("camera already opened")
    

def gen_frames():  
    first = True
    while True:
        if webCam:
            ret, frame = cap.read() # read the camera frame
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        if not ret:
            break
        else:
            if first:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                edges = cv2.Canny(gray, 50, 200)
                contours, hierarchy = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
                largest_item = sorted_contours[0]
                max = np.amax(largest_item[:], axis=0)
                min = np.amin(largest_item, axis=0)
                first = False

            frame = frame[min[0][1]:max[0][1], min[0][0]:max[0][0]]
            ret, buffer = cv2.imencode('.jpg', frame)
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
        app.run('10.56.129.2', port=port, debug=False)
#        socketio.run(app, host='0.0.0.0', debug=False, port=port)


