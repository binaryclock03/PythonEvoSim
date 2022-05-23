import pymunk
import pygame
import skeleton as sk
import phys

pygame.init()

display = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = 0, -981
FPS = 120

creatures = []

def only_collide_same(arbiter, space, data):
    a, b = arbiter.shapes
    return False
    #return a.pair_index == b.pair_index

def sim():
    #generate pop
    sample = phys.Sample()

    #collision handler
    handler = space.add_collision_handler(2, 2)
    handler.begin = only_collide_same

    #construct stage
    floor = phys.Wall((0,10), (800,10), 100)
    floor.addToSpace(space)

    wallright = phys.Wall((800,0), (800,800), 100)
    wallright.addToSpace(space)

    wallleft = phys.Wall((0,0), (0,800), 100)
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
                    sample.killall(space)
                    sample.genRandomSample(1, 5, space)
                if pressed[pygame.K_5]:
                    sample.killall(space)
                    sample.genRandomSample(5, 5, space)
                if pressed[pygame.K_2]:
                    print(str(sample.findFitness()))

        
        #draw white background
        display.fill((255,255,255))

        #draw creatures
        sample.draw(display)

        #draw stage
        floor.draw(display)
        wallright.draw(display)
        wallleft.draw(display)
        roof.draw(display)

        #update display, run clock stuff
        pygame.display.update()
        sample.update()
        clock.tick(FPS)
        space.step(1/FPS)

sim()
pygame.quit()
