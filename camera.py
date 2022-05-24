from matplotlib.pyplot import draw
import pygame
import pymunk

class GraphicsHandler():
    def __init__(self, space, display, fps):
        self.clock = 0
        self.offset = 0
        self.speed = 100
        self.fps = fps
        self.space = space
        self.display = display
        self.thingsToDraw = []
    
    def panCameraRight(self):
        self.offset -= self.speed
    
    def panCameraLeft(self):
        self.offset += self.speed

    def addToDraw(self, drawable):
        self.thingsToDraw.append(drawable)

    def removeCreatures():
        pass

    def drawAll(self):
        #print(str(len(self.thingsToDraw)))
        for drawable in self.thingsToDraw:
            drawable.draw(self.display, self.offset)