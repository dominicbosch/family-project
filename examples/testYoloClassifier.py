import sys
sys.path.insert(0, '../camera')

import cv2
from yoloClassifier import YoloClassifier

if len(sys.argv) < 2:
	print ("USAGE: python testYoloClassifier.py ../camera/snapshots/test-detect.jpg")
	sys.exit()

clf = YoloClassifier()
ret = clf.classify(cv2.imread(sys.argv[1]))
print (ret)
clf.close()