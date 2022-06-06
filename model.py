from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
import time
import cv2
import os

path=os.path.join(os.path.abspath(os.curdir) , 'my_model.onnx')
args_confidence = 0.2
# initialize the list of class labels 
CLASSES = ['paper', 'nopaper']
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
# load our serialized model from disk
net = cv2.dnn.readNetFromONNX("C:/Users/User/Rover-Trasher/models/model.onnx")

vs = VideoStream(src=0).start()
time.sleep(2.0)
fps = FPS().start()
frame = vs.read()
frame = imutils.resize(frame, width=400)


while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=400)

	# grab the frame dimensions and convert it to a blob
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (32, 32)),scalefactor=1.0/32
                              , size=(32, 32), mean= (128,128,128), swapRB=True)
	cv2.imshow("Cropped image", cv2.resize(frame, (32, 32)))

	# pass the blob through the network and obtain the detections and
	# predictions
	net.setInput(blob)
	detections = net.forward()
	a = list(zip(CLASSES, detections[0]))

	confidence = abs(detections[0][0]-detections[0][1])

	if (confidence > args_confidence) :
		
		class_mark=np.argmax(detections)
		#cv2.putText(frame, CLASSES[class_mark], (30,30),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (242, 230, 220), 2)

	for i in np.arange(0, detections.shape[1]):
		confidence = detections[0, i]

		# filter out weak detections by ensuring the `confidence` is
		# greater than the minimum confidence
		if confidence > 0.1:
			# extract the index of the class label from the
			# `detections`, then compute the (x, y)-coordinates of
			# the bounding box for the object
			idx = int(detections[0, i])
			box = detections[0, i] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")
			print(startX, startY, endX, endY)

			# draw the prediction on the frame
			label = "{}: {:.2f}%".format(CLASSES[idx],
				confidence * 100)
			cv2.rectangle(frame, (startX, startY), (endX, endY),
				COLORS[idx], 2)
			y = startY - 15 if startY - 15 > 15 else startY + 15
			cv2.putText(frame, label, (startX, y),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)


	cv2.imshow("Web camera view", frame)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("q"):
		break

	fps.update()
	#print(max(a, key=lambda x: x[1]))

fps.stop()
cv2.destroyAllWindows()
vs.stop()