# Axidraw web interface
 ## Installation
 
assuming that you have that you have your raspberry setup with linux and python intalled (at least 3.7)

here are the steps to run this code:
1. install Flask navigate to the folder flask and run the following command
```
pip3 install --upgrade pip
pip3 install -r requirements.txt
```
check the ip of the raspoberry and change the ip in app.py line 67 for the ip of the raspberry
then run 
```
python3 app.py
```
you should see 'access at http://x.x.x.x:xxxx' in your terminal
2. open a new terminal navigate to `python local script` and install the axidraw library and paho-mqtt (in case it didnt installed with the requirments.txt)
```
python3 -m pip install https://cdn.evilmadscientist.com/dl/ad/public/AxiDraw_API.zip
pip3 install paho-mqtt
```
and on `axidraw-test.py` line 61-66 and on folder `flask/static/js` in the file`drawing-table.js` line 102-109 you have to configure the mqtt services according to your server
