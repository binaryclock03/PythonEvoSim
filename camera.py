import pygame
import pymunk
import simObjects

class GraphicsHandler():
    def __init__(self, space, display, fps):
        self.clock = 0
        self.offset = 0
        self.speed = 50
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

    def removeCreatures(self):
        thingsToDelete = []
        for index, drawable in enumerate(self.thingsToDraw):
            if isinstance(drawable, simObjects.Creature):
                thingsToDelete.append(index)
        for index in sorted(thingsToDelete, reverse=True):
            del self.thingsToDraw[index]

    def drawAll(self):
        for drawable in self.thingsToDraw:
            drawable.draw(self.display, self.offset)