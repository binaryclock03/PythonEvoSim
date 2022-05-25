import simObjects
class GraphicsHandler():
    def __init__(self, space, display, fps):
        self.clock = 0
        self.offset = 0
        self.speed = 15
        self.fps = fps
        self.space = space
        self.display = display
        self.mode = 1
        #0 = free cam
        #1 = locked first

        self.dynamics = []

        self.background = []
        self.foreground = []
        self.hud = []
    
    def panCameraRight(self):
        if self.mode == 0:
            self.offset -= self.speed
    
    def panCameraLeft(self):
        if self.mode == 0:
            self.offset += self.speed

    def lockFirst(self):
        if self.mode != 1:
            self.mode = 1
        else:
            self.mode = 0

    def addToDraw(self, drawable, location = "bot", layer = "fg"):
        dict = {"fg": self.foreground, "bg": self.background, "hd": self.hud}
        if location == "bot":
            dict[layer].append(drawable)
        if location == "top":
            dict[layer].insert(0, drawable)

    def addToDynamics(self, drawableDynamic):
        self.dynamics.append(drawableDynamic)

    def clearLayerOfCreatures(self, layer):
        dict = {"fg": self.foreground, "bg": self.background, "hd": self.hud}
        thingsToDelete = []
        for index, drawable in enumerate(dict[layer]):
            if isinstance(drawable, simObjects.Creature):
                thingsToDelete.append(index)
        for index in sorted(thingsToDelete, reverse=True):
            del dict[layer][index]

    def drawAll(self, sample = None):
        #camera scrolling calculations
        if self.mode == 1:
            list = []
            for item in sample.findFitness():
                list.append(item[1])
            if len(list)>1:
                list.sort(reverse=True)
            list = list[0]
            self.offset = -list+200

        #draw layers
        for drawable in self.background:
            drawable.draw(self.display, self.offset)
        for drawable in self.foreground:
            drawable.draw(self.display, self.offset)
        for drawable in self.hud:
            drawable.draw(self.display, 0)
    
    def update(self, **kwargs):
        for drawableDynamic in self.dynamics:
            drawableDynamic.update(kwargs)