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
	arduinoCommand = '../i2c/cardo'



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
	'Camera': ['width','height','framerate','imagepath', 'average-detect-time-ms', 'cascade-file']	
}



# TODO get hflip and vflip into config



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
avgDetectTime = config['Camera']['cascade-file']


def faceHasBeenDetected(arrFaces):

	numF = len(arrFaces)
	xPerc = arrFaces[0][4]*100
	writeLog('faces | new face(s) detected ({}), nearest at {:.2f}%'.format(numF, xPerc))

	# we only head for the biggest face
	(x, y, w, h, relX, relY, relW, relH) = arrFaces[0]


detector = None
def exitHandler(*args):
	writeLog('Killed! Bye!')
	detector.stop()
	sys.exit(0)

signal.signal(signal.SIGINT, exitHandler)
signal.signal(signal.SIGTERM, exitHandler)
# atexit.register(exitHandler)
# signal.signal(signal.SIGINT, exitHandler)
# signal.signal(signal.SIGTERM, exitHandler)


time.sleep(0.1)
try:
	detector = FaceDetect(resolution=camRes, framerate=camRate, path=imagePath)
	detector.run(faceHasBeenDetected)

except KeyboardInterrupt:
	writeLog('Forced Bye!')

except:
    print("Unexpected error:", sys.exc_info()[0])

finally:
	detector.stop()
	commandArduino(motorDevice, motorBreak)
