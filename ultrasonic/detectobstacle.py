from time import sleep
from threading import Thread
from gpiozero import DistanceSensor


class DetectObstacle:
	# wait time of 0.01s after each measurement causes roughly 6% CPU usage
	# 0.01s sleep leads to roughly a distance polling of 100 hertz
	def __init__(self, callback, pinTrigger=16, pinEcho=18, maxDist=2, detectThresh=1.0, wait=0.1):
		if callable(callback) == False:
			print('No callback provided! That does not make much sense...')
			return

		self.isRunning = True
		self.wait = wait
		self.callback = callback
		self.ultrasonic = DistanceSensor(
			trigger=pinTrigger,
			echo=pinEcho,
			max_distance=maxDist, 
			threshold_distance=detectThresh
		)

		Thread(target=self.__update, args=()).start()
		print('Ultrasonic device started (trig=%i, echo=%i)...' % (pinTrigger, pinEcho))

	def __update(self):
		while self.isRunning:
			dist = self.ultrasonic.distance
			self.callback(dist)
			sleep(self.wait)

	def exit(self):
		self.isRunning = False
		self.ultrasonic.close()
		self.ultrasonic = None


