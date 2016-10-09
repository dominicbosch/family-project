import time
import datetime
import sys
import math
import os.path

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

# We add the camera folder to the path where python looks for imports
sys.path.insert(0, '../camera')
if args.simulate:
	from simulatefacedetect import SimulateFaceDetect as FaceDetect
	arduinoCommand = '../i2c/simulateArduino.py'
else:
	from facedetect import FaceDetect
	arduinoCommand = '../i2c/arduino4'


# Define the log leveld epending on whether verbose is desired
if args.verbose:
	loglevel = logging.DEBUG
else:
	loglevel = logging.INFO

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
			# try:
			# 	# Try to fetch an integer
			# 	cfg[s][opt] = oConfig.getint(s, opt)
			# except:
			try:
				# Otherwise fetch the string
				cfg[s][opt] = oConfig.get(s, opt)
			except:
				logging.warn('exception on {}!'.format(opt))
				cfg[s][opt] = None
	return cfg


# Parse the configuration file
config = parseConfigOptions()
requiredConfig = {
	'Steering': ['stop-distance','slowdown-distance'],
	'Servo': ['device','servo-left','servo-center','servo-right'],
	'Motor': ['device','fullspeed','neutral','break','reverse'],
	'Ultrasonic': ['device','maximum-distance'],
	'Temperature': ['device'],
	'KeepAlive': ['device'],
	'Camera': ['width','height','framerate','imagepath']	
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

servoDevice = castConfigToInt('Servo','device')
servoLeft = castConfigToInt('Servo','servo-left')
servoCenter = castConfigToInt('Servo','servo-center')
servoRight = castConfigToInt('Servo','servo-right')

motorDevice = castConfigToInt('Motor','device')
motorFull = castConfigToInt('Motor','fullspeed')
motorNeutral = castConfigToInt('Motor','neutral')
motorBreak = castConfigToInt('Motor','break')
motorReverse = castConfigToInt('Motor','reverse')

ultrasonicDevice = castConfigToInt('Ultrasonic','device')
# is this 100 cm? what comes back from the arduin4 command?
ultrasonicMaxDistance = castConfigToInt('Ultrasonic','maximum-distance')
# ultrasonic = ultrasonicMaxDistance # we assume no obstacles at the beginning
ultrasonic = 0 # we assume obstacles unless arduino tells us something else

temperatureDevice = castConfigToInt('Temperature','device')
keepAliveDevice = castConfigToInt('KeepAlive','device')
camRes = (castConfigToInt('Camera','width'), castConfigToInt('Camera','height'))
camRate = castConfigToInt('Camera','framerate')
imagePath = config['Camera']['imagepath']


# ###
# AND we initialize some more variables
# ###

# this will stop the thread that polls for the distance
isRunning = True

# we initialize the last face detected at the beginning of the (unix) time
lastFaceDetected = 1

# we initialize at the center
lastRelativeFacePosition = 0

# when a distance under slowDownDistance is measured, the counter is increased
# if more than two subsequent measurements are under slowDownDistance we start to slow down
numMeasurements = 0

# linear ramp for motor deceleration:
# y = m*x + b 
# m = (maxArduinoValue - minArduinoValue) / (farDistance - minDistance)
m = (motorFull - motorNeutral) / (ultrasonicMaxDistance - stopDistance)
# calculate b (= y-intercept of linear ramp) by putting any point into the equation,
# e.g. 20 = m * 100 + b (m is defined above because we have two points), then solve for b
b = 122.5

numPoll = 0
# Thread function, looping forever
def pollDistance():
	global numMeasurements
	global ultrasonic
	global numPoll

	while isRunning:

		# Refresh the ultrasonic measurement
		ultrasonic = commandArduino(ultrasonicDevice, 0)
		numPoll += 1
		if numPoll == 10:
			writeLog('Next obstacle in {}cm'.format(ultrasonic))
			numPoll = 0

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
	arduinoValue = motorBreak

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
			# speedup with linear ramp over three seconds!
			arduinoValue = motorFull + (motorFull-motorNeutral)*timePassed/3

		else:
			# we gradually slow down over the next ten seconds until we stop
			if timePassed < 10:
				# 10 is full speed, the other 90 (to reach 100, which is stop)
				# are spread over ten seconds
				arduinoValue = motorFull + (motorNeutral-motorFull)*timePassed/10

			# if the last face has been detected more than 10 seconds ago, we stay still
			else:
				arduinoValue = motorBreak

	commandArduino(motorDevice, arduinoValue)


def adjustSteering():
	now = time.time()
	
	# how much time since the last face detection passed 
	timePassed = now - lastFaceDetected
	relX = lastRelativeFacePosition
	if timePassed < 3:
		if relX < 0:
			cmd = servoCenter+(servoCenter-servoLeft)*relX #relX will be negative
			writeLog("steering left {}% = command to arduino: {}".format(relX*100, cmd))
			commandArduino(servoDevice, cmd)

		else:
			cmd = servoCenter+(servoRight-servoCenter)*relX
			writeLog("steering right {}% = command to arduino: {}".format(relX*100, cmd))
			commandArduino(servoDevice, cmd)

	else:
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
	global lastFaceDetected
	global lastRelativeFacePosition

	# new timestamp for last face detection
	lastFaceDetected = time.time()
	adjustSpeed()

	writeLog('{} new face(s) detected'.format(len(arrFaces)))
	writeLog('Nearest face at {}'.format(arrFaces[0][4]))

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
	# print('Executing Arduino command device {}, value {}'.format(device, value))
	writeLog('{} new face(s) detected'.format(len(arrFaces)))
	answerString = subprocess.check_output([arduinoCommand, str(device), str(int(value)), '255'])
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


# ###
# EVERYTHING starts here, after above definitions
# ###

time.sleep(0.1)
try:
	detector = FaceDetect(resolution=camRes, framerate=camRate, path=imagePath)
	Thread(target=pollDistance, args=()).start()
	detector.start(faceHasBeenDetected)
	raw_input('\nPRESS [ENTER] TO QUIT!\n\n')
	detector.stop()
	isRunning = False
	commandArduino(motorDevice, motorBreak)
	writeLog('Bye!')

except KeyboardInterrupt:
	writeLog('Forced Bye!')
	detector.stop()
	commandArduino(motorDevice, motorBreak)



