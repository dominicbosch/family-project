from __future__ import division

import time
import datetime
import sys
import math
import os.path
import atexit
import signal

# easy logging:
import logging

# easy parsing of command line:
import argparse

# easy parsing of config file
import ConfigParser

import subprocess
from threading import Thread

# Define possible command line arguments
parser = argparse.ArgumentParser(description='Autonomously drive a car')

parser.add_argument('--configfile',
	nargs=1,
	help='Location of the config file')

parser.add_argument('-v',
	action='store_true',
	dest='verbose',
	help='Give a lot of output')

parser.add_argument('-s',
	action='store_true',
	dest='simulate',
	help='Simulation Mode where face detection is not loaded. '
		+ 'Helpful for testing on a PC with no camera.')

# Parse command line arguments and see if something useful was provided
args = parser.parse_args()

timeFactor = 1
# We add the camera folder to the path where python looks for imports
sys.path.insert(0, '../camera')
if args.simulate:
	from simulatefacedetect import SimulateFaceDetect as FaceDetect
	arduinoCommand = '../i2c/simulateArduino.py'
	timeFactor = 20 # simulation slowdown
else:
	from facedetect import FaceDetect
	arduinoCommand = '../i2c/arduino4'



# Define the log leveld epending on whether verbose is desired
if args.verbose:
	loglevel = logging.DEBUG
else:
	loglevel = logging.INFO

# Define logging format
# logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
logging.basicConfig(format='%(asctime)s %(message)s',
	datefmt='[%Y-%m-%d|%H:%M:%S]',
	level=loglevel)

def writeLog(msg):
	timestamp = datetime.datetime.now()
	ts = timestamp.strftime('[%Y.%m.%d_%I:%M:%S]: ')
	print ts + msg

def exitWithError(msg):
	logging.error('ERROR: '+msg)
	writeLog('Have a nice day!')
	sys.exit()

# Define the standard config file location
configfile = os.path.abspath('config.ini')
if args.configfile != None:
	configfile = os.path.abspath(args.configfile[0])
# Finally read the configuration file
if not os.path.isfile(configfile):
	exitWithError('Configuration file not existing: "'+configfile+'"')

logging.info('Using configuration file "{}"'.format(configfile))
oConfig = ConfigParser.ConfigParser()
oConfig.read(configfile)

# Test the available config file sections against what we actually need
avlSections = oConfig.sections()
logging.debug('Configuration file sections: {}'.format(', '.join(avlSections)))

# Helper function to safely parse the whole configuration file
def parseConfigOptions():
	cfg = {}
	for s in avlSections:
		cfg[s] = {}
		options = oConfig.options(s)
		for opt in options:
			try:
				# try to fetch the string
				cfg[s][opt] = oConfig.get(s, opt)
			except:
				logging.warn('exception on {}!'.format(opt))
				cfg[s][opt] = None
	return cfg


# Parse the configuration file
config = parseConfigOptions()
requiredConfig = {
	'Steering': ['stop-distance','slowdown-distance', 'turn-time-ms'],
	'Servo': ['device','servo-left','servo-center','servo-right'],
	'Motor': ['device','fullspeed','neutral','fullback','break'],
	'Ultrasonic': ['device','maximum-distance'],
	'Temperature': ['device'],
	'Accelerator': ['device'],
	'KeepAlive': ['device'],
	'Camera': ['width','height','framerate','imagepath', 'average-detect-time-ms']	
}

# Beautiful Python magic to find all the missing config options... :-D
notExisting = []
for s in requiredConfig:
	if not s in config:
		notExisting.append('Section '+s)
	else:
		for o in requiredConfig[s]: 
			if not any(xo in o for xo in config[s]):
				notExisting.append(s+':'+o)

# If some configurations are not existing we stop because we really need them, really
if len(notExisting) > 0:
	# Yes we really take the time for this plural beauty: :)
	plur  = 's' if len(notExisting) > 1 else ''
	exitWithError('Missing configuration section'+plur+': '+', '.join(notExisting))

