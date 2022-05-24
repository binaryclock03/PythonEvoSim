import pymunk
import pygame
import populationManager as pm

def convert_coordinates(point):
    return point[0], 800-point[1]

class Joint():
    def __init__(self, position, radius, elasticity, friction, id):
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
        self.rotLimit = pymunk.RotaryLimitJoint(self.body, self.staticbody, 0, 0)
    
    def draw(self, display, offset):
        color = (255*self.shape.friction, 0, 0)
        x, y = convert_coordinates(self.body.position)
        pygame.draw.circle(display, color, (int(x)+offset, int(y)), self.radius)
        

    def addToSpace(self, space):
        space.add(self.body, self.shape)
        space.add(self.rotLimit)
    
    def kill(self, space):
        space.remove(self.body, self.shape)
        space.remove(self.rotLimit)
        del self
    
    def update(self):
        pass

class Limb():
    def __init__(self, joint1, joint2, lengthChangePercent, dutyCycle, peroid, phase, strength):
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
        x1, y1 = convert_coordinates(self.joint1.body.position + self.joint.anchor_a)
        x1 += offset
        x2, y2 = convert_coordinates(self.joint2.body.position + self.joint.anchor_b)
        x2 += offset
        pygame.draw.line(display, color, (x1, y1), (x2, y2), thickness)
    
    def addToSpace(self, space):
        space.add(self.joint)

    def kill(self, space):
        space.remove(self.joint)
        del self

class Creature():
    def __init__(self, id):
        self.id = id
        self.joints = []
        self.limbs = []

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
        for joint in self.joints:
            joint.update()

    def findFitness(self):
        x, y = 0,0
        num = 0
        for joint in self.joints:
            x += joint.body.position[0]
            num += 1
        return x/num     
    
class Wall():
    def __init__(self, point1, point2, thickness):
        self.point1 = point1
        self.point2 = point2
        self.thickness = thickness
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, point1, point2, thickness/2)
        self.shape.elasticity = 0
        self.shape.friction = 1
    
    def draw(self, display, offset):
        x1, y1 = convert_coordinates(self.point1)
        x1 = x1 + offset
        x2, y2 = convert_coordinates(self.point2)
        x2 = x2 + offset
        pygame.draw.line(display, (0,255,0), (x1, y1), (x2, y2), self.thickness)

    def addToSpace(self, space):
        space.add(self.body, self.shape)

class Sample():
    def __init__(self):
        self.creatures = []

    def update(self):
        for creature in self.creatures:
            creature.update()
    
    def killall(self, space):
        for creature in self.creatures:
            creature.kill(space)
        self.creatures = []

    def genRandomSample(self, numToGen, numPoints, space):
        for i in range(numToGen):
            popmanager = pm.CreatureCreator(numPoints, 100, 10)
            creature = Creature(popmanager.id)
            points = popmanager.points
            links = popmanager.links
            for point in points:
                a, b = point.pos
                creature.addJoint((a+200, b+200), 10, point.elasticity, point.friction)
            for link in links:
                a, b = link.connected
                creature.addLimb(a, b, link.delta, link.dutyCycle, link.period, link.phase, link.strength)
            creature.addToSpace(space)
            self.creatures.append(creature)

    def draw(self, display, offset):
        for creature in self.creatures:
            creature.draw(display, offset)
    
    def findFitness(self):
        list = []
        for creature in self.creatures:
            list.append((creature.id, creature.findFitness()))
        return list