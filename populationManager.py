import jsonpickle
import random
from math import sqrt

loadedPop = None

class Population():
    def __init__(self,popName,genNum = 0):
        self.popName = popName
        self.genNum = genNum

        self.creatures = []

        self.lastId = 0
    
    def clearCreatures(self):
        for c in self.creatures:
            del c
    
    def addCreatures(self,amount,numPoints,scale,radius):
        print("stuff")

    def addRandomCreatures(self,amount,scale = 100,radius = 10):
        for i in range(amount):
            self.creatures.append(Creature(random.randrange(3,10),scale,radius,self.lastId))
            self.lastId += 1
                
    def mutateAll(self):
        print("more stuff")

    def breedBest(self):
        print("even more stuff")

    def savePop(self):
        f = open("Populations\\" + self.popName + "_Gen_ " + str(self.genNum) + ".json", 'w+')
        #f = open("test.json","a")
        thing = str(jsonpickle.encode(self, indent = 2))
        f.writelines(thing)
        f.close()
        print("Saving Finished")
    
class Creature():
    def __init__(self,numPoints,scale,radius,id):
        if numPoints < 3:
            self.numPoints = random.randrange(3,10)
        else:
            self.numPoints = numPoints

        self.scale = scale
        self.radius = radius 
        if id == 0:
            self.id = random.random() * 10 ** 12
        else:
            self.id = id
        
        self.points = []
        self.links = []
        tempLinks = []

        #Create List of Points
        for x in range(numPoints):
            invalid = True
            i = 0
            while invalid:
                pos = (random.random()*scale,random.random()*scale)
                if len(self.points) > 0:
                    for y in self.points:
                        invalid = False
                        if sqrt(((y.pos[0] - pos[0])**2 + (y.pos[1] - pos[1])**2)) < radius:
                            invalid = True
                else:
                    invalid = False
                i += 1
                if i > 1000:
                    quit("Point Generation Failed")
            self.points.append(Point(pos))
        
        #Generate All Possible Links
        for x in range(numPoints):
            for y in range(x+1,(numPoints)):
                tempLinks.append((x,y))
        
        #Simplification
        for x in range(numPoints-3):
            tempLinks.pop(random.randrange(0,len(tempLinks)))
        
        for x in tempLinks:
            self.links.append(Link(x))
            
class Point():
    def __init__(self,pos):
        self.pos = pos
        self.friction = random.random()
        self.elasticity = random.random()

class Link():
    def __init__(self,connected):
        self.connected = connected
        self.delta = random.uniform(0.5,2)
        self.dutyCycle = random.uniform(0.1,0.9)
        self.period = random.uniform(120,1200)
        self.phase = random.uniform(120,1200)
        self.strength = random.uniform(1,10)

def loadPop(name,gen):
    f = open("Populations\\" + name + "_Gen_ " + str(gen) + ".json", 'r')
    global loadedPop
    loadedPop = jsonpickle.decode(f.read())
    f.close()