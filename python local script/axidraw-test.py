from pyaxidraw import axidraw
import json
import paho.mqtt.client as mqtt

width = 0
height = 0
mousDownTracker = False


def draw(currX, currY, prevX, prevY, width, height, color, mouseDown):
    global mousDownTracker
    if mouseDown == True and mousDownTracker == False:
        ad.penup()
        ad.goto(currX / width * 6.3, currY / height * 4)
    if color == "rgb(240, 80, 42)":
        ad.penup()
    if color == "rgb(35, 111, 250)":
        if mouseDown:
            ad.pendown()
        else:
            ad.penup()
    ad.goto(currX / width * 6.3, currY / height * 4)
    mousDownTracker = mouseDown


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True  # set flag
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)


def on_message(client, userdata, message):
    global width, height
    print("message received ", str(message.payload.decode("utf-8")))
    coor = json.loads(str(message.payload.decode("utf-8")))
    width = coor["width"]
    height = coor["height"]

    draw(coor["currX"], coor["currY"], coor["prevX"], coor["prevY"], width, height, coor["color"], coor["mouseDown"])


broker_address = "farlab.infosci.cornell.edu"  # use external broker
client = mqtt.Client("Axi2")  # create new instance
client.tls_set()
client.on_connect = on_connect
client.on_message = on_message  # attach function to callback
client.username_pw_set("testuser", "far1@FAR")
try:
    client.connect(broker_address, 8883)  # connect to broker
except:
    print("connection failed")
    exit(1)  # Should quit or raise flag to quit or retry
print("Subscribing to topic", "Drawing")
client.subscribe("Drawing")
ad = axidraw.AxiDraw()
ad.interactive()
ad.connect()
ad.options.units = 0
ad.options.speed_penup = 80
ad.options.accel = 100
ad.moveto(0, 0)

client.loop_forever()  # Start loop

