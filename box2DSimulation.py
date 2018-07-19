from Box2D import *
import pygame, sys, math, random
from pygame.locals import *
import numpy as np

# set up pygame-box2d constants
box_size=2
pillar_height=20.0
pygame_box2d_ratio=10.0
ground_height=1.0
pygame_screen_x=600
pygame_screen_y=400
pos_p2 = pygame_screen_x/10

# set up pygame
pygame.init()

# set up the window
windowSurface = pygame.display.set_mode((pygame_screen_x, pygame_screen_y))
pygame.display.set_caption('Box2D and Pygame demo!')

#setup boxes list

boxeslist=[]

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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


def create_dynamic_box(xpos):
    body=world.CreateDynamicBody(position=(xpos/pygame_box2d_ratio,40), angle=np.random.randint(0,179))
    box=body.CreatePolygonFixture(box=(box_size/2.0,box_size/2.0), density=100, friction=1)
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
        print(isInside(box))
        if isInside(box):
            sum += 1
        else:
            pass
    print(sum)


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
    if len(boxeslist) < 40:
        return False
    else:
        for box in boxeslist[-20:]:
            if isInside(box):
                return False
    return True




# Define the different boxcolors
boxcols = []
for col in [(255,0,0), (0,255,0), (0,0,255), (255,250,0)]:
    redbox = pygame.Surface((10, 10))
    redbox.fill(col)
    redbox = pygame.transform.scale(redbox, (int(box_size * pygame_box2d_ratio), int(box_size * pygame_box2d_ratio)))
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
while ev.type!=pygame.QUIT and i < 100000 and not stopSig:
    ev = pygame.event.poll()
    keys=pygame.key.get_pressed()
    # create random boxes

    if random.randint(1,200)==2:
        boxeslist.append(create_dynamic_box(random.randint(1,pygame_screen_x)))

    # Instruct the world to perform a single step of simulation. It is
    # generally best to keep the time step and iterations fixed.
    world.Step(timeStep, vel_iters, pos_iters)

    # Clear applied body forces. We didn't apply any forces, but you
    # should know about this function.
    world.ClearForces()

    # clean screen
    windowSurface.fill(BLACK)

    # draw ground
    pygame.draw.rect(windowSurface, GREEN, (0, pygame_screen_y-(ground_height*pygame_box2d_ratio), pygame_screen_x,pygame_screen_y ))

    # draw pillars
    pygame.draw.rect(windowSurface, GREEN, (5.0-(0.5*pygame_box2d_ratio), pygame_screen_y-((pillar_height*pygame_box2d_ratio)+(ground_height*pygame_box2d_ratio)), (1*pygame_box2d_ratio),(pillar_height*pygame_box2d_ratio)))
    pygame.draw.rect(windowSurface, GREEN, (pos_p2*10-(1.5*pygame_box2d_ratio), pygame_screen_y-((pillar_height*pygame_box2d_ratio)+(ground_height*pygame_box2d_ratio)), (3*pygame_box2d_ratio),(pillar_height*pygame_box2d_ratio)))


    if i % 10 == 0:
        for h, box in enumerate(boxeslist):
            #rotate surf by DEGREE amount degrees
            rotatedredbox =  pygame.transform.rotozoom(boxcols[h % 4], math.degrees(box.angle),1)
            rotatedredbox.set_colorkey(0)
            windowSurface.blit(rotatedredbox, ((box.position.x*pygame_box2d_ratio)-((box_size/2.0)*pygame_box2d_ratio),pygame_screen_y-(box.position.y*pygame_box2d_ratio)-((box_size/2.0)*pygame_box2d_ratio)))
        pygame.display.flip()

    if i % 100 == 0:
        stopSig = stop(boxeslist)
    i = i + 1

inside(boxeslist)
input()
#import IPython
#IPython.embed()
pygame.quit()