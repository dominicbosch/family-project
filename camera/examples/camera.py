import argparse
import datetime
import imutils
import time
import cv2
 
ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())
 
# if args.get("video", None) is None:
camera = cv2.VideoCapture(0)
time.sleep(0.25)

while True:
	(grabbed, frame) = camera.read()

	# End of video
	if not grabbed:
		break
 
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)
	(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)

#	for c in cnts: 
#		(x, y, w, h) = cv2.boundingRect(c)
#		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#		text = "Occupied"

	# draw the text and timestamp on the frame
	cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
 
	# show the frame and record if the user presses a key
	cv2.imshow("Security Feed", frame)
	cv2.imshow("Thresh", thresh)
	cv2.imshow("Frame Delta", frameDelta)
	key = cv2.waitKey(1) & 0xFF
 
	if key == ord("q"):
		break
 
camera.release()
cv2.destroyAllWindows()
