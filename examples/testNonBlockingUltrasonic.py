import sys
sys.path.insert(0, '../ultrasonic')

from detectobstacle import DetectObstacle

def callback(dist):
	print("Callback distance: %.1f" % dist)

detector = DetectObstacle(1)
# detector = DetectObstacle(callback)