# Helps casting config params to integers or exits completely if not successful
def castConfigToInt(section, option):
	text = config[section][option]
	try:
		return int(text)
	except:
		exitWithError('Unable to parse config '+section+':'+option+' to integer: '+text)


# ###
# FINALLY we start reading the configuration!
# ###

stopDistance = castConfigToInt('Steering','stop-distance')
slowDownDistance = castConfigToInt('Steering','slowdown-distance')
turnTime = castConfigToInt('Steering','turn-time-ms')

servoDevice = castConfigToInt('Servo','device')
servoLeft = castConfigToInt('Servo','servo-left')
servoCenter = castConfigToInt('Servo','servo-center')
servoRight = castConfigToInt('Servo','servo-right')

motorDevice = castConfigToInt('Motor','device')
motorFull = castConfigToInt('Motor','fullspeed')
motorNeutral = castConfigToInt('Motor','neutral')
motorBreak = castConfigToInt('Motor','break')

ultrasonicDevice = castConfigToInt('Ultrasonic','device')
# is this 100 cm? what comes back from the arduin4 command?
ultrasonicMaxDistance = castConfigToInt('Ultrasonic','maximum-distance')
pollPerSecond = castConfigToInt('Ultrasonic','poll-per-second')
writeLog('Polling {} times per second'.format(pollPerSecond))
# ultrasonic = ultrasonicMaxDistance # we assume no obstacles at the beginning
ultrasonic = 0 # we assume obstacles unless arduino tells us something else

# when a distance under slowDownDistance is measured, the counter is increased
# if more than two subsequent measurements are under slowDownDistance we start to slow down
# initially we assume obstacles
numMeasurements = 3

temperatureDevice = castConfigToInt('Temperature','device')
acceleratorDevice = castConfigToInt('Accelerator','device')
keepAliveDevice = castConfigToInt('KeepAlive','device')
camRes = (castConfigToInt('Camera','width'), castConfigToInt('Camera','height'))
camRate = castConfigToInt('Camera','framerate')
imagePath = config['Camera']['imagepath']
avgDetectTime = castConfigToInt('Camera', 'average-detect-time-ms')


# ###
# AND we initialize some more variables
# ###

# this will stop the thread that polls for the distance
isRunning = True

# we initialize the last face detected at the beginning of the (unix) time
lastFaceDetected = 1
# If we are ramping up, new lastFaceDetected can't influence the ramp,
# thus we need to register the ramp up face
rampUpFace = 1
rampUpTime = 1 # we ramp up the speed for one second

# we initialize at the center
lastRelativeFacePosition = 0


# linear ramp for motor deceleration:
# y = m*x + b 
# m = (maxArduinoValue - minArduinoValue) / (farDistance - minDistance)
m = (motorFull - motorNeutral) / (slowDownDistance - stopDistance)
# calculate b (= y-intercept of linear ramp) by putting any point into the equation,
# e.g. 100 = m * 20 + b (m is defined above because we have two points), then solve for b
b = motorNeutral - stopDistance * m

