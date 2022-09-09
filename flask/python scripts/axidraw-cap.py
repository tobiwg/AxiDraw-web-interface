import numpy as np
import cv2 as cv
import ftplib
import time
import os
session = ftplib.FTP('ftp.tobiwg.com','tobiwg@csiargentina.com','azez4012')
session.cwd('axidraw/img')
global f_blocksize
global total_size
global size_written
f_blocksize = 1024
first = True
size_written = 0
def handle(block):
    global size_written
    global total_size
    global f_blocksize
    size_written = size_written + f_blocksize if size_written + f_blocksize < total_size else total_size
    percent_complete = size_written / total_size * 100
    print("%s percent complete" %str(percent_complete))

def get_contour_areas(contours):

    all_areas= []

    for cnt in contours:
        area = cv.contourArea(cnt)
        all_areas.append(area)

    return all_areas

path = r"C:\Users\tobiw\PycharmProjects\axidraw-capturing\savedImage.jpg"
cap = cv.VideoCapture(1)
if not cap.isOpened():
     print("Cannot open camera")
     exit()
while True:
    #Capture frame-by-frame
    #frame = cv.imread(path)
    ret, frame = cap.read()
    # # if frame is read correctly ret is True
    # if not ret:
    #      print("Can't receive frame (stream end?). Exiting ...")
    #      break
    # Our operations on the frame come here
    if first:
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        edges = cv.Canny(gray, 50, 200)

        contours, hierarchy = cv.findContours(edges.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)


        sorted_contours = sorted(contours, key=cv.contourArea, reverse=True)

        largest_item = sorted_contours[0]
        max = np.amax(largest_item[:], axis=0)
        min = np.amin(largest_item, axis=0)
        first = False

    print("max x: %f, min x: %f", max[0], max[0][1])

    cropped_image = frame[min[0][1]:max[0][1], min[0][0]:max[0][0]]
    filename = 'savedImage.jpg'
    #
    # # Using cv2.imwrite() method
    # # Saving the image
    cropped_resized_img = cv.resize(cropped_image, (1260, 804))
    cv.imwrite(filename, cropped_resized_img)
    file = open(filename, 'rb')
    total_size = os.path.getsize(filename)
    try:
        session.storbinary("STOR savedImage.jpg", file, callback=handle, blocksize=f_blocksize)  # send the file
    except:
        print("upload failed")
    #session.dir()

    cv.drawContours(frame, largest_item, -1, (254, 0, 0), 3)
    time.sleep(2)
    cv.imshow('Largest Object', frame)
    cv.imshow('crpped img', cropped_resized_img)

    # Display the resulting frame
    #cv.imshow('frame', gray)
    if cv.waitKey(1) == ord('q'):
         break
# When everything done, release the capture
#cap.release()
session.quit()
cv.destroyAllWindows()