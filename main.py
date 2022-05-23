import pymunk
import pygame
from sympy import rad

pygame.init()

display = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = 0, -1000
FPS = 50

def convert_coordinates(point):
    return point[0], 800-point[1]

class Joint():
    def __init__(self, position, radius, elasticity, friction, density):
        self.radius = radius
        self.body = pymunk.Body()
        self.body.position = position
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = elasticity
        self.shape.friction = 1
        self.shape.density = density
    
    def draw(self, display):
        x, y = convert_coordinates(self.body.position)
        pygame.draw.circle(display, (255, 0 , 0), (int(x), int(y)), self.radius)

    def addToSpace(self, space):
        space.add(self.body, self.shape)

class Limb():
    def __init__(self, joint1, joint2):
        self.joint1 = joint1
        self.joint2 = joint2
        body = pymunk.Body()
        body.position = ((self.joint1.body.position + self.joint2.body.position) / 2)
        shape = pymunk.Segment(self.body, self.joint1.body.position, self.joint2.body.position, 1)

    def draw(self, display):
        pygame.draw.line(display, (0,0,0), self.joint1.body.position, self.joint1.body.position, 10)
    
    def addToSpace(self):
        space.add(self.body, self.shape)


class Creature():
    def __init__(self):
        self.joints = []
        self.limbs = []

    def addJoint(self, position, radius, elasticity, friction, density):
        self.joints.append(Joint(position, radius, elasticity, friction, density))

    def addLimb(self):
        self.limbs.append(Limb(1,1))

    def addToSpace(self, space):
        for joint in self.joints:
            joint.addToSpace(space)
        for limb in self.limbs:
            limb.addToSpace(space)

    def draw(self, display):
        for joint in self.joints:
            joint.draw(display)
        for limb in self.limbs:
            limb.draw(display)
    


def game():
    creature = Creature()
    creature.addJoint((400,400), 5, 0, 1, 1)
    creature.addJoint((420,400), 5, 0, 1, 1)
    creature.addToSpace(space)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        display.fill((255,255,255))
        creature.draw(display)
        pygame.display.update()
        clock.tick(FPS)
        space.step(1/FPS)
    

game()
pygame.quit()
