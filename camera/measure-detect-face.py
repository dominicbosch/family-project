import time
import cv2
import os
import numpy as np

# Get current file path in order to make an absolute reference to the cascade folder
rootPath = '/'.join(os.path.realpath(__file__).split('/')[:-1])
cascPath = rootPath+'/cascades/lbpcascade_frontalface.xml'
savePath = rootPath+'/detected-face.jpg'
face_cascade = cv2.CascadeClassifier(cascPath)

img = cv2.imread('test-detect.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

startDetect = time.time()
faces = face_cascade.detectMultiScale(img, 1.1, 5)
now = time.time()
print('FaceDetect | Detect Time: {}'.format(now-startDetect))

if len(faces) > 0:
	for af in faces:
		face = [af[0], af[1], af[2], af[3]]
		cv2.rectangle(img, (af[0],af[1]), (af[0]+af[2],af[1]+af[3]), (0,0,255), 2)
		cv2.imwrite(savePath, img)
else:
	print('No face detected!')



