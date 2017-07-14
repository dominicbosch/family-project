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
		storeImages=False,
		storeAllImages=False,
		cascade=None,
		verbose=False
	):
		self.imageWidth = float(res[0])
		self.imageHeight = float(res[1])
		self.hflip = hflip
		self.vflip = vflip
		self.storeImages = storeImages
		self.storeAllImages = storeAllImages
		self.verbose = verbose
		self.isRunning = False
		# Get current file path in order to make an absolute reference to the cascade folder
		rootPath = '/'.join(os.path.realpath(__file__).split('/')[:-1])
		if cascade is None:
			cascPath = rootPath+'/cascades/lbpcascade_frontalface.xml'
		else:
			cascPath = rootPath+'/cascades/{}'.format(cascade)
		self.savePath = rootPath+'/detected-faces/'
		self.savePathAll = rootPath+'/snapshots/'
		if self.verbose:
			print('Using casacade {}'.format(cascPath))
			if self.storeImages:
				print('Storing detected faces to {}'.format(self.savePath))
			if self.storeAllImages:
				print('Storing ALL images to {}'.format(self.savePathAll))
		self.face_cascade = cv2.CascadeClassifier(cascPath)
		self.stream = PiVideoStream(res=res, hflip=hflip, vflip=vflip, verbose=verbose)
		self.frame = None

	def run(self, callback):
		lastFrame = None
		self.isRunning = True
		self.stream.start(self.newFrame)
		while self.isRunning:
			if self.frame is not lastFrame:			

				startDetect = time.time()
				lastFrame = self.frame
				greyFrame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
				faces = self.face_cascade.detectMultiScale(greyFrame, 1.1, 5)
				now = time.time()
				timestamp = datetime.datetime.now()
				ts = timestamp.strftime('%Y.%m.%d_%I:%M:%S')
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
						if self.storeImages:
							cv2.rectangle(greyFrame, (af[0],af[1]), (af[0]+af[2],af[1]+af[3]), (0,0,255), 2)

					if self.storeImages:
						nm = 'face_{}.jpg'.format(ts)
						path = self.savePath + nm
						cv2.imwrite(path, greyFrame)
						if self.verbose:
							print('Stored Face as: '+nm)

					callback(arrFaces)
				
				elif self.storeAllImages:
					nm = 'snap_{}.jpg'.format(ts)
					path = self.savePathAll + nm
					cv2.imwrite(path, greyFrame)
					if self.verbose:
						print('Stored Image as: '+nm)
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


