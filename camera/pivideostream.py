from __future__ import division
import time
from picamera import PiCamera
from picamera.array import PiRGBArray
from threading import Thread

class PiVideoStream:
	def __init__(
		self,
		res=(1024,768),
		framerate=10,
		sensor_mode=0,
		hflip=False,
		vflip=False,
		verbose=False,
		use_video_port=True
	):
		# initialize the camera and stream
		if verbose:
			print 'Starting camera with res={}x{}, hflip={}, vflip={}'.format(res[0], res[1], hflip, vflip)
		self.camera = PiCamera(resolution=res, framerate=framerate, sensor_mode=sensor_mode)
		self.camera.hflip = hflip
		self.camera.vflip = vflip
		self.verbose = verbose
		self.rawCapture = PiRGBArray(self.camera, size=res)
		self.stream = self.camera.capture_continuous(self.rawCapture,
			format="bgr", use_video_port=use_video_port)

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
		# TODO we should throttle this down by adding some sleep
		for f in self.stream:
			self.frameNum += 1
			# we only calculate FPS after ten frames
			if self.frameNum == 10:
				now = time.time()
				if self.verbose:
					print 'Camera | FPS: {0:.2f}'.format(10.0/(now-wallStart))
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
