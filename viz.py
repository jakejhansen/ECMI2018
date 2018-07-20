import random
from cornerRotations import *
from utils import *
from plotGuy import *
from Rect import Rect

if __name__ == "__main__":

    w_contain = 9
    h_contain = 5
    eps = 0.0001
    a = 0
    N = 13
    b = w_contain
    box_size = 1.3

    lines = []
    boxes = []
    cx_list = []
    cy_list = []
    
    line_bottom = Line(k = 0, b = 0, min = -2, max = w_contain + 2, connected_corners=[], miny=0, maxy=0)
    
    k1, b1 = get_line([0, 0],[eps,h_contain])
    k2, b2 = get_line([w_contain, 0], [w_contain + eps, h_contain])
    
    left_side = Line(k = k1, b = b1, min = 0, max = eps, connected_corners = [], miny = 0, maxy = w_contain)
    right_side = Line(k = k2, b = b2, min = w_contain, max = w_contain + eps, connected_corners = [], miny = 0, maxy = h_contain)

    lines.append(line_bottom)
    lines.append(left_side)
    lines.append(right_side)
    
    cx_list.append(a)
    cx_list.append(b)
    
    cx_buffer = [0.93, 1.3]
    rotation_buffer = [-40, 0]
    
    prev_pos = 0
    cx_start = random.uniform(a + (box_size * math.sqrt(2) / 2 + eps), b - (box_size * math.sqrt(2) / 2 + eps))
    cx_list.append(cx_start)
    N_layer = (int(w_contain / (box_size*math.sqrt(2))) + 1)
    counter = 1
    
    im_n = -1
    for i in range(N):
        if N % N_layer == 0:
            del cx_list[N_layer*counter:]
            counter += counter
            
        boxes.append(Rect(cx_start, 10, box_size, box_size, np.random.randint(1,89)))
        #boxes.append(Rect(cx_buffer[i], 6, box_size, box_size, rotation_buffer[i]))
        
        #print("Box " + str(i) + "cx: " + str(boxes[-1].cx) + " rot: " + str(boxes[-1].angle))

        #Get the lines of the spawned box
        moving_lines = boxes[-1].get_2_lines()
        
        #Find the shortest distance and point of contact
        best_dist, PoC, touching_line = get_box_displacement(moving_lines, lines)
        boxes[-1].cy -= abs(best_dist)
        boxes[-1].update()

        stable = False
        
        while not stable:
            
            im_n += 1

            
            #Figure out tilt: -1 if right, 1 if left
            if PoC.x < boxes[-1].cx:
                tilt = -1
            else:
                tilt = 1

            # Find the corners that is not at the point of inpact
            rotating_corners = []
            for corner in boxes[-1].corners:
                if corner[0] != PoC.x:
                    rotating_corners.append(corner)

            smallest_angle = math.inf
            #Corners of falling box
            new_PoC = None
            
            rotating_box_angle, max_radius, tempPoC, im_n = get_smallest_angle_rotating(rotating_corners, tilt, PoC, lines, boxes, im_n)
            
            if rotating_box_angle < smallest_angle:
                smallest_angle = rotating_box_angle
                new_PoC = tempPoC
                
            #Corners of all other boxes
            rotating_other_angle, tempPoC, im_n = get_smallest_other_rotation(boxes, tilt, PoC, max_radius, im_n)
            
            
            if rotating_other_angle < smallest_angle:
                smallest_angle = rotating_other_angle
                new_PoC = tempPoC

            new_PoC = Point(x = new_PoC[0], y = new_PoC[1])

            #Set the angle to be correct
            if boxes[-1].cx > PoC.x:
                smallest_angle = -smallest_angle

            ### Rotate The box
            cx_new, cy_new = get_rotated_point(boxes[-1].cx, boxes[-1].cy, PoC.x, PoC.y, smallest_angle)
            boxes[-1].cx = cx_new
            boxes[-1].cy = cy_new

            # if (abs(boxes[-1].angle + smallest_angle) > 90):
            #     boxes[-1].angle = 90
            #     boxes[-1].update()
            #     min_x = math.inf
            #     min_y = math.inf
            #     for corner in boxes[-1].corners:
            #         if corner[0] < min_x:
            #             min_x = corner[0]
            #             min_y = corner[1]
            #     PoC = Point(x = min_x, y = min_y)
            #     boxes[-1].update()
            #     continue
            # else:
            
            boxes[-1].angle += smallest_angle
            boxes[-1].update()
            
            if min(PoC.x, new_PoC.x) <= boxes[-1].cx and boxes[-1].cx <= max(PoC.x, new_PoC.x):
                stable = True
                cx_start = best_rand_pos(cx_list, boxes, box_size, a, b, eps)
                cx_list.append(cx_start)
                for line in boxes[-1].lines:
                    lines.append(line)
            else:
                PoC = Point(x = new_PoC.x, y = new_PoC.y)

        
            
        #print("cx_start ",cx_start)

    #Plot result
    plot_problem(boxes, w_contain, h_contain)
    try:
        
        plt.plot(PoC.x, PoC.y, 'ro')
    except:
        import IPython
        IPython.embed()

    im_n = get_png(im_n)
    
    plt.show()
    #create_gif(plt.show())
    ##

    print("done")
