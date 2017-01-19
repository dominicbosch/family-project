from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
 
camera = PiCamera()
width = 1920
height = 1088
camera.resolution = (width, height)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(width, height))

face_cascade = cv2.CascadeClassifier('facedetct.xml')

time.sleep(0.1)
i = 0
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	start_time = time.time()
	image = frame.array
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	i += 1
	fname = 'test_{}.jpg'.format(i)
	faces = face_cascade.detectMultiScale(frame, 1.1, 5)
	# faces = face_cascade.detectMultiScale(gray, 1.1, 5)
#	for (x,y,w,h) in faces:
#		cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)

	print "Found {0} faces!".format(len(faces))

	if len(faces) >0:
		cv2.imwrite(fname, image)
	
	rawCapture.truncate(0)

	print("--- %s seconds ---" % (time.time() - start_time))
