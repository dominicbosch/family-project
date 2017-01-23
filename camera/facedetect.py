from __future__ import division
import time
import cv2
import os
import numpy as np
import datetime
from pivideostream import PiVideoStream

class FaceDetect:
	def __init__(
		self,
		res=(1024, 768),
		hflip=False,
		vflip=False,
		savepath=None,
		cascade=None,
		verbose=False
	):
		self.imageWidth = float(res[0])
		self.imageHeight = float(res[1])
		self.hflip = hflip
		self.vflip = vflip
		self.savepath = savepath
		self.saveImage = False if (savepath == None) else True
		self.verbose = verbose
		self.isRunning = False
		# Get current file path in order to make an absolute reference to the cascade folder
		cascPath = '/'.join(os.path.realpath(__file__).split('/')[:-1])
		if cascade is None:
			cascPath += '/cascades/lbpcascade_frontalface.xml'
		else:
			cascPath += '/cascades/{}'.format(cascade)
		if self.verbose:
			print('Using casacade {}'.format(cascPath))
		self.face_cascade = cv2.CascadeClassifier(cascPath)
		self.stream = PiVideoStream(res=res, hflip=hflip, vflip=vflip)
		self.frame = None

	def run(self, callback):
		lastFrame = None
		self.isRunning = True
		self.stream.start(self.newFrame)
		while self.isRunning:
			if self.frame is not lastFrame:
				startDetect = time.time()
				lastFrame = self.frame
				faces = self.face_cascade.detectMultiScale(self.frame, 1.1, 5)
				now = time.time()
				if self.verbose:
					print 'FaceDetect | Detect Time: {}'.format(now-startDetect)
				# Execute the callback whenever faces have been detected
				if len(faces) > 0:

					# sort the faces list, first the biggest ones
					sortedFaces = sorted(faces, self.getSortMeasure)
					arrFaces = []
					for af in faces:
						# gonna be: [x, y, w, h, relX, relY, relW, relH]
						# set x, y, w, h
						face = [af[0], af[1], af[2], af[3]]
						# range; [-1, 1]
						face.append((2.0*af[0]+af[2])/self.imageWidth-1)
						# range[-1, 1]
						face.append((2.0*af[1]+af[3])/self.imageHeight-1)
						# appending relative width
						face.append(1.0*af[2]/self.imageWidth)
						# appending relative height
						face.append(1.0*af[3]/self.imageHeight)
						arrFaces.append(face)
						if self.saveImage:
							cv2.rectangle(self.frame, (af[0],af[1]), (af[0]+af[2],af[1]+af[3]), (255,0,0), 2)

					if self.saveImage:
						timestamp = datetime.datetime.now()
						ts = timestamp.strftime('%Y.%m.%d_%I:%M:%S')
						cv2.imwrite('{}face_{}.jpg'.format(self.savepath, ts), self.frame)

					callback(arrFaces)
			else:
				time.sleep(0.010)

	def getSortMeasure(self, (x,y,w,h), t):
		return int(100 / (w*h)) # calculate the area of the face

	# Callback executed from the pivideostream, registers new frames
	def newFrame(self, frame):
		self.frame = frame

	def stop(self):
		self.isRunning = False
		self.stream.stop()


