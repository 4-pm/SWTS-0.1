import numpy as np 
import cv2
from imutils.video import VideoStream

'''filename = 'C:/Users/User/Rover-Trasher/image/2.jpg'
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
        break'''

img = cv2.imread("./image/1.jpg")
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

img = cv2.imread('C:/Users/User/Rover-Trasher/image/2.jpg')
coords_corner(10000, 10000, 0, 0, 0, 320, 0, 240)  # левый верхний
coords_corner(10000, 10000, 0, 0, 320, 640, 0, 240)  # Правый верхний
coords_corner(10000, 10000, 0, 0, 0, 320, 240, 480)  # Левый нижний
coords_corner(10000, 10000, 0, 0, 320, 640, 240, 480)  # правый нижний


f = open("pole/pole.txt", "w")

w, h = (5, 5)  # i, j
move = abs(corners[3][0] - corners[1][0]) // int(h)
line = abs(corners[0][0] - corners[1][0]) // (w - 1)
line_y = abs(corners[0][1] - corners[2][1]) // (w - 1)
coof = {1: 1, 2: 0.5, 3: 0, 4: -0.5, 5:-1}
x1, y1, x2, y2 = (corners[0][0], corners[0][1], corners[0][0] + line, corners[0][1] + line)
x_center = [x1] + [x1 + line * i for i in range(1, w)]
print(x_center)
f.write(" ".join(map(str, x_center)) + "\n")
for i in range(1, w + 1):
    for j in range(1, h + 1):
        move2 = coof[j] * move
        img = cv2.line(img, (x_center[j - 1], y1), (int(x_center[j - 1] - move2 * i), y2), (255,255,255), 1)
        img = cv2.line(img, (x_center[0], y1), (int(x_center[-1] - move2 * i), y1), (255,255,255), 1)  # нижняя
        x_center[j - 1] = int(x_center[j - 1] - move2 * i)
    x1 = corners[0][0]
    y1 += line_y
    y2 += line_y
    x1 -= int(move)
    x2 += int(move)
    move *= 0.7
    f.write(" ".join(map(str, x_center)) + "\n")
    #line += int(move // 5)
cv2.imshow("image",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
f.close()

points = [tuple(map(int, i.split())) for i in open("./pole/pole.txt")]
print(points)
while True:
    y = corners[0][1]
    vs = VideoStream(0)
    img = vs.read()
    cv2.imshow("image", img)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
    hsv_min = np.array((35, 83, 76), np.uint8)
    hsv_max = np.array((90, 255, 255), np.uint8)
    img = cv2.inRange(hsv, hsv_min, hsv_max)
    for i in range(w):
        for j in range(h - 1):
            print(i, j)
            x1 = points[i][j]
            x2 = points[i + 1][j + 1]
            sqr = img
            sqr = sqr[y:y + line + 1, x1:x2]
            sqr = cv2.resize(sqr, (32, 32))
            #img2 = cv2.rectangle(sqr, (x1, y), (x2, y + line), (0, 0, 255))
            cv2.imshow("image", sqr)


            while True:
                ch = cv2.waitKey(5)
                if ch == 27:
                    #cv2.imwrite(filename, img)
                    print("saved")
                    break

        y += line
        



    
