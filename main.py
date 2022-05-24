import pymunk
import pygame
import populationManager as sk
import simObjects as phys
import camera

pygame.init()

display = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
space = pymunk.Space()
FPS = 120
graphicsHandler = camera.GraphicsHandler(space, display, FPS)
space.gravity = 0, -981

creatures = []

def only_collide_same(arbiter, space, data):
    a, b = arbiter.shapes
    return False
    #return a.pair_index == b.pair_index

def sim(simLength, simPop):
    #generate sample
    sample = phys.Sample()
    sample.genRandomSample(simPop, 5, space, graphicsHandler)
    simClock = 0
    simRunning = True

    #collision handler
    handler = space.add_collision_handler(2, 2)
    handler.begin = only_collide_same

    #construct stage
    floor = phys.Wall((-800,10), (8000,10), 100)
    floor.addToSpace(space)
    graphicsHandler.addToDraw(floor)
    
    #main sim loop
    while True:
        #event handler thing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            # if event.type == pygame.KEYDOWN:
            #     pressed = pygame.key.get_pressed()
            #     if pressed[pygame.K_1]:
            #         sample.killall(space, graphicsHandler)
            #         sample.genRandomSample(1, 6, space, graphicsHandler)
            #         simClock = 0
            #         simRunning = True
            #     if pressed[pygame.K_5]:
            #         sample.killall(space, graphicsHandler)
            #         sample.genRandomSample(5, 6, space, graphicsHandler)
            #         simClock = 0
            #         simRunning = True
            #     if pressed[pygame.K_2]:
            #         print(str(sample.findFitness()))
            #     if pressed[pygame.K_LEFT]:
            #         graphicsHandler.panCameraLeft()
            #     if pressed[pygame.K_RIGHT]:
            #         graphicsHandler.panCameraRight()

        #draw white background
        display.fill((255,255,255))

        #run graphics handler draw
        graphicsHandler.drawAll()

        #update display, run clock stuff
        pygame.display.update()
        sample.update()
        clock.tick(FPS)
        space.step(1/FPS)
        simClock += 1/FPS
        if simClock > simLength and simRunning == True:
            return str(sample.findFitness())
            simRunning = False

print(sim(10, 10))
pygame.quit()