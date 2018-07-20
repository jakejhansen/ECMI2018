import matplotlib.pyplot as plt
import matplotlib
from itertools import cycle
import numpy as np

def plot_problem(boxes, w_contain, h_contain, wall_size=0.3):
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
    f, (ax1) = plt.subplots(1, 1, figsize=(4, 4))
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


def abline(slope, intercept):
    """Plot a line from slope and intercept"""
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vals = intercept + slope * x_vals
    plt.axis('equal')
    plt.plot(x_vals, y_vals, '--')

def plot_case(boxes, w_contain, h_contain, lines = None, points = None):
    plot_problem(boxes, w_contain, h_contain)
    if lines is not None:
        for line in lines:
            abline(line.k, line.b)
    if points is not None:
        for point in points:
            plt.plot(point.x, point.y, 'ro')

    plt.show()
