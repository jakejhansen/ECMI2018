import shapely.geometry
import shapely.affinity
import numpy as np

class RotatedRect:
    def __init__(self, cx, cy, w, h, angle):
        self.cx = cx
        self.cy = cy
        self.w = w
        self.h = h
        self.angle = angle

    def get_contour(self):
        w = self.w
        h = self.h
        c = shapely.geometry.box(-w/2.0, -h/2.0, w/2.0, h/2.0)
        rc = shapely.affinity.rotate(c, self.angle)
        return shapely.affinity.translate(rc, self.cx, self.cy)

    def intersection(self, other):
        return self.get_contour().intersection(other.get_contour())


b_size = 2
r1 = RotatedRect(10, 15, b_size, b_size, 30)
r2 = RotatedRect(15, 15, b_size, b_size, 0)

from matplotlib import pyplot
from descartes import PolygonPatch

boxes = []

for i in range(1000):
    best_candidate = RotatedRect(32, 32, b_size, b_size, 0)
    for h in range(100):
        r_candidate = RotatedRect(np.random.randint(0,30),
                                  np.random.randint(0,30),
                                  b_size, b_size,
                                  np.random.randint(0,180))
        flag = True
        for box in boxes:
            if box.intersection(r_candidate).area > 0:
                flag = False
                break

        if flag == True and r_candidate.cy < best_candidate.cy:
            best_candidate = r_candidate

    boxes.append(best_candidate)
    fig = pyplot.figure(1, figsize=(10, 4))
    ax = fig.add_subplot(121)
    ax.set_xlim(-2, 32)
    ax.set_ylim(-2, 32)

    for box in boxes:
        ax.add_patch(PolygonPatch(box.get_contour(), fc='#990000', alpha=0.7))
    #ax.add_patch(PolygonPatch(r1.get_contour(), fc='#990000', alpha=0.7))
    #ax.add_patch(PolygonPatch(r2.get_contour(), fc='#000099', alpha=0.7))
    #intersect = r1.intersection(r2)
    #if intersect.area > 0:
    #    ax.add_patch(PolygonPatch(r1.intersection(r2), fc='#009900', alpha=1))

    pyplot.show()
    import time
    time.sleep(0.1)