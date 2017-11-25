import sys
sys.path.insert(0, '../camera')

from facedetect import FaceDetect

def faceHasBeenDetected(arrFaces):
	numF = len(arrFaces)
	xPerc = arrFaces[0][4]*100
	if args.verbose:
		writeLog('New face(s) detected ({}), nearest at {:.2f}%'.format(numF, xPerc))
	i = 0
	for pic in arrFaces:
		arr = list(str(v) for v in pic) # cast to strings... really?!
		writeLog('#{}/{}|{}'.format(i, len(arrFaces), '|'.join(arr)))
		i += 1

try:
	detector = FaceDetect(
		res=(args.width, args.height),
		framerate=args.framerate,
		hflip=(args.hflip==True),
		vflip=(args.vflip==True),
		scaleFactor=args.scaleFactor,
		minNeighbors=args.minNeighbors,
		minSize=(args.minSize, args.minSize),
		maxSize=(args.maxSize, args.maxSize),
		cascade=args.cascade,
		storeDetections=args.store,
		storeAllImages=args.storeall,
		verbose=(args.verbose==True)
	)
	detector.run(faceHasBeenDetected)

except:
	traceback.print_exc()

finally:
	detector.stop()