# Thread function, looping forever
def pollDistance():
	global numMeasurements
	global ultrasonic
	i = 0

	while isRunning:
		# Refresh the ultrasonic measurement
		ultrasonic = commandArduino(ultrasonicDevice, 0)

		# After polling the distance 10 times, we poll all other sensor data as well:
		i += 1
		if i == 10:
			temp = commandArduino(temperatureDevice, 0)
			x = commandArduino(acceleratorDevice, 0)
			y = commandArduino(acceleratorDevice, 1)
			z = commandArduino(acceleratorDevice, 2)
			writeLog('sensr | Temperature: {:.2f} C'.format(temp))
			writeLog('sensr | Accelerator: X={:.2f}'.format(x))
			writeLog('sensr | Accelerator: Y={:.2f}'.format(y))
			writeLog('sensr | Accelerator: Z={:.2f}'.format(z))

			i = 1

		# if measured distance is below slowdown distance
		if ultrasonic < slowDownDistance:
			# we increment the obstacle measurement counter 
			numMeasurements += 1
			if numMeasurements > 2:
				writeLog('obstc | Verified obstacle in {:.2f}cm'.format(ultrasonic))
			adjustSpeed()

		# we reset the obstacle measurement counter because ther is nothing anymore
		else:
			if args.simulate:
				writeLog('obstc | Cleared obstacle counter')
			numMeasurements = 0

		# we do want to adjust the steering at any point in time because
		# we might have lost contact to the face and need to acquire a new target
		adjustSteering()

		# we only poll the ultrasonic sensor every 100 ms
		time.sleep(timeFactor/pollPerSecond)


# We need to know whether we are already ramping up, so that new pictures 
# are not causing an immediate slow down
isRampingUp = True
def adjustSpeed():
	global rampUpFace
	now = time.time()

	# how much time since the last face detection passed 
	timePassed = now - lastFaceDetected
	writeLog('faces | Last face detected {:.2f}s ago'.format(timePassed))
	# the last face was only 1 second ago detected, we speed up
	# if we are already in a speedup ramp we do not adjust to latest picture!
	if timePassed < 1*timeFactor and now-rampUpFace < rampUpTime:
		# speedup with linear ramp over one second!
		arduinoValue = motorNeutral-(motorNeutral-motorFull)*timePassed/3
		writeLog('motor | Speeding up!')

	# between 1 to 3 seconds since lasg face detected we stay at full speed
	elif timePassed < 3*timeFactor:
		arduinoValue = motorFull
		writeLog('motor | Staying at full speed!')

	# if more than 3 seconds passed since last face detected, 
	# we gradually slow down over the next seven seconds until we stop
	elif timePassed < 10*timeFactor:
		# we reset the ramp up face
		rampUpFace = 1
		
		# 10 is full speed, the other 90 (to reach 100, which is stop)
		# are spread over ten seconds
		arduinoValue = motorFull+(motorNeutral-motorFull)*timePassed/10
						# 70				100			70			
		writeLog('motor | Slowing down because no more face detected')

	# if the last face has been detected more than 10 seconds ago, we stay still
	else:
		arduinoValue = motorBreak
		writeLog('motor | !BREAKING! because no faces')

	# if more than twice an obstacle has been detected we slow down if we are not already breaking
	if arduinoValue != motorBreak and numMeasurements > 2:
		if ultrasonic < slowDownDistance:
			writeLog('motor | obstacle in: {}cm'.format(ultrasonic))
			# slow down with a linear ramp y = m*x + b defined above.
			# if it is far away, the value would be under motorFull, thus we take
			# the maximum value in order to not send negative numbers to the arduino command
			arduinoValue = max(m*ultrasonic+b, motorFull)
			# writeLog('us={}, m={}, b={}, mF={}, aV={}, '.format(ultrasonic, m, b, motorFull, arduinoValue))
			if arduinoValue > motorNeutral:
				# if we are closer than neutral position, we break
				arduinoValue = motorBreak
				writeLog('motor | !BREAKING! because of obstacle')
			else:
				writeLog('motor | Slowing down because of obstacle')

	writeLog('MOTOR | FINAL DECISION SENT: {}'.format(int(arduinoValue)))
	commandArduino(motorDevice, arduinoValue)


