import pymunk
import pygame
from sympy import Q
import skeleton as sk
import phys

pygame.init()

display = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = 0, -981
FPS = 120

creatures = []

def sim():
    #generate random creatures
    for i in range(10):
        creature = phys.Creature()
        points, links = sk.genSkeleton(5,100)
        for point in points:
            creature.addJoint((point[0]+200, point[1]+200), 5)
        for link in links:
            creature.addLimb(link[0],link[1])
        creature.addToSpace(space)
        creatures.append(creature)

    #construct stage
    floor = phys.Wall((0,10), (800,10), 100)
    floor.addToSpace(space)

    wallright = phys.Wall((800,0), (800,800), 100)
    wallright.addToSpace(space)

    wallleft= phys.Wall((0,0), (0,800), 100)
    wallleft.addToSpace(space)

    roof = phys.Wall((0,800), (800,800), 100)
    roof.addToSpace(space)

    #main sim loop
    while True:
        #check for exit condition
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        #draw white background
        display.fill((255,255,255))

        #draw creatures
        for creature in creatures:
            creature.draw(display)

        #draw stage
        floor.draw(display)
        wallright.draw(display)
        wallleft.draw(display)
        roof.draw(display)

        #update display, run clock stuff
        pygame.display.update()
        clock.tick(FPS)
        space.step(1/FPS)

sim()
pygame.quit()
