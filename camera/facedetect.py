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
		framerate=10,
		hflip=False,
		vflip=False,
		scaleFactor=1.1,
		minNeighbors=5,
		minSize=(30, 30),
		maxSize=(200, 200),
		storeImages=False,
		storeAllImages=False,
		cascade=None,
		verbose=False
	):
		self.imageWidth = float(res[0])
		self.imageHeight = float(res[1])
		self.hflip = hflip
		self.vflip = vflip
		self.scaleFactor = scaleFactor
		self.minNeighbors = minNeighbors
		self.minSize = minSize
		self.maxSize = maxSize
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
			print('Using scaleFactor={}, minNeighbors={}, minSize={}x{}, maxSize={}x{}'.format(
				scaleFactor, minNeighbors, minSize, minSize, maxSize, maxSize)
			)
			if self.storeImages:
				print('Storing detected faces to {}'.format(self.savePath))
			if self.storeAllImages:
				print('Storing ALL images to {}'.format(self.savePathAll))
		self.face_cascade = cv2.CascadeClassifier(cascPath)
		self.stream = PiVideoStream(res=res, framerate=framerate, hflip=hflip, vflip=vflip, verbose=verbose)
		self.frame = None

	def run(self, callback):
		lastFrame = None
		self.isRunning = True
		self.stream.start(self.newFrame)
		while self.isRunning:
			if self.frame is not lastFrame:			

				startDetect = time.time()
				lastFrame = self.frame
				# greyscale might improove accuracyx
				detectframe = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
				# detectframe = lastFrame

				# image - Matrix of the type CV_8U containing an image where objects are detected. 
				# scaleFactor - Parameter specifying how much the image size is reduced at each image scale. 
				# minNeighbors - Parameter specifying how many neighbors each candidate rectangle should have to retain it. 
				# flags - Parameter with the same meaning for an old cascade as in the function cvHaarDetectObjects. It is not used for a new cascade. 
				# minSize - Minimum possible object size. Objects smaller than that are ignored. 
				# maxSize - Maximum possible object size. Objects larger than that are ignored. 
				# Possible improvement through TBB? on the other hand we are already using the CPU exhaustingly
				faces = self.face_cascade.detectMultiScale(
					image=detectframe,
					scaleFactor=self.scaleFactor,
					minNeighbors=self.minNeighbors,
					minSize=self.minSize,
					maxSize=self.maxSize
				)
				now = time.time()
				timestamp = datetime.datetime.now()
				ts = timestamp.strftime('%Y.%m.%d_%I:%M:%S')
				if self.verbose:
					print 'FaceDetect | Detect FPS: {0:.2f}'.format(1/(now-startDetect))
				
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
							cv2.rectangle(lastFrame, (af[0],af[1]), (af[0]+af[2],af[1]+af[3]), (0,0,255), 2)

					if self.storeImages:
						nm = 'face_{}.jpg'.format(ts)
						path = self.savePath + nm
						cv2.imwrite(path, lastFrame)
						if self.verbose:
							print('Stored Face as: '+nm)

					callback(arrFaces)
				
				elif self.storeAllImages:
					nm = 'snap_{}.jpg'.format(ts)
					path = self.savePathAll + nm
					cv2.imwrite(path, lastFrame)
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


