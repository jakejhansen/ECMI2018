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
        y = 0
        m = 0

        # This does not work.
        # Try canonicalizing orientations.
        for u0, u1 in zip(rect0.get_normals(), rect1.get_normals()):
            y += np.dot(u0, u1)
            m += 1

        x += y / m
        n += 1

    return x / n
