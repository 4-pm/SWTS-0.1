import cv2
import numpy as np
from imutils.video import VideoStream


def range_p(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def draw_point(img, point, name):
    cv2.circle(img, point, 5, color, 2)
    cv2.putText(img, name, (point[0] + 10, point[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)


if __name__ == '__main__':
    def callback(*arg):
        print(arg)

cv2.namedWindow("result")

cap = VideoStream(src=0).start()
hsv_min = np.array((0, 158, 114), np.uint8)
hsv_max = np.array((193, 255, 255), np.uint8)

color = (255, 255, 255)

for i in range(1, 6):
    left, right, back = (0, 0), (0, 0), (0, 0)
    points = []
    img = cv2.imread(f"./image/{i}.jpg")
    #img = cv2.flip(img, 1)  # отражение кадра вдоль оси Y
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    thresh = cv2.inRange(hsv, hsv_min, hsv_max)
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_L1)
    print(len(contours))
    for i in range(len(contours)):
        moments = cv2.moments(contours[i])

    #moments = cv2.moments(thresh, 1)
        dM01 = moments['m01']
        dM10 = moments['m10']
        dArea = moments['m00']

        if 500 > dArea > 100:
            x = int(dM10 / dArea)
            y = int(dM01 / dArea)
            points.append([x, y])
            #cv2.circle(img, (x, y), 5, color_yellow, 2)
            #cv2.putText(img, "%d-%d" % (x, y), (x + 10, y - 10),
                        #cv2.FONT_HERSHEY_SIMPLEX, 1, color_yellow, 2)

    print(points)

    points2 = [[range_p(points[0][0], points[0][1], points[1][0], points[1][1]),
                range_p(points[0][0], points[0][1], points[2][0], points[2][1])],

               [range_p(points[1][0], points[1][1], points[0][0], points[0][1]),
                range_p(points[1][0], points[1][1], points[2][0], points[2][1])],

               [range_p(points[2][0], points[2][1], points[1][0], points[1][1]),
                range_p(points[2][0], points[2][1], points[0][0], points[0][1])]
               ]

    left = points[points2.index(min(points2, key=lambda _: sum(_)))]
    print(left)
    draw_point(img, left, "Left")
    points.remove(left)

    points2 = (range_p(left[0], left[1], points[0][0], points[0][1]),
               range_p(left[0], left[1], points[1][0], points[1][1]))
    print(points2, "2 points")

    right = points[points2.index(min(points2))]
    draw_point(img, right, "Right")
    back = points[points2.index(max(points2))]
    draw_point(img, back, "Back")






    cv2.imshow('result', img)

    while True:
        ch = cv2.waitKey(5)
        if ch == 27:
            break

#cap.release()
cv2.destroyAllWindows()