import pymunk
import pygame
import skeleton as sk

def convert_coordinates(point):
    return point[0], 800-point[1]

class Joint():
    def __init__(self, position, radius):
        self.radius = radius
        self.body = pymunk.Body()
        self.body.position = position
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = 0.5
        self.shape.friction = 0
        self.shape.density = 1
    
    def draw(self, display):
        x, y = convert_coordinates(self.body.position)
        pygame.draw.circle(display, (255, 0 , 0), (int(x), int(y)), self.radius)

    def addToSpace(self, space):
        space.add(self.body, self.shape)
    
    def kill(self, space):
        space.remove(self.body, self.shape)
        del self

class Limb():
    def __init__(self, joint1, joint2):
        self.joint1 = joint1
        self.joint2 = joint2
        self.joint = pymunk.PinJoint(self.joint1.body, self.joint2.body) 

    def draw(self, display):
        pygame.draw.line(display, (0,0,0), convert_coordinates(self.joint1.body.position + self.joint.anchor_a), convert_coordinates(self.joint2.body.position + self.joint.anchor_b), 2)
    
    def addToSpace(self, space):
        space.add(self.joint)

    def kill(self, space):
        space.remove(self.joint)
        del self

class Creature():
    def __init__(self):
        self.joints = []
        self.limbs = []

    def addJoint(self, position, radius):
        self.joints.append(Joint(position, radius))

    def addLimb(self, jointindex1, jointindex2):
        self.limbs.append(Limb(self.joints[jointindex1],self.joints[jointindex2]))

    def addToSpace(self, space):
        for joint in self.joints:
            joint.addToSpace(space)
        for limb in self.limbs:
            limb.addToSpace(space)

    def draw(self, display):
        for limb in self.limbs:
            limb.draw(display)
        for joint in self.joints:
            joint.draw(display)
    
    def kill(self, space):
        for limb in self.limbs:
            limb.kill(space)
        for joint in self.joints:
            joint.kill(space)
        del self
    
class Wall():
    def __init__(self, point1, point2, thickness):
        self.point1 = point1
        self.point2 = point2
        self.thickness = thickness
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, point1, point2, thickness/2)
        self.shape.elasticity = 1
        self.shape.friction = 1
    
    def draw(self, display):
        pygame.draw.line(display, (0,255,0), convert_coordinates(self.point1), convert_coordinates(self.point2), self.thickness)

    def addToSpace(self, space):
        space.add(self.body, self.shape)

class Population():
    def __init__(self):
        self.creatures = []
    
    def killall(self, space):
        for creature in self.creatures:
            creature.kill(space)
        self.creatures = []

    def genRandomPop(self, numToGen, points, space):
        for i in range(numToGen):
            creature = Creature()
            points, links = sk.genSkeleton(5,100,5)
            for point in points:
                creature.addJoint((point[0]+200, point[1]+200), 5)
            for link in links:
                creature.addLimb(link[0],link[1])
            creature.addToSpace(space)
            self.creatures.append(creature)

    def draw(self, display):
        for creature in self.creatures:
            creature.draw(display)
