import sys
sys.path.insert(0, '../camera')
from facedetectYoloNCS import FaceDetect

fd = FaceDetect(storeImages=True)
fd.run()