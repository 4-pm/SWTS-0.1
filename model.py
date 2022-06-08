from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
import time
import cv2
import os

#path=os.path.join(os.path.abspath(os.curdir) , 'my_model.onnx')
args_confidence = 0.1
CLASSES = ["trash"]
print("[INFO] loading model...")
net = cv2.dnn.readNetFromONNX("C:/Users/User/Documents/GitHub/SWTS-0.1/models/model.onnx")
vs = VideoStream(src=0).start()
time.sleep(2.0)
fps = FPS().start()
frame = vs.read()
corners = [tuple(map(int, i.split())) for i in open("./pole/pole.txt")]
print(corners)
#frame = imutils.resize(frame, width=400)


while True:
	frame = vs.read()
	for i in range(6):
		for j in range(6):
			x1, y1 = corners[i][j]
			x2, y2 = corners[i + 1][j + 1]
			sqr = frame[x1:x1, y1:y2]
			hsv = cv2.cvtColor(sqr, cv2.COLOR_BGR2HSV )
			hsv_min = np.array((35, 83, 76), np.uint8)
			hsv_max = np.array((90, 255, 255), np.uint8)
			sqr = cv2.inRange(hsv, hsv_min, hsv_max)
			sqr = cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB)

			# grab the frame dimensions and convert it to a blob
			(h, w) = sqr.shape[:2]
			blob = cv2.dnn.blobFromImage(cv2.resize(sqr, (32, 32)),scalefactor=1.0/32
									, size=(32, 32), mean= (128,128,128), swapRB=True)
			cv2.imshow("Cropped image", cv2.resize(frame, (32, 32)))
			net.setInput(blob)
			detections = net.forward()
			a = list(zip(CLASSES, detections[0]))
			confidence = detections[0][0] - detections[0][1]
			if confidence > args_confidence :
				frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255))
				#print(confidence)
				#class_mark=np.argmax(detections)
				#cv2.putText(frame, CLASSES[class_mark], (30,30),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (242, 230, 220), 2)

	cv2.imshow("Web camera view", frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break
	fps.update()
	#print(max(a, key=lambda x: x[1]))

fps.stop()
cv2.destroyAllWindows()
vs.stop()