def adjustSteering():
	now = time.time()
	
	# how much time since the last face detection passed 
	timePassed = now - lastFaceDetected
	relX = lastRelativeFacePosition
	writeLog('steer | time since last face {:.2f}s'.format(timePassed))

	# if we are still in valid turn time, we turn
	if timePassed < turnTime*timeFactor:
		if relX < 0:
			cmd = servoCenter+(servoCenter-servoLeft)*relX #relX will be negative
			# writeLog("steering left {}% = command to arduino: {}".format(relX*100, cmd))
			commandArduino(servoDevice, cmd)

		else:
			cmd = servoCenter+(servoRight-servoCenter)*relX
			# writeLog("steering right {}% = command to arduino: {}".format(relX*100, cmd))
			commandArduino(servoDevice, cmd)
		writeLog('STEER | TURNING: {}'.format(int(cmd)))

	# if we are under the detect time we assume we are heading the right direction, thus we stop turning
	elif timePassed < avgDetectTime*timeFactor:
		writeLog('steer | Heading straight')
		commandArduino(servoDevice, servoCenter)

	# if turn time passed, we don't know what to do anymore. So we start going left right
	else:
		writeLog('steer | TODO should go left, right, left,... until new face detected or stop')
		pass
		# print "else"
	# use sinus if face hasnt been detected for 3 seconds
	# steering will do a bit of left right left in order to acquire a new target
	
	# math.sin([0 .. 2*math.pi]) => left -> right -> center
	
	# we need to steer double the time to the right than to the left because we want to be
	# turning over the center

	# when all the way to the left again (5/2*math.pi) we stay for a full turn at the end
	
	# else head towards the face

def faceHasBeenDetected(arrFaces):
	global rampUpFace
	global lastFaceDetected
	global lastRelativeFacePosition

	numF = len(arrFaces)
	xPerc = arrFaces[0][4]*100
	writeLog('faces | new face(s) detected ({}), nearest at {:.2f}%'.format(numF, xPerc))

	# new timestamp for last face detection
	lastFaceDetected = time.time()
	# if the rampUpFace is not set (=1), we take this timestamp for it
	if rampUpFace == 1:
		rampUpFace = lastFaceDetected
	adjustSpeed()


	# we only head for the biggest face
	(x, y, w, h, relX, relY, relW, relH) = arrFaces[0]
	lastRelativeFacePosition = relX
	adjustSteering()


# commandArduino
								# 100 = center
# Servo:		arduino4	1	[45-150]	255
								# stop 200 fullback 200
# Motor:		arduino4	2	[100-10]	255
# Ultraschall:	arduino4	10		0		255 
# Temperatur:	arduino4	11		0		255
# keep-alive:	arduino4	254		0		255
def commandArduino(device, value):
	# print('Executing Arduino command device {}, value {}'.format(device, value))
	dev = str(device)
	cmd = str(int(value))
	# writeLog('Executing device={}, command={}'.format(dev, cmd))
	answerString = subprocess.check_output([arduinoCommand, dev, cmd, '255'])
	arr = answerString.split('\n')
	answer = 0
	if len(arr) > 4:
		try:
			answer = int(arr[4])
		except ValueError:
			try:
				answer = float(arr[4])
			except ValueError:
				answer = -1
	return answer

def exitHandler(*args):
	writeLog('Killed! Bye!')
	detector.stop()
	isRunning = False
	commandArduino(motorDevice, motorBreak)
	sys.exit(0)

signal.signal(signal.SIGINT, exitHandler)
signal.signal(signal.SIGTERM, exitHandler)
# atexit.register(exitHandler)
# signal.signal(signal.SIGINT, exitHandler)
# signal.signal(signal.SIGTERM, exitHandler)


# ###
# EVERYTHING starts here, after above definitions
# ###

time.sleep(0.1)
try:
	detector = FaceDetect(resolution=camRes, framerate=camRate, path=imagePath)
	Thread(target=pollDistance, args=()).start()
	detector.start(faceHasBeenDetected)
	raw_input('\nPRESS [ENTER] TO QUIT!\n\n')
	writeLog('Bye!')

except KeyboardInterrupt:
	writeLog('Forced Bye!')

finally:
	detector.stop()
	isRunning = False
	commandArduino(motorDevice, motorBreak)
