import sys
import glob
from os import listdir
from os.path import isfile, join
sys.path.insert(0, '../camera')

import cv2
from yoloClassifier import YoloClassifier

if len(sys.argv) < 2:
	print ("USAGE: python testYoloClassifier.py ../camera/snapshots/test-detect.jpg")
	sys.exit()

clf = YoloClassifier(verbose=True)

path = sys.argv[1]
arrImages = glob.glob("{}*.jpg".format(path))
for im in arrImages:
	ret = clf.classify(cv2.imread(im))
	print (ret)

clf.close()