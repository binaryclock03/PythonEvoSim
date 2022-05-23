import pymunk
import pygame

pygame.init()

display = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = 0, -1000
FPS = 50

def convert_coordinates(point):
    return point[0], 800-point[1]

body = pymunk.Body()
body.position = (400, 400)
shape = pymunk.Circle(body, 10)
shape.density = 1
shape.elasticity = 1.1
space.add(body, shape)

segment_body = pymunk.Body(body_type=pymunk.Body.STATIC)
segment_shape = pymunk.Segment(segment_body, (0,50), (800,100), 5)
segment_shape.elasticity = 1
space.add(segment_body, segment_shape)



def game():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        display.fill((255,255,255))
        x, y = convert_coordinates(body.position)
        pygame.draw.circle(display, (255, 0 , 0), (int(x), int(y)), 10)
        pygame.draw.line(display, (0,0,0), convert_coordinates((0,50)), convert_coordinates((800,100)), 10)

        pygame.display.update()
        clock.tick(FPS)
        space.step(1/FPS)
    

game()
pygame.quit()
