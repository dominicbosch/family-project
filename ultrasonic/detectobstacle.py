from time import sleep
from gpiozero import DistanceSensor

class DetectObstacle:
	def __init__(self, callback, pinTrigger=4, pinEcho=17, maxDist=2, detectThresh=1.0, wait=0.1):
		if callable(callback) == False:
			print('No callback provided! That does not make much sense...')
			return

		self.wait = wait

		self.ultrasonic = DistanceSensor(
			trigger=pinTrigger,
			echo=pinEcho,
			max_distance=maxDist, 
			threshold_distance=detectThresh
		)

		self.ultrasonic.when_in_range = self.__detectedObstacle
		self.ultrasonic.when_out_of_range = self.__noMoreObstacle

	def __detectedObstacle(self):
		print("Obstacle at %.1f " % self.ultrasonic.distance)
		self.isRunning = True
		while self.isRunning:
			print("... Updated to: %.1f " % self.ultrasonic.distance)
			time.sleep(self.wait)

	def __noMoreObstacle(self):
		self.isRunning = False
		print("Out of range at %.1f " % self.ultrasonic.distance)

	def exit(self):
		self.isRunning = False
		self.ultrasonic.close()
		self.ultrasonic = None


