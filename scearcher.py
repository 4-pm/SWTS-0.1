import numpy as np 
import cv2
from imutils.video import VideoStream
import sys
from math import sqrt

filename = 'C:/Users/User/Rover-Trasher/image/1.jpg'
corners = []
while True:
    vs = VideoStream(0)
    img = vs.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
    hsv_min = np.array((9, 62, 170), np.uint8)
    hsv_max = np.array((23, 101, 255), np.uint8)
    img = cv2.inRange(hsv, hsv_min, hsv_max)
    cv2.imshow('result', img)

    ch = cv2.waitKey(5)
    if ch == 27:
        cv2.imwrite(filename, img)
        print("saved")
        break

#img = cv2.imread("./image/1.jpg")
corners = []
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

img = cv2.imread(filename)
coords_corner(10000, 10000, 0, 0, 0, 320, 0, 240)  # левый верхний
coords_corner(10000, 10000, 0, 0, 320, 640, 0, 240)  # Правый верхний
coords_corner(10000, 10000, 0, 0, 0, 320, 240, 480)  # Левый нижний
coords_corner(10000, 10000, 0, 0, 320, 640, 240, 480)  # правый нижний
#img = cv2.line(img, (corners[0][0], corners[0][1]), (corners[2][0], corners[2][1]), (0,0,255), 1)
#img = cv2.line(img, (corners[1][0], corners[1][1]), (corners[3][0], corners[3][1]), (0,0,255), 1)

img = vs.read()
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
hsv_min = np.array((35, 83, 76), np.uint8)
hsv_max = np.array((90, 255, 255), np.uint8)
img = cv2.inRange(hsv, hsv_min, hsv_max)
cv2.imwrite(filename, img)
img = cv2.imread(filename)




w, h = (4, 5)  # i, j
points = []
line_up = abs(corners[0][0] - corners[1][0]) // w
line_down = abs(corners[2][0] - corners[3][0]) // w
y_lines = [corners[0][1]]
x_up = [corners[0][0] + line_up * i for i in range(w + 1)]
x_down = [corners[2][0] + line_down * i for i in range(w + 1)]
points.append(x_up)
for i in range(w + 1):
    img = cv2.line(img, (x_up[i], corners[0][1]), (x_down[i], corners[2][1]), (0,0,255), 1)
    #f.write(" ".join(map(str, x_center)) + "\n")
age = 20
age_dict = {0: 30, 1: 45, 2: 45, 3: 50}
for i in range(h - 1):
    a = []
    for j in range(w + 1):
        Rab = sqrt((x_down[j] - x_up[j]) ** 2 + (corners[2][1] - corners[0][1]) ** 2)
        k = age / Rab
        Xc = int(x_up[j] + (x_down[j] - x_up[j]) * k)
        a.append(Xc)
        Yc = int(corners[0][1] + (corners[2][1] - corners[0][1]) * k)
    points.append(a)
    y_lines.append(Yc)
    age += age_dict[i] ############################ Откалибровать значение длины
    img = cv2.line(img, (a[0], Yc), (a[-1], Yc), (0,0,255), 1)

cv2.imshow("image", img)
pole = img
cv2.waitKey(0)
cv2.destroyAllWindows()
points.append(x_down)
y_lines.append(corners[3][1])
y_lines = sorted(list(set(y_lines)))
print(*points, sep="\n")
print(y_lines, 'Y')
while True:
    img2 = pole[:]
    vs = VideoStream(0)
    img = vs.read()
    cv2.imwrite(filename, img)
    img = cv2.imread(filename)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
    hsv_min = np.array((35, 83, 76), np.uint8)
    hsv_max = np.array((90, 255, 255), np.uint8)
    img = cv2.inRange(hsv, hsv_min, hsv_max)
    for i in range(w + 1):
        for j in range(h - 1):
            print(i, j)
            x1 = points[i][j]
            x2 = points[i + 1][j + 1]
            sqr = img
            print(x1, x2, y_lines[i], y_lines[i + 1])
            sqr = sqr[y_lines[i]:y_lines[i + 1], x1:x2]
            sqr = cv2.resize(sqr, (32, 32))
            #img2 = cv2.rectangle(img2, (x1, y_lines[i]), (x2, y_lines[i + 1]), (255, 255, 0), 2)
            if sum(sum(sqr)) > 300:
                print("Finded trash in", i, j)
                img2 = cv2.rectangle(img2, (x1, y_lines[i]), (x2, y_lines[i + 1]), (0, 255, 0), 2)
            #cv2.imshow("image", sqr)
    cv2.imshow("image", img2)
    while True:
            ch = cv2.waitKey(5)
            if ch == 27:
                print("saved")
                break
        
        



    
