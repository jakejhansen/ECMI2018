from Box2D import *
import pygame, sys, math, random
from pygame.locals import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math
from ordermetrics import *

def create_dynamic_box(xpos):
    body=world.CreateDynamicBody(position=(xpos/pygame_box2d_ratio,pygame_screen_y/10), angle=np.random.randint(0,179))
    box=body.CreatePolygonFixture(box=(box_size/2.0,box_size/2.0), density=0.1, friction=1, restitution = 0)
    return body

def isInside(box):
    """Finds out if a box is inside the container region"""
    AABB = box.fixtures[0].GetAABB(0)
    if AABB.lowerBound[1] > -1 and AABB.upperBound[1] < pillar_height + ground_height and AABB.lowerBound[0] > 0.5 and \
            AABB.upperBound[0] < pos_p2:
        return True
    else:
        return False

def inside(boxeslist):
    sum = 0
    for box in boxeslist:
        if isInside(box):
            sum += 1
        else:
            pass
    return sum

def get_ofc():
    boxesinside = []
    for box in boxeslist:
        if isInside(box):
            boxesinside.append(box)

    info = []
    for box in boxesinside:
        fix = box.fixtures[0].body
        #print(fix.position.x, fix.position.y, box_size, box_size, math.radians(fix.angle))
        info.append([fix.position.x, fix.position.y, box_size, box_size, math.radians(fix.angle)])

    return(ocf_np(np.array(info)))

def drawAABB(box):
    f = box.fixtures[0]
    AABB = f.GetAABB(0)
    lx = AABB.lowerBound.x * 10
    uy = AABB.upperBound.y * 10
    w = AABB.extents.x * 2 * 10
    h = AABB.extents.y * 2 * 10
    pygame.draw.rect(windowSurface,(255,255,0),
        (lx,
        pygame_screen_y - uy,
        w,
        h))
    pygame.display.update()

def stop(boxeslist):
    if box_size < 5:
        val = 60
    elif box_size < 10:
        val = 20
    elif box_size < 15:
        val = 15
    else:
        val = 8
    if len(boxeslist) < 2 * val:
        return False
    else:
        for box in boxeslist[-val:]:
            if isInside(box):
                return False
    return True

def plotti(total_result):
    means = []
    for result in total_result:
        result = result[result > 0]
        for den in result[1:]:
            plt.plot(result[0] + (np.random.rand() - 0.5) * 0.1, den, 'bo')
        means.append(np.mean(result[1:]))
    plt.plot(list(range(int(total_result[0][0]), int(total_result[-1][0]) + 1)), means, 'r')
    plt.xlabel('Object Size wrt Container Size')
    plt.ylabel('Packing Density [%]')
    #plt.title('Packing Density as a function of Square Size')
    plt.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter('%d/39'))
    plt.grid()
    plt.rc('font', size=15)
    plt.show()

def animation():
    # clean screen
    windowSurface.fill(BLACK)
    # draw ground
    pygame.draw.rect(windowSurface, GREEN,
                     (0, pygame_screen_y - (ground_height * pygame_box2d_ratio), pygame_screen_x, pygame_screen_y))

    # draw pillars
    pygame.draw.rect(windowSurface, GREEN, (5.0 - (0.5 * pygame_box2d_ratio), pygame_screen_y - (
            (pillar_height * pygame_box2d_ratio) + (ground_height * pygame_box2d_ratio)),
                                            (1 * pygame_box2d_ratio), (pillar_height * pygame_box2d_ratio)))
    pygame.draw.rect(windowSurface, GREEN, (pos_p2 * 10 - (1.5 * pygame_box2d_ratio), pygame_screen_y - (
            (pillar_height * pygame_box2d_ratio) + (ground_height * pygame_box2d_ratio)),
                                            (3 * pygame_box2d_ratio), (pillar_height * pygame_box2d_ratio)))
    for h, box in enumerate(boxeslist):
        # rotate surf by DEGREE amount degrees
        rotatedredbox = pygame.transform.rotozoom(boxcols[h % 4], math.degrees(box.angle), 1)
        rotatedredbox.set_colorkey(0)
        windowSurface.blit(rotatedredbox, (
        (box.position.x * pygame_box2d_ratio) - ((box_size / 2.0) * pygame_box2d_ratio),
        pygame_screen_y - (box.position.y * pygame_box2d_ratio) - ((box_size / 2.0) * pygame_box2d_ratio)))
    pygame.display.flip()

