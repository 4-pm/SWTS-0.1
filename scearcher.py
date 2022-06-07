import numpy as np
from PIL import Image 
import cv2
from imutils.video import VideoStream

filename = 'C:/Users/User/Rover-Trasher/image/2.jpg'
corners = []
while True:
    vs = VideoStream(0)
    img = vs.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
    hsv_min = np.array((10, 61, 201), np.uint8)
    hsv_max = np.array((23, 147, 255), np.uint8)
    img = cv2.inRange(hsv, hsv_min, hsv_max)
    cv2.imshow('result', img)

    ch = cv2.waitKey(5)
    if ch == 27:
        cv2.imwrite(filename, img)
        print("saved")
        break


def coords_corner(x1, y1, x2, y2, i_left, i_right, j_left, j_right):
    global img
    for i in range(i_left, i_right):
        for j in range(j_left, j_right):
            if int(img[j][i][0]) == 255:
                if i < x1 and j < y1:
                    x1 = i
                    y1 = j
                elif i > x2 and j > y2:
                    x2 = i
                    y2 = j
    corners.append((x1 + abs(x1 - x2), y1 + abs(y1 - y2)))
    img = cv2.line(img, (x1,y1), (x2,y2), (255,0,0), 5)

img = cv2.imread('C:/Users/User/Rover-Trasher/image/2.jpg')
coords_corner(10000, 10000, 0, 0, 0, 320, 0, 240)  # левый верхний
coords_corner(10000, 10000, 0, 0, 320, 640, 0, 240)  # Правый верхний
coords_corner(10000, 10000, 0, 0, 0, 320, 240, 480)  # Левый нижний
coords_corner(10000, 10000, 0, 0, 320, 640, 240, 480)  # правый нижний


f = open("pole/pole.txt", "w")
w, h = (5, 7)
move = abs(corners[3][0] - corners[1][0]) // int(h)
line = abs(corners[0][0] - corners[1][0]) // w
print(move, line)
coof = {1: 1, 2: 0.6, 3: 0.3, 4: -0.3, 5:-0.6, 6: -1}
x1, y1, x2, y2 = (corners[0][0], corners[0][1], corners[0][0] + line, corners[0][1] + line)
x_center = [x1] + [x1 + line * i for i in range(1, 6)]
f.write(" ".join(map(str, x_center)) + "\n")
for i in range(1, 7):
    for j in range(1, 7):
        move2 = coof[j] * move
        img = cv2.line(img, (x_center[j - 1], y1), (int(x_center[j - 1] - move2 * i), y2), (255,255,255), 1)  # левая
        x_center[j - 1] = int(x_center[j - 1] - move2 * i)
    x1 = corners[0][0]
    y1 += line
    y2 += line
    x1 -= int(move)
    x2 += int(move)
    move *= 0.7
    f.write(" ".join(map(str, x_center)) + "\n")
    #line += int(move // 5)
cv2.imshow("image",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
