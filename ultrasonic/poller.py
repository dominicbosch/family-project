import sys
from time import sleep
from gpiozero import DistanceSensor

pinTrigger = 4
pinEcho = 17
maxDist = 2
detectThresh = 1
wait = 0.1

num = len(sys.argv)
if num > 1:
	pinTrigger = int(sys.argv[1])
if num > 2:
	pinEcho = int(sys.argv[2])
if num > 3:
	maxDist = float(sys.argv[3])
if num > 4:
	detectThresh = float(sys.argv[4])
if num > 5:
	wait = float(sys.argv[5])

# wait time of 0.01s after each measurement causes roughly 6% CPU usage
# 0.01s sleep leads to roughly a distance polling of 100 hertz
ultrasonic = DistanceSensor(
	trigger=pinTrigger,
	echo=pinEcho,
	max_distance=maxDist, 
	threshold_distance=detectThresh
)

try:
	while True:
		print('%.3f'%ultrasonic.distance)
		sleep(wait)

finally:
	ultrasonic.close()
	ultrasonic = None

