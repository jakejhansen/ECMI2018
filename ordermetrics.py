import itertools as it
import numpy as np
import objects as objs

def ocf(rects):
    """
    Return the value of the orientational correlation function
    for the given collection of rectangular objects.
    """
    x = 0
    n = 0
    for rect0, rect1 in it.combinations(rects, 2):
        y = None
        for (u0, n0), (u1, n1) in it.product(rect0.get_normals(), rect1.get_normals()):
            if n0 == n1:
                y0 = n0 * np.arccos(np.dot(u0, u1))
                if y is None:
                    y = y0
                else:
                    y = max(y, y0)
        if not (y is None):
            x += np.cos(y)
            n += 1
    return x / n

def ocf_np(a):
    """
    Return the value of the orientational correlation function
    for the given collection of rectangular objects represented
    as a NumPy array with x, y, width, height and angle
    on the columns of each row.
    """
    rs = []
    for b in a:
        rs.append(objs.rect(np.array([b[0], b[1]]), np.array([b[2], b[3]]), b[4]))
    return ocf(rs)
