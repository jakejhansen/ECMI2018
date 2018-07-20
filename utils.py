import math
import numpy.linalg as la
import numpy as np
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
Line = namedtuple('Line', ['k', 'b', 'min', 'max', 'connected_corners', 'miny', 'maxy'])

def get_rotated_point(x, y, cx, cy, theta):
    tempX = x - cx
    tempY = y - cy
    rotatedX = tempX * math.cos(math.radians(theta)) - tempY * math.sin(math.radians(theta))

    rotatedY = tempX * math.sin(math.radians(theta)) + tempY * math.cos(math.radians(theta))

    x = rotatedX + cx
    y = rotatedY + cy

    return x, y

def get_corners(box):
    corners = []
    theta = box[3]
    cx = box[0][0]
    cy = box[0][1]

    # top right
    x, y = get_rotated_point(cx + box[1] / 2, cy + box[2] / 2, cx, cy, theta)
    corners.append([x,y])
    # Top left
    x, y = get_rotated_point(cx - box[1] / 2, cy + box[2] / 2, cx, cy, theta)
    corners.append([x, y])
    # Bottom Left
    x, y = get_rotated_point(cx - box[1] / 2, cy - box[2] / 2, cx, cy, theta)
    corners.append([x, y])
    # Bottom Right
    x, y = get_rotated_point(cx + box[1] / 2, cy - box[2] / 2, cx, cy, theta)
    corners.append([x, y])

    return corners

def get_line(corner0, corner1):

    if (corner1[0] - corner0[0]) != 0:
        k = (corner1[1] - corner0[1]) / (corner1[0] - corner0[0])
    else:
        k = 0
    b = corner0[1] - k*corner0[0]

    return k, b


def get_dist(point, line):
    if point.x >= line.min and point.x <= line.max:
        dist = abs(point.y - (line.k * point.x + line.b))
        return dist
    else:
        return None


def py_ang(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'    """
    cosang = np.dot(v1, v2)
    sinang = la.norm(np.cross(v1, v2))
    return np.arctan2(sinang, cosang)

def get_box_displacement(moving_lines, lines):
    best_dist = math.inf
    PoC = None
    touching_Line = None
    for moving_line in moving_lines:
        p1_moving = Point(x=moving_line.min, y=moving_line.k * moving_line.min + moving_line.b)
        p2_moving = Point(x=moving_line.max, y=moving_line.k * moving_line.max + moving_line.b)

        for line in lines:
            p1 = Point(x = line.min, y = line.k*line.min + line.b)
            p2 = Point(x = line.max, y = line.k*line.max + line.b)

            dist = get_dist(p1, moving_line)
            if dist != None:
                if dist <= best_dist:
                    best_dist = dist
                    PoC = Point(x = p1.x, y=p1.y+best_dist)
                    touching_Line = moving_line
            dist = get_dist(p2, moving_line)
            if dist != None:
                if dist <= best_dist:
                    best_dist = dist
                    PoC = p2
                    PoC = Point(x=p2.x, y=p2.y + best_dist)
                    touching_Line = moving_line
            dist = get_dist(p1_moving, line)
            if dist != None:
                if dist <= best_dist:
                    best_dist = dist
                    PoC = p1_moving
                    touching_Line = line
            dist = get_dist(p2_moving, line)
            if dist != None:
                if dist <= best_dist:
                    best_dist = dist
                    PoC = p2_moving
                    touching_Line = line

    if PoC is not None:
        PoC = Point(x = PoC.x, y = PoC.y - best_dist)
    return best_dist, PoC, touching_Line

def best_rand_pos(cx_list):
    max_delta = 0
    x1 = 0
    x2 = 0
    for i in range(1,len(cx_list)):
        delta = cx_list[i] - cx_list[i-1]
        if (max_delta < delta):
            max_delta = delta
            x2 = cx_list[i]
            x1 = cx_list[i - 1]
    return (x2 + x1)/2, max_delta