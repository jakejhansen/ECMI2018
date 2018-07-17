import matplotlib.pyplot as plt
import matplotlib
from collections import namedtuple
from itertools import cycle
import math
import numpy as np


def plot_problem(boxes, w_container, h_container, wall_size=0.3):
    """
    Plots the problem
    Args:
        boxes: List of boxes [ [[cx, cy], w, h, rotation], ... ]
        w_container: width of the container
        h_container: height of the container
        wall_size: size of the walls (default = 0.3)

    Returns:
        None: Plots the figure
    """

    # Define axies
    f, (ax1) = plt.subplots(1, 1, figsize=(3, 3))
    f.subplots_adjust(hspace=0, wspace=0)

    # Plot the contianer
    left_side = matplotlib.patches.Rectangle((-wall_size, 0), wall_size, h_contain)
    right_side = matplotlib.patches.Rectangle((w_contain, 0), wall_size, h_contain)
    bottom = matplotlib.patches.Rectangle((-wall_size, -wall_size), w_contain + 2 * wall_size, wall_size)
    ax1.add_patch(left_side)
    ax1.add_patch(right_side)
    ax1.add_patch(bottom)

    # Used as overhead, to create some space above the container
    buffer = matplotlib.patches.Rectangle((0, h_contain), w_contain, 5, facecolor='white')
    ax1.add_patch(buffer)

    cycol = cycle('bgrcmk')
    # Run over the boxes
    for box in boxes:
        cx = box.cx
        cy = box.cy
        w = box.w
        h = box.h
        rot = box.angle
        #Define rotation
        tr = matplotlib.transforms.Affine2D().rotate_deg_around(cx, cy, rot)
        t = tr + ax1.transData
        col = next(cycol)
        #Rotate the object
        rect1 = matplotlib.patches.Rectangle((cx - w / 2, cy - h / 2), w, h,
                                             linewidth=0, edgecolor=col, facecolor=col, transform=t)

        ax1.add_patch(rect1)


    #Show the plot
    plt.axis('equal')
    #plt.show()


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

def abline(slope, intercept):
    """Plot a line from slope and intercept"""
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vals = intercept + slope * x_vals
    plt.plot(x_vals, y_vals, '--')

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


class Rect(object):
    Line = namedtuple('Line', ['k', 'b', 'min', 'max', 'connected_corners'])
    Point = namedtuple('Point', ['x', 'y'])

    def __init__(self, cx, cy, w, h, angle):
        self.cx = cx
        self.cy = cy
        self.w = w
        self.h = h
        self.angle = angle
        self.corners = self.get_corners()
        self.lines = self.get_lines()

    def get_corners(self):
        corners = []
        theta = self.angle
        cx = self.cx
        cy = self.cy
        w = self.w
        h = self.h

        # top right
        x, y = get_rotated_point(cx + w / 2, cy + h / 2, cx, cy, theta)
        corners.append([x,y])
        # Top left
        x, y = get_rotated_point(cx - w / 2, cy + h / 2, cx, cy, theta)
        corners.append([x, y])
        # Bottom Left
        x, y = get_rotated_point(cx - w / 2, cy - h / 2, cx, cy, theta)
        corners.append([x, y])
        # Bottom Right
        x, y = get_rotated_point(cx + w / 2, cy - h / 2, cx, cy, theta)
        corners.append([x, y])

        return corners

    def get_lines(self):
        moving_lines = []
        corners = self.corners
        for i in range(4):
            corner0 = corners[i]
            corner1 = corners[(i + 1) % 4]
            k, b = get_line(corner0, corner1)
            moving_line = Rect.Line(k=k,
                                    b=b,
                                    max=max(corner0[0], corner1[0]),
                                    min=min(corner0[0], corner1[0]),
                                    connected_corners = [i, (i+1) % 4])
            moving_lines.append(moving_line)
            #abline(k, b)

        return moving_lines

    def get_2_lines(self):
        result = []
        corners_y = [x[1] for x in self.corners]
        #Find the minimum corner
        min_corner = np.argmin(corners_y)
        #plt.plot(self.corners[min_corner][0], self.corners[min_corner][1], 'ro')

        #Any line connected to the minmum corner (y) is added to the list
        for line in self.lines:
            if min_corner in line.connected_corners:
                result.append(line)

        return result

    def update(self):
        self.corners = self.get_corners()
        self.lines = self.get_lines()

def get_box_displacement(moving_lines, lines):
    best_dist = math.inf
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
            dist = get_dist(p2, moving_line)
            if dist != None:
                if dist <= best_dist:
                    best_dist = dist
            dist = get_dist(p1_moving, line)
            if dist != None:
                if dist <= best_dist:
                    best_dist = dist
            dist = get_dist(p2_moving, line)
            if dist != None:
                if dist <= best_dist:
                    best_dist = dist

    return best_dist

if __name__ == "__main__":
    Line = namedtuple('Line', ['k', 'b', 'min', 'max', 'connected_corners'])
    Point = namedtuple('Point', ['x', 'y'])

    w_contain = 5
    h_contain = 5
    b_size = 2
    line_bottom = Line(k = 0, b = 0, min = 0, max = w_contain, connected_corners=[])
    #line_bottom_k, line_bottom_b = 0, 0
    #abline(line_bottom_k, line_bottom_b)

    lines = []
    lines.append(line_bottom)

    #boxes = [[[np.random.randint(1,4), 7], 1, 1, np.random.randint(0.0001,180)]]
    boxes = []

    for i in range(2):
        #Spawn a box
        boxes.append(Rect(np.random.randint(1,4), 7, 1, 1, np.random.randint(0.1,45)))

        #Plot what we have
        plot_problem(boxes, w_contain, h_contain)
        plt.show()

        #Get the lines of the spawned box
        moving_lines = boxes[-1].get_2_lines()


        #Find the shortest distance
        best_dist = get_box_displacement(moving_lines, lines)
        boxes[0].get_2_lines()
        boxes[-1].cy -= abs(best_dist)
        boxes[-1].update()
        for line in boxes[-1].lines:
            lines.append(line)

        plot_problem(boxes, w_contain, h_contain)
        plt.show()
        print("")

    print("done")