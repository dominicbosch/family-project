from facedetect import FaceDetect
import cv2

fd = FaceDetect(framerate=5)
def newface(arr):
	print arr[0]
#	key = cv2.waitKey(1) & 0xFF

fd.start(newface)
