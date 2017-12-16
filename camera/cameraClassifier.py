from __future__ import division
import time
import cv2
import os
import numpy as np
import datetime
from pivideostream import PiVideoStream
from yoloClassifier import YoloClassifier

class CameraClassifier:
	def __init__(
		self,
		res=(1296, 730),
		sensor_mode=5, # 5: 1296x730, 16:9, 1-49fps, Full FoV, 2x2 Binning
		framerate=20,
		hflip=False,
		vflip=False,
		storeDetections=False,
		storeAllImages=False,
		verbose=False
	):
 		self.imageWidth = float(res[0])
		self.imageHeight = float(res[1])
		self.hflip = hflip
		self.vflip = vflip
		self.storeDetections = storeDetections
		self.storeAllImages = storeAllImages
		self.verbose = verbose
		self.isRunning = False
		self.yolo = YoloClassifier(verbose=verbose)
		
		# Get current file path in order to make an absolute reference to the cascade folder
		rootPath = '/'.join(os.path.realpath(__file__).split('/')[:-1])
		self.savePath = rootPath+'/output/'
		if self.verbose:
			if self.storeDetections:
				print('Storing detections to {}'.format(self.savePath))
			if self.storeAllImages:
				print('Storing ALL images to {}'.format(self.savePath))
		self.stream = PiVideoStream(
			res=res,
			framerate=framerate,
			sensor_mode=sensor_mode,
			hflip=hflip,
			vflip=vflip,
			verbose=verbose
		)
		self.frame = None

	def run(self, callback):
		lastFrame = None
		self.isRunning = True
		self.stream.start(self.newFrame)
		while self.isRunning:
			if self.frame is not lastFrame:			

				startDetect = time.time()
				lastFrame = self.frame

				ret = self.yolo.classify(self.frame)

				now = time.time()
				timestamp = datetime.datetime.now()
				ts = timestamp.strftime('%Y.%m.%d_%I:%M:%S')
				if self.verbose:
					print 'CameraClassifier | found {} in {} ms Detect FPS: {:.2f}'.format(len(ret[1]),ret[0],1/(now-startDetect))

				if len(ret[1]) > 0:
					arrFaces = []
					for el in ret[1]:
						x = int(el[1])
						y = int(el[2])
						w = int(el[3])//2
						h = int(el[4])//2
						if self.verbose:
							print ('    class : ' + el[0] 
								+ ' , [x,y,w,h]=[' + str(x) 
								+ ',' + str(y) + ',' + str(int(el[3])) 
								+ ',' + str(int(el[4]))+'], Confidence = ' + str(el[5]) )

						# set x, y, w, h
						face = [x, y, w, h]
						# range; [-1, 1]
						face.append((2.0*x+w)/self.imageWidth-1)
						# range[-1, 1]
						face.append((2.0*y+h)/self.imageHeight-1)
						# appending relative width
						face.append(1.0*w/self.imageWidth)
						# appending relative height
						face.append(1.0*h/self.imageHeight)
						arrFaces.append(face)

					if self.storeDetections or self.storeAllImages:
						self.yolo.tagImage(lastFrame, ret, self.imageWidth, self.imageHeight)
						nm = 'fdyncs.py_{}_detected.jpg'.format(ts)
						path = self.savePath + nm
						cv2.imwrite(path, lastFrame)
						if self.verbose:
							print('Stored detected image as: '+nm)

					callback(arrFaces)
				
				elif self.storeAllImages:
					nm = 'fdyncs.py_{}.jpg'.format(ts)
					path = self.savePath + nm
					cv2.imwrite(path, lastFrame)
					if self.verbose:
						print('Stored image as: '+nm)
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
		self.yolo.close()


