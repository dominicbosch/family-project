from __future__ import division
import time
from picamera import PiCamera
from picamera.array import PiRGBArray
from threading import Thread

class PiVideoStream:
	def __init__(self, res=(1024, 768), hflip=False, vflip=False):
		# initialize the camera and stream
		print 'Starting camera with hflip={}, vflip={}, res={}x{}'.format(hflip, vflip, res[0], res[1])
		self.camera = PiCamera()
		self.camera.hflip = hflip
		self.camera.vflip = vflip
		self.rawCapture = PiRGBArray(self.camera, size=res)
		self.stream = self.camera.capture_continuous(self.rawCapture,
			format="bgr", use_video_port=True)

		# initialize the frame and the variable used to indicate
		# if the thread should be stopped
		self.frame = None
		self.stopped = False
		self.frameNum = 0

	def start(self, callback):
		self.callback = callback
		# start the thread to read frames from the video stream
		Thread(target=self.update, args=()).start()

	def update(self):
		wallStart = time.time()
		# keep looping infinitely until the thread is stopped
		for f in self.stream:
			self.frameNum += 1
			if self.frameNum == 10:
				now = time.time()
				print 'Camera | FPS: {}'.format((now-wallStart)/10)
				self.frameNum = 0
				wallStart = now
			# grab the frame from the stream and clear the stream in
			# preparation for the next frame
			self.frame = f.array
			self.rawCapture.truncate(0)
			self.callback(self.frame)

			# if the thread indicator variable is set, stop the thread
			# and resource camera resources
			if self.stopped:
				self.stream.close()
				self.rawCapture.close()
				self.camera.close()

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True
