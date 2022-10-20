import cv2
import numpy as np
from math import degrees
#from imutils.video import VideoStream


def range_p(x1, y1, x2, y2):  # расстояние между точками
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def draw_point(img, point, name):  # рисование на фото
    cv2.circle(img, point, 5, color, 2)
    cv2.putText(img, name, (point[0] + 10, point[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

def points_returner(img):
    hsv_min = np.array((92, 59, 142), np.uint8)
    hsv_max = np.array((127, 187, 221), np.uint8)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    thresh = cv2.inRange(hsv, hsv_min, hsv_max)
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_L1)
    # print(len(contours))
    for i in range(len(contours)):
        moments = cv2.moments(contours[i])

        # moments = cv2.moments(thresh, 1)
        dM01 = moments['m01']
        dM10 = moments['m10']
        dArea = moments['m00']

        if 1000 > dArea > 50:
            x = int(dM10 / dArea)
            y = int(dM01 / dArea)
            points.append([x, y])
            # cv2.circle(img, (x, y), 5, color_yellow, 2)
            # cv2.putText(img, "%d-%d" % (x, y), (x + 10, y - 10),
            # cv2.FONT_HERSHEY_SIMPLEX, 1, color_yellow, 2)

    print(points, "points")

    points2 = [[range_p(points[0][0], points[0][1], points[1][0], points[1][1]),
                range_p(points[0][0], points[0][1], points[2][0], points[2][1])],

               [range_p(points[1][0], points[1][1], points[0][0], points[0][1]),
                range_p(points[1][0], points[1][1], points[2][0], points[2][1])],

               [range_p(points[2][0], points[2][1], points[1][0], points[1][1]),
                range_p(points[2][0], points[2][1], points[0][0], points[0][1])]
               ]

    left = points[points2.index(min(points2, key=lambda _: sum(_)))]
    draw_point(img, left, "Left")
    points.remove(left)

    points2 = (range_p(left[0], left[1], points[0][0], points[0][1]),
               range_p(left[0], left[1], points[1][0], points[1][1]))
    # print(points2, "2 points")

    right = points[points2.index(min(points2))]
    draw_point(img, right, "Right")
    back = points[points2.index(max(points2))]
    draw_point(img, back, "Back")

    center = [(right[0] + back[0]) // 2, (right[1] + back[1]) // 2]
    front = [(right[0] + left[0]) // 2, (right[1] + left[1]) // 2]

    # для мусора
    trash_p = 0
    hsv_min2 = np.array((59, 150, 106), np.uint8)
    hsv_max2 = np.array((102, 255, 174), np.uint8)
    img2 = cv2.imread(f"./image/{num}.jpg")
    hsv2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
    thresh2 = cv2.inRange(hsv2, hsv_min2, hsv_max2)
    cv2.namedWindow("tresh", cv2.WINDOW_NORMAL)
    cv2.resizeWindow('tresh', 600, 600) 
    cv2.imshow('tresh', thresh2) 

    contours2, _ = cv2.findContours(thresh2.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_L1)
    dArea_n = 0
    for i in range(len(contours2)):
        moments2 = cv2.moments(contours2[i])

        # moments = cv2.moments(thresh, 1)
        dM01 = moments2['m01']
        dM10 = moments2['m10']
        dArea = moments2['m00']

        if dArea > dArea_n:
            x = int(dM10 / dArea)
            y = int(dM01 / dArea)
            trash_p = [x, y]
            dArea_n = dArea
    draw_point(img, trash_p, "Trash")

    return center, front, trash_p

def angle_returner(v_bot, v_trash):
    v_bot = unit_vector(v_bot)
    v_trash = unit_vector(v_trash)
    return degrees(np.arccos(np.clip(np.dot(v_bot, v_trash), -1.0, 1.0)))

if __name__ == '__main__':
    def callback(*arg):
        print(arg)


cv2.namedWindow("result")
cv2.namedWindow("hsv")

#cap = cv2.VideoStream(src=0).start()

color = (255, 0, 0)

for num in range(1, 9):
    left, right, back = (0, 0), (0, 0), (0, 0)
    points = []
    img = cv2.imread(f"./image/{num}.jpg")
    center, front, trash = points_returner(img)


    cv2.line(img, center, front, (0, 0, 255), 2)
    cv2.line(img, center, trash, (0, 0, 255), 2)

    v_bot = np.array([front[0] - center[0], front[1] - center[1]])
    v_trash = np.array([trash[0] - center[0], trash[1] - center[1]])
    print(angle_returner(v_bot, v_trash))

    cv2.namedWindow("main", cv2.WINDOW_NORMAL)
    cv2.resizeWindow('main', 600, 600) 
    cv2.imshow('main', img) 

    while True:
        ch = cv2.waitKey(5)
        if ch == 27:
            break

#cap.release()
cv2.destroyAllWindows()