from collections import namedtuple
data = namedtuple("Data", ["size", "density"])
# set up the colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)


## PROGRAM
## set up pygame-box2d constants
animate = False
pillar_height=40.0
pygame_box2d_ratio=10.0
ground_height=1.0
pygame_screen_x=400
pygame_screen_y=800
pos_p2 = pygame_screen_x/10
##

#Test Variables
box_sizes = list(range(5,21))
iterations_z = [6, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190]
iterations_z = [30]*len(box_sizes)
total_result = np.zeros((len(box_sizes), max(iterations_z)+1))


#Run animation for different sizes of box
for vv, box_size in enumerate(box_sizes):
    iterations = iterations_z[vv]

    result_boxes = []
    result_density = []

    for iteration in range(iterations):
        # set up pygame
        pygame.init()

        # set up the window
        windowSurface = pygame.display.set_mode((pygame_screen_x, pygame_screen_y))
        pygame.display.set_caption('Animation')

        #setup boxes list
        boxeslist=[]

        # set up  box2d world
        world=b2World()

        # ground body
        groundBody=world.CreateStaticBody(
            position=(25,ground_height/2.0),
            shapes=b2PolygonShape(box=(pygame_screen_x/10,ground_height/2.0)),
            )

        # pillars bodies
        pillarBody=world.CreateStaticBody(
            position=(0.5,(pillar_height/2.0)+ground_height),
            shapes=b2PolygonShape(box=(0.5,pillar_height/2.0)),
            )

        pillarBody=world.CreateStaticBody(
            position=(pos_p2,(pillar_height/2.0)+ground_height),
            shapes=b2PolygonShape(box=(1.5,pillar_height/2.0)),
            )

        # Define the different boxcolors
        boxcols = []
        for col in [(255,0,0), (0,255,0), (0,0,255), (255,250,0)]:
            redbox = pygame.Surface((10, 10))
            redbox.fill(col)
            redbox = pygame.transform.scale(redbox, (int(box_size * pygame_box2d_ratio),
                                                     int(box_size * pygame_box2d_ratio)))
            boxcols.append(redbox)



        # Prepare for simulation. Typically we use a time step of 1/60 of a
        # second (60Hz) and 6 velocity/2 position iterations. This provides a
        # high quality simulation in most game scenarios.
        timeStep = 1.0 / 300
        vel_iters, pos_iters = 3, 1

        # This is our little animation loop.
        ev = pygame.event.poll()
        i = 0
        stopSig = False
        while ev.type!=pygame.QUIT and i < 9e20 and not stopSig:
            ev = pygame.event.poll()
            keys=pygame.key.get_pressed()
            # create random boxes

            #Spawn boxes
            if i % int(25*box_size) == 0:
                boxeslist.append(create_dynamic_box(random.randint(2,pygame_screen_x-2)))

            # Instruct the world to perform a single step of simulation. It is
            # generally best to keep the time step and iterations fixed.
            world.Step(timeStep, vel_iters, pos_iters)

            # Clear applied body forces. We didn't apply any forces, but you
            # should know about this function.
            world.ClearForces()

            if animate == True:
                if i % 10 == 0:
                    animation()

            if i % 100 == 0:
                stopSig = stop(boxeslist)

            i = i + 1

        #Show the last animation
        animation()

        #Calculte statistics
        density_boxes = inside(boxeslist) * box_size ** 2
        density_container = (pos_p2-0.5) * (pillar_height - ground_height)
        ratio = density_boxes / density_container + 0.0001
        print("Box Size {}, Iteration {}| Number of boxes: {}, Density: {}".format(
            box_size, iteration, inside(boxeslist), ratio))
        result_density.append(ratio)
        result_boxes.append(inside(boxeslist))
        #Save image so we can verify results later
        pygame.image.save(windowSurface, "box2dimg/{}_{}.jpeg".format(box_size, iteration))

    total_result[vv][0] = box_size
    total_result[vv][1:len(result_density)+1] = result_density


plotti(total_result)

import IPython
IPython.embed()

#np.save("box2dsimresult", total_result)

pygame.quit()
