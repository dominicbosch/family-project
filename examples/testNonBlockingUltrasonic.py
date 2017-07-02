import sys
sys.path.insert(0, '../ultrasonic')

from detectobstacle import DetectObstacle



detector = DetectObstacle(
	res=(args.width, args.height),
	hflip=(args.hflip==True),
	vflip=(args.vflip==True),
	cascade=args.cascade,
	storeImages=args.store,
	verbose=(args.verbose==True)
)
