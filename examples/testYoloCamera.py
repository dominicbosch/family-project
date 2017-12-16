import sys
sys.path.insert(0, '../camera')
from cameraClassifier import CameraClassifier

def detectedStuff(arrResults):
	print ('So much stuff has been detected: {}'.format(len(arrResults)))

try:
	fd = CameraClassifier(storeDetections=True, verbose=True)
	fd.run(detectedStuff)

except KeyboardInterrupt:
	print('Cleaning and exiting')
	fd.stop()
