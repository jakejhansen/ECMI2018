import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import objects as objs
import ordermetrics as oms
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

def plot2(cont, parts):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for rect in parts:
        c = rect.get_corners()
        p = plt.Polygon([c[0], c[2], c[3], c[1]], closed = True, edgecolor = 'r')
        ax.add_patch(p)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    plt.axis('equal')
    plt.show()

def plot3(cont, parts):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for rect in parts:
        v = np.zeros([8, 3])
        for i in range(8):
            v[i, :] = rect.get_corners()[i, :]
        verts = [
            [v[0], v[2], v[3], v[1]],
            [v[4], v[6], v[7], v[5]],
            [v[3], v[1], v[5], v[7]],
            [v[0], v[2], v[6], v[4]],
            [v[0], v[4], v[5], v[1]],
            [v[2], v[3], v[7], v[6]]]
        ax.scatter3D(v[:, 0], v[:, 1], v[:, 2])
        ax.add_collection3d(Poly3DCollection(verts,
            facecolors = 'cyan', linewidths = 1, edgecolors = 'r',
            alpha = 0.25, antialiased = False))
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.axis('equal')
    plt.show()

# plot2(None, [
#     objs.rect(np.array([69, 42]), np.array([13, 7]), np.deg2rad(10)),
#     objs.rect(np.array([22, 22]), np.array([13, 7]), np.deg2rad(10 + 22))])
plot3(None, [
    objs.rect(np.array([69, 42, 20]), np.array([20, 13, 7]), np.deg2rad(10)),
    objs.rect(np.array([22, 22, 22]), np.array([20, 13, 7]), np.deg2rad(10 + 22))])
