import itertools as it
import numpy as np

class rect:
    """
    Rectangular object, currently only in two dimensions.

    Examples
    --------
    The following examples demonstrate basic usage.

    >>> r = rect(np.array([69, 42]), np.array([13, 7]), np.deg2rad(90))
    >>> r.get_corners()
    np.array([[76.0, 29.0], [62.0, 29.0], [76.0, 55.0], [62.0, 55.0]])
    >>> r.get_aabb().get_corners()
    np.array([[62.0, 29.0], [62.0, 55.0], [76.0, 29.0], [76.0, 55.0]])
    """

    def __init__(self, com, halfexts, eangles):
        self.ndim = len(com)
        self.com = com
        self.halfexts = halfexts
        self.eangles = eangles

    def get_ndim(self):
        """
        Return the number of dimensions.
        """
        return self.ndim

    def get_com(self):
        """
        Return the center of mass vector.
        """
        return self.com

    def get_halfexts(self):
        """
        Return the half-extent vector.
        """
        return self.halfexts

    def get_eangles(self):
        """
        Return the Euler angles.
        """
        return self.eangles

    def get_corners(self):
        """
        Return the corners in the lexicographical order of the signs.
        The result may not form a Hamiltonian cycle.
        """
        c, s = np.cos(self.eangles), np.sin(self.eangles)
        # Not like this.
        r = np.array([[c, -s], [s, c]]) if self.get_ndim() == 2 else np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
        return np.array([self.com + np.dot(r, v * self.halfexts)
            for v in it.product(*it.repeat([-1, 1], self.ndim))])

    def get_aabb(self):
        """
        Return the axis-aligned bounding box.
        """
        c, s = np.cos(self.eangles), np.sin(self.eangles)
        r = np.array([[c, s], [s, c]])
        return rect(self.get_com(), np.abs(np.dot(r, self.halfexts)), 0)

    def get_normal(self):
        """
        Return the outwards-pointing principal normal vector.
        """
        c, s = np.cos(self.eangles), np.sin(self.eangles)
        r = np.array([[c, -s], [s, c]])
        u = np.array([1, 0])
        return np.dot(r, u)

    def get_normals(self):
        """
        Return the outwards-pointing normal vectors and
        their numbers of orientational symmetries in an arbitrary order.

        This only works for squares and rectangles.
        """
        c, s = np.cos(self.eangles), np.sin(self.eangles)
        r = np.array([[c, -s], [s, c]])
        us = np.array([[1, 0], [0, 1], [-1, 0], [0, -1]])
        nsyms = 4 if self.halfexts[0] == self.halfexts[1] else 2
        return [(np.dot(r, u), nsyms) for u in us]
