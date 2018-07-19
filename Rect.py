from collections import namedtuple

from utils import *
class Rect(object):
    Line = namedtuple('Line', ['k', 'b', 'min', 'max', 'connected_corners', 'miny','maxy'])
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
                                    connected_corners = [i, (i+1) % 4],
                                    miny=min(corner0[1], corner1[1]),
                                    maxy=max(corner0[1], corner1[1]))
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