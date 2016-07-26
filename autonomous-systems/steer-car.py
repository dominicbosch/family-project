import sys
import subprocess
sys.path.insert(0, '../camera')
from facedetect import FaceDetect

detector = FaceDetect(resolution=(1024, 768), framerate=32)

def callback(arrFaces):

	# faces are arrays: [x, y, w, h, relX, relY, relW, relH]
	for f in arrFaces:
		print "relative x position: {}, relative y position: {}, ".format(f[4], f[5])

	# we only head for the biggest face

									# 100 = center
	# Servo:		arduino4	1	[45-150]	255
									# stop 150 fullback 200
	# Motor:		arduino4	2	[100-10]	255
	# Ultraschall:	arduino4	10		0		255 
	# Temperatur:	arduino4	11		0		255
	# keep-alive:	arduino4	254		0		255

	(x, y, w, h, relX, relY, relW, relH) = arrFaces[0]
	if relX < 0.5:
		sendCommand(1, 45)
		print "hello"
		# start when face detected
		# send keep-alive every 300ms
		# send steering
		# reduce speed when no face detected, steer left right and finally stop
		# send stop when no face detected after 5 s
	else:
		print "hallo"

def sendCommand(device, value):
	answer = subprocess.check_output(['../i2c/arduino4', str(device), str(value), '255'])
	print('the answer is {}'.format(answer))


try:
	detector.start(callback)
	raw_input('\nPRESS [ENTER] TO QUIT!\n\n')
	detector.stop()
	print 'Bye!'

except KeyboardInterrupt:
	print 'Forced Bye!'
	detector.stop()



