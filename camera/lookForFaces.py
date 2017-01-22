from __future__ import division

import sys
import time
import signal
import datetime
import argparse # easy parsing of command line
from facedetect import FaceDetect

# Define possible command line arguments
parser = argparse.ArgumentParser(description='Look for faces on the PI Camera')

parser.add_argument('-hf',
	action='store_true',
	dest='hflip',
	help='Horizontal camera flip')

parser.add_argument('-vf',
	action='store_true',
	dest='vflip',
	help='Vertical camera flip')

parser.add_argument('-v',
	action='store_true',
	dest='verbose',
	help='Verbose output')

parser.add_argument('--iw',
	nargs='?',
	default=1024,
	type=int,
	dest='width',
	help='Image width')

parser.add_argument('--ih',
	nargs='?',
	default=768,
	type=int,
	dest='height',
	help='Image height')

# Parse command line arguments and see if something useful was provided
args = parser.parse_args()

def writeLog(msg):
	timestamp = datetime.datetime.now()
	ts = timestamp.strftime('[%Y.%m.%d_%I:%M:%S]: ')
	print ts + msg

def faceHasBeenDetected(arrFaces):
	numF = len(arrFaces)
	xPerc = arrFaces[0][4]*100
	if args.verbose:
		writeLog('New face(s) detected ({}), nearest at {:.2f}%'.format(numF, xPerc))
	i = 0
	for pic in arrFaces:
		writeLog('{}|{}'.format(i, '|'.join(pic)))
		i += 1

detector = None
def exitHandler(*args):
	writeLog('Killed! Bye!')
	detector.stop()
	sys.exit(0)

signal.signal(signal.SIGINT, exitHandler)
signal.signal(signal.SIGTERM, exitHandler)


# TODO really needed? would save an import
time.sleep(0.1)
try:
	detector = FaceDetect(res=(args.width, args.height), hflip=args.hflip, vflip=args.vflip, savepath=imagePath, verbose=args.verbose)
	detector.run(faceHasBeenDetected)

except:
    print("Error: ", sys.exc_info()[0])

finally:
	detector.stop()
