import numpy as np
from PIL import Image 
import cv2, os

img = cv2.imread("cuttest.jpg")
img = img[0:200, 0:100]
#img.resize(300, 300)

cv2.imshow('result', img)


while True:
        ch = cv2.waitKey(5)
        if ch == 27:
            #cv2.imwrite(filename, img)
            print("saved")
            break
