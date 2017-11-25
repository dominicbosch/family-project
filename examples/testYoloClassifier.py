import sys
import glob
import datetime

sys.path.insert(0, '../camera')

import cv2
from yoloClassifier import YoloClassifier

if len(sys.argv) < 2:
	print ("USAGE: python testYoloClassifier.py ~/examples/")
	sys.exit()

timestamp = datetime.datetime.now()
ts = timestamp.strftime('%Y.%m.%d_%I:%M:%S')

clf = YoloClassifier(verbose=True)

# Get current file path in order to make an absolute reference to the cascade folder
savePath = '/'.join(os.path.realpath(__file__).split('/')[:-1])+'/detections/'
f = open('run_{}.csv'.format(ts), 'w')
f.write('filename,time,1st class,1st confidence,2nd class,2nd confidence,\n')

path = sys.argv[1]
arrImages = glob.glob("{}*.jpg".format(path))
for im in arrImages:
	frame = cv2.imread(im)
	ret = clf.classify(frame)
	res = ret[1]
	shp = frame.shape
	clf.tagImage(frame, res, shp[0], shp[1])
	filePath = savePath+'run_{}_{}'.format(ts, os.path.basename(im))
	cv2.imwrite(filePath, lastFrame)
	f.write('{},{}'.format(filePath, ret[0]))
	if len(res) > 0:
		f.write(',{},{}'.format(res[0][0], res[0][5]))
	if len(res) > 1:
		f.write(',{},{}'.format(res[1][0], res[1][5]))
	f.write('\n')

f.close()
clf.close()