import cv2
import numpy as np
from math import degrees
import serial
import time
from functions import *


cap = cv2.VideoCapture(0)

while True:
    T, img = cap.read()
    img2 = img[:]
    if T:
        if start_tresh(img):
            while True:
                center, front, trash = points_returner(img)
                v_bot = np.array([front[0] - center[0], front[1] - center[1]])
                v_trash = np.array([trash[0] - center[0], trash[1] - center[1]])
                angle = angle_returner(v_bot, v_trash)
                angle_time = 5 #!!!!!!!!!!! формула времени
                s = serial.Serial(port='COM9', baudrate=9600, timeout=angle_time + 1)
                if angle > 0:
                    s.write(b'6')
                else:
                    s.write(b'4')
                s.close()
                center, front, trash = points_returner(img)
                if range_p(center[0], center[1], front[0], front[1]) * 2 // range_p(front[0], front[1], trash[0], trash[1]) < 2:
                    s = serial.Serial(port='COM9', baudrate=9600, timeout=angle_time + 1)
                    s.write(b'8')
                    s.write(b'5')
                    s.close()
                    time.sleep(10)
                    break
                else:
                    s = serial.Serial(port='COM9', baudrate=9600, timeout=angle_time + 1)
                    s.write(b'8')
                    s.close()
                draw_point(img2, center, "Center")
                draw_point(img2, front, "Front")
                draw_point(img2, trash, "Trash")
        cv2.imshow('main', img2) 
        time.sleep(1)
            
    if cv2.waitKey(1) == ord('q'):
        break