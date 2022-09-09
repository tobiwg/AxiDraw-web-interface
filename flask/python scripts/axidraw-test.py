from pyaxidraw import axidraw
import json
import paho.mqtt.client as mqtt

width = 0
height = 0
mousDownTracker = False

def drawimg(path, w, h):
    ad.goto(0, 0)
    if path != "static/img/blank.jpg":
        if path == "static/img/home.svg":
            ad.interactive()
            ad.disconnect()
            ad.connect()  # Open serial port to AxiDraw
            ad.moveto(6.3, 0)  # Pen-up move to (1 inch, 1 inch)

        ad.plot_setup(path)
        ad.plot_run()
        ad.interactive()  # Enter interactive context
        ad.disconnect()
        ad.connect()  # Open serial port to AxiDraw
        ad.goto(0, 0)  # Pen-up move to (1 inch, 1 inch)


def draw(currX, currY, prevX, prevY, width, height, color, mouseDown):
    global mousDownTracker
    ad.interactive()  # Enter interactive context

    if mouseDown == True and mousDownTracker == False:  # check if the mouse is clicked and it wasnt clicked before (transition between draings)
        ad.penup()  # lift pen
        ad.goto(currX / width * 6.3, currY / height * 4)  # move to the new drawing location
    if color == "rgb(240, 80, 42)":  # if the color is red lift the pen
        ad.penup()
    if color == "rgb(35, 111, 250)":  # if the color is blue pen down if the mouse is clicked
        if mouseDown:
            ad.pendown()  # pen down
        else:
            ad.penup()  # lift pen
    ad.goto(currX / width * 6.3, currY / height * 4)  # move to the position normalized for the axidraw
    mousDownTracker = mouseDown


# onConnect event
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True  # set flag
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)


# new message event
def on_message(client, userdata, message):
    global width, height
    print("message received ", str(message.payload.decode("utf-8")))  # print incoming message
    msg = json.loads(str(message.payload.decode("utf-8")))  # decode JSON message
    width = msg["width"]  # get canva width in px
    height = msg["height"]  # get canva height in px
    if "path" in msg:
        drawimg(msg["path"], msg["width"], msg["height"])
    else:
        draw(msg["currX"], msg["currY"], msg["prevX"], msg["prevY"], width, height, msg["color"],
        msg["mouseDown"])  # send all the incoming data to the drawing function


broker_address = "farlab.infosci.cornell.edu"  # use external broker
client = mqtt.Client("Axi2")  # create new instance
client.tls_set()  # set tls for the mqtt connection
client.on_connect = on_connect  # attach function callback
client.on_message = on_message  # attach function to callback
client.username_pw_set("testuser", "far1@FAR")
try:
    client.connect(broker_address, 8883)  # connect to broker
except:
    print("connection failed")
    exit(1)  # Should quit or raise flag to quit or retry
print("Subscribing to topic", "Drawing")
client.subscribe("Drawing")  # subscribe to the topic

# create axidraw instance
ad = axidraw.AxiDraw()  # Initialize class
ad.interactive()  # Enter interactive context
ad.connect()  # Open serial port to AxiDraw
ad.options.units = 0  # units in inches
ad.options.speed_penup = 80  # pen up acceleration 80%
ad.options.accel = 100  # max acceleration 100%
ad.moveto(0, 0)  # Pen-up move to (1 inch, 1 inch)
ad.lineto(6.3, 0)  # Pen-down move, to (2 inch, 1 inch)
ad.lineto(6.3, 4)
ad.lineto(0, 4)
ad.lineto(0, 0)
ad.moveto(6.3, 0)
ad.penup()  # lift pen

client.loop_forever()  # Start loop
