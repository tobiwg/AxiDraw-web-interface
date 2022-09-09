	var canvas, context, color, prevX = 0, canvas_back, ctx
        currX = 0,
        prevY = 0,
        currY = 0;
	var lastEvent;
	var mouseDown = false;
	var flag=false;
//init function will be executed when the body of the webpage is loaded
 function init() {
				canvas = document.getElementById('can2'); //get the canva element
				context = canvas.getContext("2d");
			//	canvas_back = document.getElementById('can1'); //get the canva element
				//ctx = canvas_back.getContext("2d");
				color = $(".selected").css("background-color"); //get selected color
				canvas.width = $("#can2").width(); //set canva width
				canvas.height = $("#can2").height(); //set canva height
				w = canvas.width; //store canva width
				h = canvas.height; //store canv height
				setInterval(loadBackground, 1500);
				//listener to the click or pointerdown event
				var background = new Image();
				background.src = "img/savedImage.jpg";
				
				// Make sure the image is loaded first otherwise nothing will draw.
				background.onload = function(){
						//		context.drawImage(background,0,0);   
				}
				canvas.addEventListener('pointerdown', function(e) {
						lastEvent = e;
						mouseDown = true; //set mause click to true
						prevX = currX; //save last position X
						prevY = currY; //save last position Y
						currX = e.clientX - canvas.offsetLeft; //get new position X
						currY = e.clientY - canvas.offsetTop; //get new position in Y
						context.moveTo(currX, currY); //move to the current position to start drawing
				});
				//listener mouse/pen move event
				canvas.addEventListener('pointermove',function(e){
					if(mouseDown){ //if we move and we are clicking this will be true 
						prevX = currX; //save last position X
						prevY = currY; //save last position Y
						currX = e.clientX - canvas.offsetLeft; //get new position X
						currY = e.clientY - canvas.offsetTop; //get new position in Y
						context.beginPath(); //start the drawing
						context.moveTo(prevX, prevY); //move to the previus position to start drawing (i think this line is not needed)
						context.lineTo(currX, currY); //make a line to the current position
						context.strokeStyle = color; //set color
						context.stroke();
						lastEvent = e;
						send(currX,currY, prevX,prevY,color,mouseDown); //send to mqtt
						flag=true;
					}
				
				});
				//listener mouse/pen up event
				canvas.addEventListener('pointerup',function(){
					mouseDown = false; //set click/pendown to false
					if(flag){ //check if it was mooving before the event
						send(currX,currY, prevX,prevY,color,mouseDown);
						flag=false;
					}
				});
				//listener mouse/pen out of the canvas event
				canvas.addEventListener('pointerout',function(){
					mouseDown = false; //set click/pendown to false
					if(flag){ //check if it was mooving before the event
						send(currX,currY, prevX,prevY,color,mouseDown);
						flag=false;
					}
				}); 
				// show border on clicked color
				$("#controls").on("click", "li", function(){
					$(this).siblings().removeClass("selected");
					$(this).addClass("selected");
					color = $(this).css("background-color");
					
				});
				
				$("img").on("click", function(){
					context.clearRect(0, 0, canvas.width, canvas.height);
					var img=document.createElement('img');
					img.src=$(this).attr("src");
					context.drawImage(img,0,0,canvas.width, canvas.height);
					drawimg(img);
				});
}
function loadBackground(){
	var img=document.createElement('img');
					img.src="img/savedImage.jpg";
				///	ctx.drawImage(img,0,0);
				document.getElementById('can1').src = "img/savedImage.jpg?random="+new Date().getTime();
					
				//var background = new Image();
				//background.src = 
				//
				//// Make sure the image is loaded first otherwise nothing will draw.
				//background.onload = function(){
				//				///context.drawImage(background,0,0);   
				//}
				console.log("bacground updated");
}
function drawimg(img){
	client.subscribe("Drawing"); //subscribe to mqtt server
								path ={"path": img.getAttribute('src') ,"width":w,"height":h};
        message = new Paho.MQTT.Message(JSON.stringify(path)); //create new mqtt message
        message.destinationName = "Drawing"; //set destination for the message
        client.send(message); //send message
        console.log("message sent: "+ path); //log to check data
}
//function send data over mqtt
function send(currX, currY, prevX, prevY, color, mouseDown){
        coor={"width":w,"height":h,"currX": currX,"currY":currY,"prevX":prevX,"prevY":prevY,"color":color, "mouseDown":mouseDown}; //contruct JSON with data
								console.log(coor); //log to check data
        client.subscribe("Drawing"); //subscribe to mqtt server
        message = new Paho.MQTT.Message(JSON.stringify(coor)); //create new mqtt message
        message.destinationName = "Drawing"; //set destination for the message
        client.send(message); //send message
        console.log("message sent: "+ coor); //log to check data
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
    
