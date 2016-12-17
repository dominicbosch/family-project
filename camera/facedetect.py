from __future__ import division
import time
import cv2
import numpy as np
import datetime
from pivideostream import PiVideoStream

class FaceDetect:
	def __init__(self, resolution=(1024, 768), framerate=32, hflip=False, vflip=False, path="", cascade=None):
		self.imageWidth = resolution[0]
		self.imageHeight = resolution[1]
		self.framerate = framerate
		self.hflip = hflip
		self.vflip = vflip
		self.path = path
#		if cascade:
#			print("choosing default")
		cascPath = '../camera/cascades/haarcascade_frontalcatface.xml'
#		else:
#			print("choosing custom")
#			cascPath = '../camera/cascades/'+cascade
		self.face_cascade = cv2.CascadeClassifier(cascPath)
		self.stream = PiVideoStream(resolution=resolution, framerate=framerate)
		self.frame = None
		self.lastFrameAccessed = time.time()

	def start(self, callback):
		self.callback = callback
		self.stream.start(self.newFrame)

	def getSortMeasure(self, (x,y,w,h), t):
		return int(100 / (w*h)) # calculate the area of the face

	# FIXME since this is a callback, the pivideostream gets to exectue this
	# hence one thread needs to fetch the frame AND detect faces.
	# though we might run into too few cpus if we also create a thread for this.
	# on the other hand FPS will increase. we should really use two threads for those
	# two compute intensive tasks
	def newFrame(self, frame):
		self.frame = frame
		faces = self.face_cascade.detectMultiScale(frame, 1.1, 5)
		# Execute the callback whenever faces have been detected
		if len(faces) > 0:

			# sortedFaces = faces
			sortedFaces = sorted(faces, self.getSortMeasure)
			arrFaces = []
			for af in faces:
				cv2.rectangle(frame, (af[0],af[1]), (af[0]+af[2],af[1]+af[3]), (255,0,0), 2)
				# gonna be: [x, y, w, h, relX, relY, relW, relH]
				# set x, y, w, h
				face = [af[0], af[1], af[2], af[3]]
				# percentage; left -100%, right 100%: [-1,1]
				fw = float(self.imageWidth)
				fh = float(self.imageHeight)

				# range; [-1, 1]
				face.append((2*af[0]+af[2])/fw-1)
				# range[-1, 1]
				face.append((2*af[1]+af[3])/fh-1)
				# appending relative width
				face.append(af[2]/fw)
				# appending relative height
				face.append(af[3]/fh)
				arrFaces.append(face)

			timestamp = datetime.datetime.now()
			ts = timestamp.strftime("%Y.%m.%d_%I:%M:%S")
			cv2.imwrite("{}face_{}.jpg".format(self.path, ts), frame)

			# sort the faces list, first the biggest ones
			self.callback(arrFaces)

	def stop(self):
		self.stream.stop()


