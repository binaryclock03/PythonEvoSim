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
    #generate pop
    population = phys.Population()

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
            if event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_1]:
                    population.killall(space)
                    population.genRandomPop(1, 5, space)
                if pressed[pygame.K_5]:
                    population.killall(space)
                    population.genRandomPop(5, 5, space)

        
        #draw white background
        display.fill((255,255,255))

        #draw creatures
        population.draw(display)

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
