import sys
sys.path.insert(0, '../camera')

from yoloClassifier import YoloClassifier

if len(sys.argv) < 2:
	print ("USAGE: python testYoloClassifier.py ../camera/snapshots/test-detect.jpg")
	sys.exit()

clf = YoloClassifier()
clf.classify(cv2.imread(sys.argv[1]))
clf.close()