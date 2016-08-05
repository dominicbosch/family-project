import cv2
import time
import datetime
import numpy as np
from pivideostream import PiVideoStream


width = 1024
height = 768
framerate = 32
print('init stream')
stream = PiVideoStream(resolution=(width, height), framerate=framerate)
 
print('Starting stream')
# start a video thread

print('Loading Face recognition')
face_cascade = cv2.CascadeClassifier('facedetect.xml')

time.sleep(0.1)
def test(frame):

	print('Looping')
	start_time = time.time()

	# frame = stream.read()

	# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	# faces = face_cascade.detectMultiScale(gray, 1.1, 5)
	print('Detect faces')
	faces = face_cascade.detectMultiScale(frame, 1.1, 5)

	print "Found {0} faces!".format(len(faces))
	for (x,y,w,h) in faces:
		cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)

	# draw the timestamp on the frame
	timestamp = datetime.datetime.now()
	ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
	cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.35, (0, 0, 255), 1)

	#if len(faces) >0:
	fname = 'test_{}.jpg'.format(ts)
	cv2.imwrite(fname, frame)
	print("--- %s seconds ---" % (time.time() - start_time))

try:
	stream.start(test)
	# loop over the frames from the video stream

except KeyboardInterrupt:
	print 'Bye!'
	stream.stop()


