from __future__ import division
import cv2
import numpy as np
import datetime
from pivideostream import PiVideoStream

class FaceDetect:
	def __init__(self, resolution=(1024, 768), framerate=32, hflip=True, vflip=True, path=""):
		self.imageWidth = resolution[0]
		self.imageHeight = resolution[1]
		self.framerate = framerate
		self.hflip = hflip
		self.vflip = vflip
		self.path = path
		self.face_cascade = cv2.CascadeClassifier('../camera/facedetect.xml')
		self.stream = PiVideoStream(resolution=resolution, framerate=framerate)

	def start(self, callback):
		self.callback = callback
		self.stream.start(self.detect)

	def getSortMeasure(self, (x,y,w,h), t):
		return int(100 / (w*h)) # calculate the area of the face

	def detect(self, frame):
		faces = self.face_cascade.detectMultiScale(frame, 1.1, 5)
		# Execute the callback whenever faces have been detected
		if len(faces) > 0:

			# sortedFaces = faces
			sortedFaces = sorted(faces, self.getSortMeasure)
			arrFaces = []
			for af in faces:
				# gonna be: [x, y, w, h, relX, relY, relW, relH]
				face = [af[0], af[1], af[2], af[3]]
				cv2.rectangle(frame, (af[0],af[1]), (af[0]+af[2],af[1]+af[3]), (255,0,0), 2)
				# percentage; left 0%, right 100%
				fw = float(self.imageWidth)
				fh = float(self.imageHeight)
				face.append((af[0]+af[2]/2)/fw)
				# percentage; top 0%, bottom 100%
				face.append((af[1]+af[3]/2)/fh)
				face.append(af[2]/fw)
				face.append(af[3]/fh)
				arrFaces.append(face)

			timestamp = datetime.datetime.now()
			ts = timestamp.strftime("%Y.%m.%d_%I:%M:%S")
			cv2.imwrite("{}face_{}.jpg".format(self.path, ts), frame)

			# sort the faces list, first the biggest ones
			self.callback(arrFaces)

	def stop(self):
		self.stream.stop()


