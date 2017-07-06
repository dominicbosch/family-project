import sys
sys.path.insert(0, '../ultrasonic')

from time import sleep
from detectobstacle import DetectObstacle


def callback(dist):
	print("Callback distance: %.2fcm" % (dist*100))

detector = DetectObstacle(callback)

# we pretend to be a very busy process:
i = 0
while i < 20:
	print("busy parent %.0f" % i)
	i += 1
	sleep(1)

detector.exit()