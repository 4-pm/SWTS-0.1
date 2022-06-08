import numpy as np
from PIL import Image 
import cv2, os

a = os.listdir("C:/Users/User/Documents/GitHub/SWTS-0.1/train/trash")
for i in a:
    filename = "C:/Users/User/Documents/GitHub/SWTS-0.1/train/trash/" + i
    img = cv2.imread(filename)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
    hsv_min = np.array((35, 83, 76), np.uint8)
    hsv_max = np.array((90, 255, 255), np.uint8)
    img = cv2.inRange(hsv, hsv_min, hsv_max)
    cv2.imshow('result', img)
    cv2.imwrite(filename, img)

    while True:
        ch = cv2.waitKey(5)
        if ch == 27:
            #cv2.imwrite(filename, img)
            print("saved")
            break


