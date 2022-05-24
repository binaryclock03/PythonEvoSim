import jsonpickle
import random
import copy
from math import sqrt,floor

loadedPop = None

maxstrength = 200000+50000
minstrength = 200000-50000

class Population():
    def __init__(self,popName,genNum = 0):
        self.popName = popName
        self.genNum = genNum

        self.creatures = []

        self.lastId = 1
    
    def clearCreatures(self):
        for c in self.creatures:
            del c
    
    def addCreatures(self,amount,numPoints,scale,radius):
        print("stuff")

    def addRandomCreatures(self,amount,scale = 100,radius = 10):
        for i in range(amount):
            self.creatures.append(CreatureCreator(random.randrange(3,8),scale,radius,self.lastId))
            self.lastId += 1
                
    def nextGenertation(self,simResults):

        toKill = []
        toMutate = []

        (simResults.sort(key=sortFunc))

        originalLen = len(simResults)
        bottom = floor(len(simResults)/2)

        for c in range(bottom):
            toKill.append(simResults[c][0])
            simResults.pop(c)

 
        self.killSpecified(toKill)


        top = int(len(simResults)*0.2)

        for c in range(top):
            toMutate.append(simResults[c][0])
            simResults.pop(c)

        self.mutateSpecified(toMutate,2)

        toMutate = []

        for c in simResults:
            toMutate.append(c[0])
        
        self.mutateSpecified(toMutate,1)

        self.addRandomCreatures(originalLen-len(self.creatures))

        self.genNum += 1

    def killSpecified(self,toKill):
        fuck = []
        for i,c in enumerate(self.creatures):
            if c.id in toKill:
                fuck.append(i)
        for i in sorted(fuck,reverse=True):
            del self.creatures[i]
        

    def mutateSpecified(self,toMutate,offspringPer):
        #Create Copies if needed
        tempCreatures = []
        tempToMutate = []
        for c in self.creatures:
            if c.id in toMutate:
                if offspringPer > 1:
                    #for cc in range(offspringPer-1):
                    cpy = copy.deepcopy(c)
                    cpy.id = self.lastId
                    tempToMutate.append(self.lastId)
                    tempCreatures.append(cpy)
                    self.lastId += 1
                        
        self.creatures.extend(tempCreatures)
        toMutate.extend(tempToMutate)

        #Preform Mutations
        for c in self.creatures:
            if c.id in toMutate:
                c.id = self.lastId
                self.lastId += 1
                for p in c.points:
                    p.pos = (p.pos[0]+random.uniform(-1,1),p.pos[1]+random.uniform(-1,1))
                    
                    p.fritction = clamp(p.friction + random.uniform(-1,1),0,1)
                    
                    p.elasticity = clamp(p.elasticity + random.uniform(-1,1),0,1)
                    
                for l in c.links:
                    l.delta = clamp(l.delta + random.uniform(-0.015,0.015),0.5,2)

                    l.dutyCycle = clamp(l.dutyCycle + random.uniform(-0.008,0.008),0.1,0.9)

                    l.period = clamp(l.period + random.uniform(-1.2,1.2),120,1200)

                    l.phase = clamp(l.phase + random.uniform(-1.2,1.2),120,1200)

                    l.strength = clamp(l.strength + random.uniform(-(maxstrength-minstrength)/100,(maxstrength-minstrength)/100),minstrength,maxstrength)
        
    def savePop(self):
        f = open("Populations\\" + self.popName + "_Gen_" + str(self.genNum) + ".json", 'w+')
        f.writelines(jsonpickle.encode(self, indent = 2))
        f.close()
        print("Saving Finished")
    
    def getCreatures(self):
        return self.creatures
    
class CreatureCreator():
    def __init__(self,numPoints,scale,radius,id = 0):
        if numPoints < 3:
            self.numPoints = random.randrange(3,10)
        else:
            self.numPoints = numPoints

        self.scale = scale
        self.radius = radius 
        if id == 0:
            self.id = int(random.random() * 10 ** 16)
        else:
            self.id = int(id)
        
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
        self.strength = random.uniform(minstrength,maxstrength)

def loadPop(name,gen):
    f = open("Populations\\" + name + "_Gen_" + str(gen) + ".json", 'r')
    global loadedPop
    loadedPop = jsonpickle.decode(f.read())
    f.close()
    print("Pop: " + name + ", Gen: " + str(gen) + " loaded")
    return loadedPop

def initNewPop(name):
    loadedPop = Population(name)

def clamp(num, min_value, max_value):
        num = max(min(num, max_value), min_value)
        return num

def sortFunc(e):
    return e[1]