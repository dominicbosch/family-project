from __future__ import division

import sys
import time
import signal
import datetime
import traceback
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

parser.add_argument('--cf',
	nargs='?',
	dest='cascade',
	help='Pattern recognition cascade filename as it is found in folder "cascades"')

parser.add_argument('--iw',
	nargs='?', type=int, default=1024,
	dest='width',
	help='Image width')

parser.add_argument('--ih',
	nargs='?', type=int, default=768,
	dest='height',
	help='Image height')

parser.add_argument('--savepath',
	nargs='?',
	default='detected-faces/',
	dest='path',
	help='Path to folder where images are stored')

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
		arr = list(str(v) for v in pic) # cast to strings... really?!
		writeLog('#{}|{}'.format(i, '|'.join(arr)))
		i += 1

detector = None
def exitHandler(*args):
	writeLog('Killed! Bye!')
	detector.stop()
	sys.exit(0)

signal.signal(signal.SIGINT, exitHandler)
signal.signal(signal.SIGTERM, exitHandler)

try:
	detector = FaceDetect(
		res=(args.width, args.height),
		hflip=(args.hflip==True),
		vflip=(args.vflip==True),
		cascade=args.cascade,
		savepath=args.path,
		verbose=(args.verbose==True)
	)
	detector.run(faceHasBeenDetected)

except:
	traceback.print_stack()

finally:
	detector.stop()
