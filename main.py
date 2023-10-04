import cv2
import numpy as np
from math import degrees
#import serial
import time
from functions import *


cap = cv2.VideoCapture(1)
#s = serial.Serial(port='COM9', baudrate=9600, timeout=0)
while True:
        #T, img = cap.read()
        img = cv2.imread(f"./image/1.jpg")
        T = True
        img2 = img[:]
    #if T:
        if start_tresh(img):
            while True:
                print("work")
                try:
                    center, front, trash = points_returner(img)
                    draw_point(img2, center, "Center")
                    draw_point(img2, front, "Front")

                    cv2.imshow('main', img2) 
                    v_bot = np.array([front[0] - center[0], front[1] - center[1]])
                    v_trash = np.array([trash[0] - center[0], trash[1] - center[1]])
                except:
                    print("ERROE points", center, front, trash)
                    break

                angle = angle_returner(v_bot, v_trash)
                angle_time = str(round(15 * angle))
                if len(angle_time) < 4:
                    angle_time = ("0" * (4 - len(angle_time))) + angle_time
                print(angle_time, angle)
                draw_point(img2, trash, f"Trash Angle: {round(angle)}")
                #draw_point(img2, trash, f"Angle: -{round(angle)}°")

                #s = serial.Serial(port='COM9', baudrate=9600, timeout=10)
                #s.write(b'6')
                #s.write(bytes(angle_time, encoding='utf8'))
                #s.close()
                try:
                    T, img = cap.read()
                    center, front, trash = points_returner(img)
                except:
                    print("ERROE points - 2")
                    break
                if ((range_p(center[0], center[1], front[0], front[1]) * 2) // range_p(front[0], front[1], trash[0], trash[1])) < 2:
                    print("gOTCHA")
                    #s = serial.Serial(port='COM9', baudrate=9600, timeout=1)
                    #s.write(b'8')
                    #s.write(b'5')
                    #s.close()
                    #time.sleep(5)
                    break
                #else:
                    #s = serial.Serial(port='COM9', baudrate=9600, timeout=1)
                    #s.write(b'8')
                    #s.close()
                draw_point(img2, center, "Center")
                draw_point(img2, front, "Front")
                draw_point(img2, trash, "Trash")
                cv2.imshow('main', img2) 
        cv2.imshow('main', img2)
        #time.sleep(3)
            
        if cv2.waitKey(1) == ord('q'):
            break