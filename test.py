import matplotlib.pyplot as plt
import matplotlib
from itertools import cycle


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
        cx = box[0][0]
        cy = box[0][1]
        w = box[1]
        h = box[2]
        rot = box[3]
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
    plt.show()


#Params and variables (boxes)
w_contain = 10
h_contain = 10
boxes = [[[3, 2], 2, 1, 50], [[5, 3], 2, 2, 45]]

#Plot the problem
plot_problem(boxes, w_contain, h_contain)
