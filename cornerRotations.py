from shapely.geometry import LineString
from shapely.geometry import Point as Point2
import math
import numpy as np
from utils import *
from plotGuy import *

def get_smallest_angle_rotating(corners, tilt, PoC, lines, boxes):
    smallest_angle = math.inf
    max_radius = math.inf
    new_PoC = None

    for corner in corners:
        if (tilt == 1 and corner[0] < PoC.x) or (tilt == -1 and corner[0] > PoC.x):
            if abs(PoC.x - corner[0]) > 0.000001:
                radius = math.sqrt((corner[0] - PoC.x) ** 2 + (corner[1] - PoC.y) ** 2)
                if radius > max_radius:
                    max_radius = radius

                p = Point2(PoC.x, PoC.y)
                c = p.buffer(radius).boundary

                plot_problem(boxes, w_contain= 9, h_contain= 5)
                plt.plot(corner[0], corner[1], 'bo')
                for line in lines:

                    if abs(line.min - line.max) < 0.001:
                        l = LineString([(line.min, line.miny), (line.min, line.maxy)])
                    else:
                        l = LineString(
                            [(line.min, line.min * line.k + line.b), (line.max, line.max * line.k + line.b)])
                    i = c.intersection(l)

                    if i.geom_type == "MultiPoint":

                        p = i.geoms[0].coords[0]
                        angle = math.degrees(py_ang(np.array([corner[0] - PoC.x, corner[1] - PoC.y]),
                                                    np.array([p[0] - PoC.x, p[1] - PoC.y])))
                        if angle < smallest_angle:
                            smallest_angle = angle
                            new_PoC = p

                        plt.plot(p[0], p[1], 'ro')

                        p = i.geoms[1].coords[0]
                        angle = math.degrees(py_ang(np.array([corner[0] - PoC.x, corner[1] - PoC.y]),
                                                    np.array([p[0] - PoC.x, p[1] - PoC.y])))
                        if angle < smallest_angle:
                            smallest_angle = angle
                            new_PoC = p

                        plt.plot(p[0], p[1], 'ro')

                    if i.geom_type == "Point":
                        ps = i.coords[0]
                        angle = math.degrees(py_ang(np.array([corner[0] - PoC.x, corner[1] - PoC.y]),
                                                    np.array([ps[0] - PoC.x, ps[1] - PoC.y])))
                        if angle < smallest_angle:
                            smallest_angle = angle
                            new_PoC = ps
                        plt.plot(ps[0], ps[1], 'ro')

    plt.show()
    return smallest_angle, max_radius, new_PoC


def get_smallest_other_rotation(boxes, tilt, PoC, max_radius):
    smallest_angle = math.inf
    new_PoC = None
    for box in boxes[:-1]:
        for corner in box.corners:
            if (tilt == 1 and corner[0] < PoC.x) or (tilt == -1 and corner[0] > PoC.x):
                if abs(PoC.x - corner[0]) > 0.000001:
                    dist_to_PoC = math.sqrt((corner[0] - PoC.x) ** 2 + (corner[1] - PoC.y) ** 2)
                    if dist_to_PoC <= max_radius:
                        p = Point2(PoC.x, PoC.y)
                        c = p.buffer(dist_to_PoC).boundary
                        for line in boxes[-1].lines:

                            if abs(line.min - line.max) < 0.001:
                                l = LineString([(line.min, line.miny), (line.min, line.maxy)])
                            else:
                                l = LineString(
                                    [(line.min, line.min * line.k + line.b),
                                     (line.max, line.max * line.k + line.b)])

                            i = c.intersection(l)

                            if i.geom_type == "MultiPoint":

                                p = i.geoms[0].coords[0]
                                angle = math.degrees(py_ang(np.array([corner[0] - PoC.x, corner[1] - PoC.y]),
                                                            np.array([p[0] - PoC.x, p[1] - PoC.y])))
                                # print(angle)
                                if angle < smallest_angle:
                                    smallest_angle = angle
                                    new_PoC = p
                                # plt.plot(p[0], p[1], 'bo')

                                p = i.geoms[1].coords[0]
                                angle = math.degrees(py_ang(np.array([corner[0] - PoC.x, corner[1] - PoC.y]),
                                                            np.array([p[0] - PoC.x, p[1] - PoC.y])))
                                # print(angle)
                                if angle < smallest_angle:
                                    smallest_angle = angle
                                    new_PoC = p

                            if i.geom_type == "Point":
                                ps = i.coords[0]
                                angle = math.degrees(py_ang(np.array([corner[0] - PoC.x, corner[1] - PoC.y]),
                                                            np.array([ps[0] - PoC.x, ps[1] - PoC.y])))
                                # print(angle)
                                if angle < smallest_angle:
                                    smallest_angle = angle
                                    new_PoC = ps
                                # plot_case(boxes, w_contain, h_contain, points=[PoC, Point(x = ps[0], y = ps[1]), Point(x = corner[0], y = corner[1])])
                                # plt.show()

    return smallest_angle, new_PoC