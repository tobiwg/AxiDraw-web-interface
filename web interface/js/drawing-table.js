	var canvas, context, color, prevX = 0,
        currX = 0,
        prevY = 0,
        currY = 0;
	var lastEvent;
	var mouseDown = false;
	var flag=false;

 function init() {
	canvas = document.getElementById('can');
	context = canvas.getContext("2d");
	color = $(".selected").css("background-color");
	canvas.width = $("#can").width(); //document.width is obsolete
    canvas.height = $("#can").height(); //document.height is obsolete
	w = canvas.width;
    h = canvas.height;
	canvas.addEventListener('pointerdown', function(e) {
	lastEvent = e;
	mouseDown = true;
	prevX = currX;
	prevY = currY;  
	currX = e.clientX - canvas.offsetLeft;
	currY = e.clientY - canvas.offsetTop;
	context.moveTo(currX, currY);
	});
	canvas.addEventListener('pointermove',function(e){
		if(mouseDown){
			prevX = currX;
			prevY = currY;
			currX = e.clientX - canvas.offsetLeft;
            currY = e.clientY - canvas.offsetTop;
			context.beginPath();
			context.moveTo(prevX, prevY);
			context.lineTo(currX, currY);
			context.strokeStyle = color;
			context.stroke();
			lastEvent = e;
			send(currX,currY, prevX,prevY,color,mouseDown);
			flag=true;
		}
	
	});
	canvas.addEventListener('pointerup',function(){
		mouseDown = false;
		if(flag){
			send(currX,currY, prevX,prevY,color,mouseDown);
		}
	});
	canvas.addEventListener('pointerout',function(){
		mouseDown = false;
		if(flag){
			send(currX,currY, prevX,prevY,color,mouseDown);
		}
	}); 
	// show border on clicked color
	$("#controls").on("click", "li", function(){
		$(this).siblings().removeClass("selected");
		$(this).addClass("selected");
		color = $(this).css("background-color");
		
	});
}
function send(currX, currY, prevX, prevY, color, mouseDown){
        coor={"width":w,"height":h,"currX": currX,"currY":currY,"prevX":prevX,"prevY":prevY,"color":color, "mouseDown":mouseDown};
		console.log(coor);
        client.subscribe("Drawing");
        message = new Paho.MQTT.Message(JSON.stringify(coor));
        message.destinationName = "Drawing";
        client.send(message);
        console.log("message sent: "+ coor);
}
    
        
// Create a client instance
client = new Paho.MQTT.Client("farlab.infosci.cornell.edu", 8083 , "DrawingPad");

// set callback handlers
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

// connect the client
client.connect( {onSuccess:onConnect, userName : "testuser", password : "far1@FAR", useSSL:true});


// called when the client connects
function onConnect() {
  // Once a connection has been made, make a subscription and send a message.
  console.log("onConnect");
  client.subscribe("Drawing");
  //message = new Paho.MQTT.Message(JSON.stringify({"width":w,"height":h}));
  //message.destinationName = "Drawing";
  //client.send(message);
}

// called when the client loses its connection
function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:"+responseObject.errorMessage);
  }
}

// called when a message arrives
function onMessageArrived(message) {
  console.log("onMessageArrived:"+message.payloadString);
}
    
