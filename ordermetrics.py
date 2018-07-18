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
        y = -1
        for u0, u1 in it.product(rect0.get_normals(), rect1.get_normals()):
            y = max(y, np.arccos(np.dot(u0, u1)))
        nsyms = np.sqrt(rect0.get_nsyms() * rect1.get_nsyms())
        x += np.cos(nsyms * y)
        n += 1
    return x / n
