import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import time
import pymunk
import pygame
import populationManager as pm
import camera
import multiprocessing as mp

def convert_coordinates(point, offset = 0):
    return int(point[0]+offset), int(800-point[1])

class Drawable():
    def __init__(self):
        pass
    
    def draw(self, display, offset):
        pass

class DrawableImage(Drawable):
    def __init__(self, image, position):
        self.position = position
        self.image = image

    def draw(self, display, offset):
        coords = convert_coordinates(self.position, offset)
        display.blit(self.image, (coords))

class SimObject(Drawable):
    def __init__(self):
        super().__init__()

    def update(self):
        pass

    def addToSpace(self, space):
        pass

    def kill(self, space):
        del self

class PhysicsObject(SimObject):
    def __init__(self):
        super().__init__()
        self.body = None
        self.shape = None
        self.joint = None

    def addToSpace(self, space):
        if (self.body != None) and (self.shape != None):
            space.add(self.body, self.shape)
        elif (self.body != None):
            space.add(self.body)
        if (self.joint != None):
            space.add(self.joint)
            

    def kill(self, space):
        if (self.body != None) and not (self.shape != None):
            space.remove(self.body, self.shape)
        elif (self.body != None):
            space.remove(self.body)
        if (self.joint != None):
            space.remove(self.joint)
        del self

class Joint(PhysicsObject):
    def __init__(self, position, radius, elasticity, friction, id):
        super().__init__()
        self.radius = radius
        self.body = pymunk.Body()
        self.body.position = position
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = elasticity
        self.shape.friction = friction
        self.shape.density = 1
        self.shape.collision_type = 2
        self.shape.pair_index = id
        self.staticbody = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.staticbody.position = position
        self.joint = pymunk.RotaryLimitJoint(self.body, self.staticbody, 0, 0)
    
    def draw(self, display, offset):
        color = (255*self.shape.friction, 0, 0)
        coord = convert_coordinates(self.body.position, offset)
        pygame.draw.circle(display, color, coord, self.radius)

class Limb(PhysicsObject):
    def __init__(self, joint1, joint2, lengthChangePercent, dutyCycle, peroid, phase, strength):
        super().__init__()
        self.clock = 0
        self.state = False
        self.lengthChangePercent = lengthChangePercent
        self.dutyCycle = dutyCycle
        self.peroid = peroid
        self.phase = phase
        self.strength = strength
        self.joint1 = joint1
        self.joint2 = joint2
        self.regularLen = abs(self.joint2.body.position-self.joint1.body.position)
        self.joint = pymunk.DampedSpring(self.joint1.body, self.joint2.body, (0,0), (0,0), self.regularLen, self.strength, 5000) 

    def setLength(self, length):
        self.joint.rest_length = length

    def update(self):
        self.clock += 1
        if (self.clock + self.phase)%self.peroid > self.peroid * self.dutyCycle:
            self.state = False
            self.setLength(self.regularLen)
        else:
            self.state = True
            self.setLength(self.regularLen * self.lengthChangePercent)

    def draw(self, display, offset):
        if self.state:
            color = (0,0,255)
        else:
            color = (0,0,0)
        thickness = int(3+8*((self.strength-pm.minstrength)/(pm.maxstrength-pm.minstrength)))
        coord = convert_coordinates(self.joint1.body.position, offset)
        coord2 = convert_coordinates(self.joint2.body.position, offset)
        pygame.draw.line(display, color, coord, coord2, thickness)

class Creature(SimObject):
    def __init__(self, popmanager):
        super().__init__()
        self.id = popmanager.id
        self.joints = []
        self.limbs = []
        points = popmanager.points
        links = popmanager.links
        for point in points:
            a, b = point.pos
            self.addJoint((a+200, b+200), 10, point.elasticity, point.friction)
        for link in links:
            a, b = link.connected
            self.addLimb(a, b, link.delta, link.dutyCycle, link.period, link.phase, link.strength)

    def addJoint(self, position, radius, elasticity, friciton):
        self.joints.append(Joint(position, radius, elasticity, friciton, self.id))

    def addLimb(self, jointindex1, jointindex2, lengthChangePercent, dutyCycle, peroid, phase, strength):
        self.limbs.append(Limb(self.joints[jointindex1],self.joints[jointindex2], lengthChangePercent, dutyCycle, peroid, phase, strength))

    def addToSpace(self, space):
        for joint in self.joints:
            joint.addToSpace(space)
        for limb in self.limbs:
            limb.addToSpace(space)

    def draw(self, display, offset):
        for limb in self.limbs:
            limb.draw(display, offset)
        for joint in self.joints:
            joint.draw(display, offset)
    
    def kill(self, space):
        for limb in self.limbs:
            limb.kill(space)
        for joint in self.joints:
            joint.kill(space)
        del self
    
    def update(self):
        for limb in self.limbs:
            limb.update()

    def findFitness(self):
        x, y = 0,0
        num = 0
        for joint in self.joints:
            xtemp, ytemp = joint.body.position
            x += (xtemp-200)
            y += (ytemp-70)
            num += 1
        return self.id, x/num, y<5

class BackgroundWall(Drawable):
    def __init__(self, point1, point2, thickness, color = (0,100,0)):
        super().__init__()
        self.color = color
        self.point1 = point1
        self.point2 = point2
        self.thickness = thickness
    
    def draw(self, display, offset):
        coord = convert_coordinates(self.point1, offset)
        coord2 = convert_coordinates(self.point2, offset)
        pygame.draw.line(display, self.color, coord, coord2, self.thickness)

class Wall(BackgroundWall, PhysicsObject):
    def __init__(self, point1, point2, thickness, color = (0,255,0)):
        super().__init__(point1, point2, thickness, color)
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, point1, point2, thickness/2)
        self.shape.elasticity = 0
        self.shape.friction = 1

class Sample():
    def __init__(self):
        self.creatures = []

    def update(self):
        for creature in self.creatures:
            creature.update()
    
    def killall(self, space, graphicsHandler = None):
        if graphicsHandler != None:
            graphicsHandler.removeCreatures()
        for creature in self.creatures:
            creature.kill(space)
        self.creatures = []
    
    def addCreature(self, popmanager, space, graphicsHandler):
        creature = Creature(popmanager)
        self.creatures.append(creature)
        creature.addToSpace(space)
        graphicsHandler.addToDraw(creature)

    def findFitness(self):
        list = []
        for creature in self.creatures:
            list.append(creature.findFitness())
        return list

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
    for i in range(10):
        background = DrawableImage(image, (i*1600-1600, 800))
        graphicsHandler.addToDraw(background)
    for i in range(50):
        post = BackgroundWall((i*250,0), (i*250,100), 5, color= (100,100,100))
        graphicsHandler.addToDraw(post)

    floor = Wall((-800,10), (80000,10), 100)
    floor.addToSpace(space)
    graphicsHandler.addToDraw(floor)

    #generate sample
    sample = Sample()
    for creature in creatureList:
        sample.addCreature(creature, space, graphicsHandler)

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
                return
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
        graphicsHandler.drawAll(sample)

        #update display, run clock stuff
        pygame.display.update()
        clock.tick(FPS)
        sample.update()
        space.step(1/FPS)
        simClock += 1
        if simClock >= simLength*FPS and simRunning == True:
            pygame.quit()
            simRunning = False
            return

def fastsimHelper(batch):
    simLength, popmanager, TPS = batch
    space = pymunk.Space()
    space.gravity = 0, -981

    #construct stage
    floor = Wall((-800,10), (8000,10), 100)
    floor.addToSpace(space)

    #define sim clock and set sim to true
    creature = Creature(popmanager)
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