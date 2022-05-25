import pygame
import pymunk
import simObjects

class GraphicsHandler():
    def __init__(self, space, display, fps):
        self.clock = 0
        self.offset = 0
        self.speed = 15
        self.fps = fps
        self.space = space
        self.display = display
        self.thingsToDraw = []
        self.mode = 0
        #0 = free cam
        #1 = locked first
    
    def panCameraRight(self):
        if self.mode == 0:
            self.offset -= self.speed
    
    def panCameraLeft(self):
        if self.mode == 0:
            self.offset += self.speed

    def lockFirst(self):
        print("toggling lock")
        if self.mode != 1:
            self.mode = 1
        else:
            self.mode = 0

    def addToDraw(self, drawable, location = "bot"):
        if location == "bot":
            self.thingsToDraw.append(drawable)
        if location == "top":
            self.thingsToDraw.insert(0, drawable)

    def removeCreatures(self):
        thingsToDelete = []
        for index, drawable in enumerate(self.thingsToDraw):
            if isinstance(drawable, simObjects.Creature):
                thingsToDelete.append(index)
        for index in sorted(thingsToDelete, reverse=True):
            del self.thingsToDraw[index]

    def drawAll(self, sample = None):
        if self.mode == 1:
            list = []
            for item in sample.findFitness():
                list.append(item[1])
            if len(list)>1:
                list.sort(reverse=True)
            list = list[0]
            self.offset = -list

        for drawable in self.thingsToDraw:
            drawable.draw(self.display, self.offset)