from shapely.geometry import LineString
from shapely.geometry import Point as Point2
import matplotlib.pyplot as plt
import matplotlib
from collections import namedtuple
from itertools import cycle
import math
import numpy as np

from cornerRotations import *
from utils import *
from plotGuy import *
from Rect import Rect


if __name__ == "__main__":

    w_contain = 9
    h_contain = 5
    b_size = 2
    line_bottom = Line(k = 0, b = 0, min = 0-5, max = w_contain+5, connected_corners=[], miny=0, maxy=0)

    lines = []
    lines.append(line_bottom)

    #boxes = [[[np.random.randint(1,4), 7], 1, 1, np.random.randint(0.0001,180)]]
    boxes = []

    #Spawn and place N number of boxes
    N = 10
    cxbuffer = [4, 4]
    rotationbuffer = [128, 136]
    cxbuffer = [3, 3, 4]
    rotationbuffer = [304, 42, 31]
    for i in range(N):

        #Spawn a box
        boxes.append(Rect(np.random.randint(2,5), 6, 1, 1, np.random.randint(1,179)))
        #boxes.append(Rect(cxbuffer[i], 6, 1, 1, rotationbuffer[i]))

        print("Box " + str(i) + "cx: " + str(boxes[-1].cx) + " rot: " + str(boxes[-1].angle))

        #Get the lines of the spawned box
        moving_lines = boxes[-1].get_2_lines()

        #plot_problem(boxes, w_contain, h_contain)
        #plt.show()


        #Find the shortest distance and point of contact
        best_dist, PoC, touching_line = get_box_displacement(moving_lines, lines)
        boxes[-1].cy -= abs(best_dist)
        boxes[-1].update()

        stable = False
        while not stable:
            #Figure out tilt: -1 if right, 1 if left
            if PoC.x < boxes[-1].cx:
                tilt = -1
            else:
                tilt = 1

            # Find the corners that is not at the point of inpact
            rotating_corners = []
            for corner in boxes[-1].corners:
                if corner[0] != PoC.x:
                    rotating_corners.append(corner)



            smallest_angle = math.inf
            #Corners of falling box
            new_PoC = None
            rotating_box_angle, max_radius, tempPoC = get_smallest_angle_rotating(rotating_corners, tilt, PoC, lines, boxes)
            if rotating_box_angle < smallest_angle:
                smallest_angle = rotating_box_angle
                new_PoC = tempPoC
            #Corners of all other boxes
            rotating_other_angle, tempPoC = get_smallest_other_rotation(boxes, tilt, PoC, max_radius)
            if rotating_other_angle < smallest_angle:
                smallest_angle = rotating_other_angle
                new_PoC = tempPoC

            new_PoC = Point(x = new_PoC[0], y = new_PoC[1])

            #Set the angle to be correct
            if boxes[-1].cx > PoC.x:
                smallest_angle = -smallest_angle

            ### Rotate The box
            cx_new, cy_new = get_rotated_point(boxes[-1].cx, boxes[-1].cy, PoC.x, PoC.y, smallest_angle)
            boxes[-1].cx = cx_new
            boxes[-1].cy = cy_new

            boxes[-1].angle += smallest_angle

            boxes[-1].update()


            if min(PoC.x, new_PoC.x) <= boxes[-1].cx and boxes[-1].cx <= max(PoC.x, new_PoC.x):
                stable = True
                for line in boxes[-1].lines:
                    lines.append(line)
            else:
                PoC = Point(x = new_PoC.x, y = new_PoC.y)

        ###


    #Plot result
    plot_problem(boxes, w_contain, h_contain)
    try:
        plt.plot(PoC.x, PoC.y, 'ro')
    except:
        import IPython
        IPython.embed()

    plt.show()
    ##

    print("done")