from __future__ import division
import math
import time
import random
from threading import Thread

class SimulateFaceDetect:
	def __init__(self, resolution=(1024, 768), framerate=32, hflip=True, vflip=True, path=""):
		self.fw = resolution[0] / 4
		self.fh = resolution[1] / 4
		self.framerate = framerate
		self.loopNum = 0
		self.isRunning = False

	def start(self, callback):
		self.callback = callback
		self.isRunning = True
		Thread(target=self.simulate, args=()).start()

	def simulate(self):
		time.sleep(5) # we just wait 5 seconds at the beginning
		while self.isRunning:
			self.loopNum += 1
			# gonna be: [x, y, w, h, relX, relY, relW, relH]
			arrFaces = [[
				self.fw, self.fh, self.fw, self.fh,
				# shift random number from [0, 1) to [-1,1)
				2*random.random()-1, 2*random.random()-1, 1/4, 1/4
			]] 
			self.callback(arrFaces)
			# This is a delaying function which means that after ten iterations
			# the possibility to not see a face for twenty seconds is pretty high
			sleep = random.random()+10*abs(math.sin(math.pi*self.loopNum/5))
			# print '\nface detect sleeping {}s\n'.format(sleep)
			time.sleep(sleep)

	def stop(self):
		self.isRunning = False


