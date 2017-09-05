#!/usr/bin/env python
from __future__ import division
import sys
import time
import random

def castToInt(text):
	try:
		answer = int(text)
	except ValueError:
		answer = -1
	return answer

if len(sys.argv) < 4:
	print "Too few argumets!"
	sys.exit(1)

elif int(sys.argv[3]) != 255:
	print "Wrong end command!"
	sys.exit(1)

else:
	rand = random.random()+0.01
	time.sleep(rand/20)
	device = castToInt(sys.argv[1])
	if not device in [1, 2, 10, 11, 12, 13]:
		print "Wrong Device!"
		sys.exit(1)
	
	# Ultraschall:	arduino4	10		0		255 
	elif device == 10:
		# simulate distances from 0 to 200
		print 'line1\nline2\nline3\nline4, value:\n{}'.format(rand*200)

	# Temperatur:	arduino4	11		0		255
	elif device == 11:
		# simulate temperatures from 0 to 40
		print 'line1\nline2\nline3\nline4, value:\n{}'.format(rand*40)

	# Humidity:	arduino4	12		0		255
	elif device == 12:
		# simulate humidity from 0 to 100
		print 'line1\nline2\nline3\nline4, value:\n{}'.format(rand*100)

	# Humidity:	arduino4	12		0		255
	elif device == 13:
		# simulate g force from 0 to 100
		print 'line1\nline2\nline3\nline4, value:\n{}'.format(rand*100)

	sys.exit(0)
