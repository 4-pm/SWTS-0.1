import cv2
import numpy as np
from math import degrees
import serial
import time
from functions import *


# блютуз
#s = serial.Serial(port='COM9', baudrate=9600, timeout=10)
#s.write(b'5')
#s.close()

cap = cv2.VideoCapture(0)

while True:
    frame = cap.read()
    # if frame is read correctly ret is True
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv2.imshow('frame', gray)
    time.sleep(1)
    if cv2.waitKey(1) == ord('q'):
        break