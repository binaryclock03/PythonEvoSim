import os
from matplotlib.pyplot import draw
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import pymunk
import camera
import multiprocessing as mp
import simObjects as so

def only_collide_same(arbiter, space, data):
    a, b = arbiter.shapes
    return False
    #return a.pair_index == b.pair_index

def playback(simLength, creatureList, FPS = 60):
    #initial setup stuff
    pygame.init()
    clock = pygame.time.Clock()
    space = pymunk.Space()
    display = pygame.display.set_mode((800,800))
    pygame.display.set_caption("Python Evolution Simulator")
    graphicsHandler = camera.GraphicsHandler(space, display, FPS)
    space.gravity = 0, -981

    #construct stage
    image = pygame.image.load("Graphics\\Background1.png")
    for i in range(20):
        background = so.DrawableImage(image, (i*1600-1600, 800))
        graphicsHandler.addToDraw(background, layer = "bg")
    # for i in range(100):
    #     x = ((i-5)*250)+200
    #     post = so.BackgroundWall((x,0), (x,100), 5, color= (100,100,100))
    #     graphicsHandler.addToDraw(post, layer = "bg")
    #     number = so.DrawableText(str((i-5)*250), (x,115))
    #     graphicsHandler.addToDraw(number, layer="bg")

    floor = so.Wall((-800,0), (80000,0), 100)
    floor.addToSpace(space)

    #generate sample
    sample = so.Sample(showStats = True)
    for creature in creatureList:
        sample.addCreature(creature, space, graphicsHandler)

    graphicsHandler.addToDraw(floor, layer="fg")

    #make hud
    secondsCounter = so.DrawableDynText((50,750), "clock")
    graphicsHandler.addToDraw(secondsCounter, layer="hd")
    graphicsHandler.addToDynamics(secondsCounter)

    #define sim clock and set sim to true
    simClock = 0
    simRunning = True

    #collision handler
    handler = space.add_collision_handler(2, 2)
    handler.begin = only_collide_same

    #main sim loop
    while True:
        #event handler thing
        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                keydown = pygame.key.get_pressed()
                if keydown[pygame.K_l]:
                    graphicsHandler.lockFirst()
        if pressed[pygame.K_LEFT]:
            graphicsHandler.panCameraLeft()
        if pressed[pygame.K_RIGHT]:
            graphicsHandler.panCameraRight()

        #draw white background
        display.fill((255,255,255))

        #run graphics handler draw
        graphicsHandler.update(clock = str(round(simClock/FPS,2)))
        graphicsHandler.drawAll(sample)
        
        #update display, run clock stuff
        pygame.display.update()
        clock.tick(FPS)
        sample.update()
        space.step(1/FPS)
        simClock += 1
        if simLength != 0 and simClock >= simLength*FPS and simRunning == True:
            pygame.quit()
            simRunning = False
            return False

def showCreatures(simLength, creatureList, FPS = 60):
    #initial setup stuff
    pygame.init()
    clock = pygame.time.Clock()
    space = pymunk.Space()
    display = pygame.display.set_mode((800,800))
    pygame.display.set_caption("Python Evolution Simulator")
    graphicsHandler = camera.GraphicsHandler(space, display, FPS)
    space.gravity = 0, 0

    #generate sample
    sample = so.Sample()
    scale = 0.4
    buffer = 150 * scale
    numPerRow = 10
    for i, creature in enumerate(creatureList):
        x =      ((800-(buffer))/numPerRow)*(i%numPerRow) + buffer
        y = 800-(((800-(buffer))/numPerRow)*(i//numPerRow) + buffer)
        sample.addCreature(creature, space, graphicsHandler, pos = (x, y), scale = scale)

    #define sim clock and set sim to true
    simClock = 0
    simRunning = True

    #collision handler
    handler = space.add_collision_handler(2, 2)
    handler.begin = only_collide_same

    #main sim loop
    while True:
        #event handler thing
        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        #draw white background
        display.fill((50,100,50))

        #run graphics handler draw
        graphicsHandler.drawAll(sample)

        #update display, run clock stuff
        pygame.display.update()
        clock.tick(FPS)
        #sample.update()
        space.step(1/FPS)
        simClock += 1
        if simLength != 0 and simClock >= simLength*FPS and simRunning == True:
            pygame.quit()
            simRunning = False
            return False

def fastsimHelper(batch):
    simLength, popmanager, TPS = batch
    space = pymunk.Space()
    space.gravity = 0, -981

    #construct stage
    floor = so.Wall((-800,10), (80000,10), 100)
    floor.addToSpace(space)

    #define sim clock and set sim to true
    creature = so.Creature(popmanager)
    creature.addToSpace(space)
    simClock = 0
    while True:    
        creature.update()
        space.step(1/TPS)
        simClock += 1
        if simClock >= simLength*TPS:
            return creature.findFitness()

def fastsim(simLength, creatureList, TPS = 60):
    fitnessList = []
    data = []
    for creature in creatureList:
        data.append([simLength, creature, TPS])
    with mp.Pool(mp.cpu_count()) as p:    
        fitnessbatch = p.map(fastsimHelper, data)
        fitnessList = fitnessList + fitnessbatch
    return fitnessList