import time
import sys
import math
import subprocess
from threading import Thread
sys.path.insert(0, '../camera')
from facedetect import FaceDetect

steeringLeft = 45
steeringRight = 150
steeringCenter = 100

# is this 100 cm? what comes back from the arduin4 command?
ultrasonic = 100

# this will stop the thread that polls for the distance
isRunning = True

# we initialize the last face detected at the beginning of the (unix) time
lastFaceDetected = 1

# we initialize at the center
lastRelativeFacePosition = 0.5

# when a distance under threshold is measured, the counter is increased
# if more than two subsequent measurements are under threshold we start to slow down
slowDownDistance = 90 # 90 cm
numMeasurements = 0

# linear ramp for motor deceleration:
# y = m*x + b 
# m = (maxArduinoValue - minArduinoValue) / (farDistance - minDistance)
m = (10 - 100) / (100 - 20)
# calculate b (= y-intercept of linear ramp) by putting any point into the equation,
# e.g. 20 = m * 100 + b (m is defined above because we have two points), then solve for b
b = 122.5

# Thread function, looping forever
def pollDistance():
	global numMeasurements
	global ultrasonic

	while isRunning:

		# Refresh the ultrasonic measurement
		ultrasonic = commandArduino(10, 0)

		# if measured distance is below slowdown distance
		if ultrasonic < slowDownDistance:
			# we increment the obstacle measurement counter 
			numMeasurements += 1
			adjustSpeed()

		# we reset the obstacle measurement counter because ther is nothing anymore
		else:
			numMeasurements = 0

		# we do want to adjust the steering at any point in time because
		# we might have lost contact to the face and need to acquire a new target
		adjustSteering()

		# we only poll the ultrasonic sensor every 200 ms
		time.sleep(0.1)


def adjustSpeed():
	# we stay basically still unless...
	arduinoValue = 150

	# if more than twice an obstacle has been detected
	if numMeasurements > 2:
		# slow down with a linear ramp y = m*x + b defined above
		# set the decelerated speed
		arduinoValue = m * ultrasonic + b

	else:
		now = time.time()
		
		# how much time since the last face detection passed 
		timePassed = now - lastFaceDetected

		# the last face was only 3 seconds ago detected, we stay at full speed
		if timePassed < 3:
			arduinoValue = 10

		else:
			# we gradually slow down over the next ten seconds until we stop
			if timePassed < 10:
				# 10 is full speed, the other 90 (to reach 100, which is stop)
				# are spread over ten seconds
				arduinoValue = 10 + 9*timePassed

			# if the last face has been detected more than 10 seconds ago, we stay still
			else:
				arduinoValue = 150

	commandArduino(2, arduinoValue)


def adjustSteering():
	now = time.time()
	
	# how much time since the last face detection passed 
	timePassed = now - lastFaceDetected
	relX = lastRelativeFacePosition
	if timePassed < 3:
		if relX < 0.5:
			prct = 2*relX
			print "left {}%".format(prct*100)
			commandArduino(1, steeringLeft + (steeringCenter-steeringLeft)*prct)

		else:
			prct = 2*(relX-0.5)
			print "right {}%".format(prct*100)
			commandArduino(1, steeringCenter + (steeringRight-steeringCenter)*prct)

	else:
		print "else"
	# use sinus if face hasnt been detected for 3 seconds
	# steering will do a bit of left right left in order to acquire a new target
	
	# math.sin([0 .. 2*math.pi]) => left -> right -> center
	
	# we need to steer double the time to the right than to the left because we want to be
	# turning over the center

	# when all the way to the left again (5/2*math.pi) we stay for a full turn at the end
	
	# else head towards the face

def faceHasBeenDetected(arrFaces):
	global lastFaceDetected
	global lastRelativeFacePosition

	# new timestamp for last face detection
	lastFaceDetected = time.time()
	adjustSpeed()

	# we only head for the biggest face
	(x, y, w, h, relX, relY, relW, relH) = arrFaces[0]
	lastRelativeFacePosition = relX
	adjustSteering()


# commandArduino
								# 100 = center
# Servo:		arduino4	1	[45-150]	255
								# stop 150 fullback 200
# Motor:		arduino4	2	[100-10]	255
# Ultraschall:	arduino4	10		0		255 
# Temperatur:	arduino4	11		0		255
# keep-alive:	arduino4	254		0		255
def commandArduino(device, value):
	print('Executing Arduino command device {}, value {}'.format(device, value))
	answerString = subprocess.check_output(['../i2c/arduino4', str(device), str(value), '255'])
	arr = answerString.split('\n')
	answer = 0
	if len(arr) > 4:
		try:
			answer = int(arr[4])
		except ValueError:
			answer = -1
	return answer

time.sleep(0.1)
try:
	detector = FaceDetect(resolution=(1024, 768), framerate=32, path='detected-faces/')
	Thread(target=pollDistance, args=()).start()
	detector.start(faceHasBeenDetected)
	raw_input('\nPRESS [ENTER] TO QUIT!\n\n')
	detector.stop()
	isRunning = False
	print 'Bye!'

except KeyboardInterrupt:
	print 'Forced Bye!'
	detector.stop()



