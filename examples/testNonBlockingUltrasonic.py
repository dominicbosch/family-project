import sys
sys.path.insert(0, '../ultrasonic')

from time import sleep
from detectobstacle import DetectObstacle


def callback(dist):
	print("Callback distance: %.1f" % dist)

detector = DetectObstacle(callback)

# we pretend to be a very busy process:
while True:
	sleep(0.01)