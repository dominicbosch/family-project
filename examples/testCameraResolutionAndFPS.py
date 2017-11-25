
import sys

print('Needs implementation!');
sys.exit()

sys.path.insert(0, '../camera')

import time
import datetime
from pivideostream import PiVideoStream


stream = PiVideoStream(
	res=res,
	framerate=framerate,
	sensor_mode=sensor_mode,
	hflip=False,
	vflip=False,
	verbose=True
)

def newFrame(frame):
	print('new frame');

stream.start(self.newFrame)