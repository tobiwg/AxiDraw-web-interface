from pyaxidraw import axidraw
import json
import paho.mqtt.client as mqtt

width = 0
height = 0
mousDownTracker = False


def draw(currX, currY, prevX, prevY, width, height, color, mouseDown):
    global mousDownTracker
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
    coor = json.loads(str(message.payload.decode("utf-8")))  # decode JSON message
    width = coor["width"]  # get canva width in px
    height = coor["height"]  # get canva height in px
    draw(coor["currX"], coor["currY"], coor["prevX"], coor["prevY"], width, height, coor["color"],
         coor["mouseDown"])  # send all the incoming data to the drawing function


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

client.loop_forever()  # Start loop
