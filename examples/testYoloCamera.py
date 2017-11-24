import sys
sys.path.insert(0, '../camera')
from facedetectYoloNCS import FaceDetect

def detectedStuff(arrResults):
	print ('Stuff has been detected: {}'.format(len(arrResults)))

fd = FaceDetect(storeImages=True)
fd.run(detectedStuff)