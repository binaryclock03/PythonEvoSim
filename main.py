import pymunk
import pygame
import skeleton as sk

pygame.init()

display = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = 0, -1000
FPS = 120

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

class Limb():
    def __init__(self, joint1, joint2):
        self.joint1 = joint1
        self.joint2 = joint2
        self.joint = pymunk.PinJoint(self.joint1.body, self.joint2.body) 

    def draw(self, display):
        pygame.draw.line(display, (0,0,0), convert_coordinates(self.joint1.body.position + self.joint.anchor_a), convert_coordinates(self.joint2.body.position + self.joint.anchor_b), 2)
    
    def addToSpace(self, space):
        space.add(self.joint)
        pass

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

creatures = []

def game():
    for i in range(10):
        creature = Creature()
        points, links = sk.genSkeleton(5,100)
        for point in points:
            creature.addJoint((point[0]+200, point[1]+200), 5)
        for link in links:
            creature.addLimb(link[0],link[1])
        creature.addToSpace(space)
        creatures.append(creature)

    floor = Wall((0,10), (800,10), 100)
    floor.addToSpace(space)

    wallright = Wall((800,0), (800,800), 100)
    wallright.addToSpace(space)

    wallleft= Wall((0,0), (0,800), 100)
    wallleft.addToSpace(space)

    roof = Wall((0,800), (800,800), 100)
    roof.addToSpace(space)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        display.fill((255,255,255))

        for creature in creatures:
            creature.draw(display)

        floor.draw(display)
        wallright.draw(display)
        wallleft.draw(display)
        roof.draw(display)

        pygame.display.update()
        clock.tick(FPS)
        space.step(1/FPS)
    

game()
pygame.quit()
