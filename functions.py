import cv2
import numpy as np
from math import degrees, atan2


def range_p(x1, y1, x2, y2):  # расстояние между точками
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

#def unit_vector(vector):
    #""" Returns the unit vector of the vector.  """
    #return vector / np.linalg.norm(vector)

def draw_point(img, point, name):  # рисование на фото
    cv2.circle(img, point, 5, (255, 0, 0), 2)
    cv2.putText(img, name, (point[0] + 10, point[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

def points_returner(img):
    points = []
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

    #print(points, "points")

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
    img2 = img
    hsv2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
    thresh2 = cv2.inRange(hsv2, hsv_min2, hsv_max2)
    #cv2.namedWindow("tresh", cv2.WINDOW_NORMAL)
    #cv2.resizeWindow('tresh', 600, 600) 
    #cv2.imshow('tresh', thresh2) 

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
    return round(degrees(atan2(v_trash[1], v_trash[0]) - atan2(v_bot[1], v_bot[0])))

def start_tresh(img):
    hsv_min2 = np.array((59, 150, 106), np.uint8)
    hsv_max2 = np.array((102, 255, 174), np.uint8)
    hsv2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    thresh2 = cv2.inRange(hsv2, hsv_min2, hsv_max2)

    contours2, _ = cv2.findContours(thresh2.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_L1)
    dArea_n = 0
    for i in range(len(contours2)):
        moments2 = cv2.moments(contours2[i])

        dM01 = moments2['m01']
        dM10 = moments2['m10']
        dArea = moments2['m00']

        if dArea > dArea_n:
            dArea_n = dArea

    if dArea_n > 100:
        return True
    return False