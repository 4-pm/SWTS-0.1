import cv2
import os
from imutils.video import VideoStream
import numpy as np

vs = VideoStream(src=0).start()
img = vs.read()
filename = 'C:/Users/User/Rover-Trasher/image/1.jpg'
#cv2.imwrite(filename, img)

#vs = VideoStream(src=0).start()
#img = vs.read()
'''img = cv2.imread('C:/Users/User/Rover-Trasher/image/1.jpg')
img = cv2.resize(img, (600, 600))
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
hsv_min = np.array((9, 154, 147), np.uint8)
hsv_max = np.array((28, 220, 251), np.uint8)
thresh = cv2.inRange(hsv, hsv_min, hsv_max)
cv2.imshow('result', thresh)'''

while True:
    img = vs.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
    hsv_min = np.array((0, 0, 203), np.uint8)
    hsv_max = np.array((21, 158, 240), np.uint8)
    thresh = cv2.inRange(hsv, hsv_min, hsv_max)
    cv2.imshow('result', thresh)

    ch = cv2.waitKey(5)
    if ch == 27:
        cv2.imwrite(filename, thresh)
        break

cv2.destroyAllWindows()
