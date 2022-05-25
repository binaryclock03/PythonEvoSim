import jsonpickle
import pickle
import random
import copy
import csv
from math import sqrt,floor

from numpy import average

loadedPop = None

maxstrength = 200000+50000
minstrength = 200000-50000

class Population():
    def __init__(self,popName,genNum = 0):
        self.popName = popName
        self.genNum = genNum

        self.avgFitness = 0
        self.topFitness = 0

        self.creatures = []

        self.lastId = 1
    
    def addCreatures(self,amount,numPoints,scale,radius):
        print("stuff") #useless rn

    def addRandomCreatures(self,amount,scale = 100,radius = 10):
        for i in range(amount):
            self.creatures.append(CreatureCreator(random.randrange(3,8),scale,radius,self.lastId))
            self.lastId += 1
                
    def nextGenertation(self,simResults):

        for c in self.creatures:
            for cc in simResults:
                if cc[0] == c.id:
                    c.fitness = cc[1]

        fitnessList = []

        for c in simResults:
            fitnessList.append(c[1])            

        toKill = []
        toMutate = []

        simResults.sort(key=sortFunc)

    #Start of mess
        
        self.topFitness = simResults[-1][1]

        sum = 0

        simResultIds = []

        for x in simResults:
            sum += x[1]
            simResultIds.append(x[0])

        self.avgFitness = sum/len(simResults)

        originalLen = len(simResults)
        bottom = floor(len(simResults)/2)

        self.medianFitness = simResults[bottom][1]

        for c in range(bottom):
            toKill.append(simResults[c][0])
        
        for c in range(len(simResults)):
            if simResults[c][2] and simResults[c][0] not in toKill:
                toKill.append(simResults[c][0])

        for c in toKill:
            simResultIds.remove(c)

        self.killSpecified(toKill)

        top = int(len(simResults)*0.2)

        if top >= len(simResultIds):
            self.mutateSpecified(simResultIds,2)
        else:
            for c in range(top):
                toMutate.append(simResultIds[c])

            for c in toMutate:
                simResultIds.remove(c)

            self.mutateSpecified(toMutate,2)

            toMutate = []

            for c in simResultIds:
                toMutate.append(c)
        
            self.mutateSpecified(toMutate,1)

    #end of mess

        self.addRandomCreatures(originalLen-len(self.creatures))

        summary = "\nGeneration: " + str(self.genNum) + " Avg: " + str(self.avgFitness) + " Best: " + str(self.topFitness) + " Median: " + str(self.medianFitness)
        print(summary)

        if self.genNum == 0:
             f = open("Populations\\"+ self.popName + "_summary.cvs", 'w+')
             f.close()

        f = open("Populations\\"+ self.popName + "_summary.cvs", 'a')
        csv.writer(f).writerow(fitnessList)
        f.close()

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
                
                pointPosList = []
                
                coin1 = random.random()
                
                for p in c.points:
                    p.pos = (clamp(p.pos[0]+random.uniform(-1,1),0,c.scale*1.5),clamp(p.pos[1]+random.uniform(-1,1),0,c.scale*1.5))
                    
                    p.fritction = clamp(p.friction + random.uniform(-1,1),0,1)
                    
                    p.elasticity = clamp(p.elasticity + random.uniform(-1,1),0,1)

                    pointPosList.append(p.pos)
                    
                    #Check for possible point merge

                    merger = None
                    mergee = None

                    #Finds Points that are close enough, is kinda wierd so it plays nice with the link generation
                    if coin1 > 0.9:
                        for t in range(c.points.index(p)+1,(len(c.points))):
                            distance = sqrt((p.pos[0]-c.points[t].pos[0])**2+(p.pos[1]-c.points[t].pos[1])**2)
                            if distance < 15:
                                newPos = ((p.pos[0]+c.points[t].pos[0])/2,(p.pos[1]+c.points[t].pos[1])/2)
                                merger = c.points.index(p)
                                mergee = t
                                
                for l in c.links:
                
                    l.delta = clamp(l.delta + random.uniform(-0.015,0.015),0.5,2)

                    l.dutyCycle = clamp(l.dutyCycle + random.uniform(-0.008,0.008),0.1,0.9)

                    l.period = clamp(l.period + random.uniform(-0.06,0.06),10,120)

                    l.phase = clamp(l.phase + random.uniform(-0.06,0.06),10,120)

                    l.strength = clamp(l.strength + random.uniform(-(maxstrength-minstrength)/100,(maxstrength-minstrength)/100),minstrength,maxstrength)
        
                coin2 = random.random()
                coin3 = random.random()

                if coin3 < 0.05:
                    availableConnections = []
                    
                    for x in range(len(c.points)):
                            for y in range(x+1,(len(c.points))):
                                availableConnections.append((x,y))
                                
                    for connection in c.links:
                        if connection.connected in availableConnections:
                            availableConnections.remove(connection.connected)

                    if coin2 < 0.3:
                        c.links.remove(random.choice(c.links))

                    if len(availableConnections) > 0:    
                        c.links.append(Link(random.choice(availableConnections)))
                
                elif coin2 < 0.5 and coin2 > 0.4:
                    c.links.remove(random.choice(c.links))
                    

    def savePopJson(self):
        f = open("Populations\\"+ self.popName + "_Gen_" + str(self.genNum) + ".json", 'w+')
        f.writelines(jsonpickle.encode(self, indent = 2))
        f.close()
        print("Saving Json Finished")

    def savePop(self):
        f = open("Populations\\"+ self.popName + "_Gen_" + str(self.genNum) + ".pickle", 'wb')
        pickle.dump(self,f)
        f.close()
        print("Saving Finished")


    def getCreatures(self):
        return self.creatures
    
    def getBestCreature(self):
        for c in self.creatures:
            if self.topFitness == c.fitness:
                return c

    def getMedianCreature(self):
        for c in self.creatures:
            if self.medianFitness == c.fitness:
                return c
    
    def sortCreatures(self):
        self.creatures.sort(key=fitnessSortFunc)

    def getPreview(self):
        self.sortCreatures()
        sample = []

        for x in range(0,len(self.creatures),len(self.creatures)//4):
            sample.append(self.creatures[x])
        for x in range(len(self.creatures)-1,len(self.creatures)-10,-1):
            sample.append(self.creatures[x])

        return sample

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

        self.fitness = 0

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
        
    def getLinkByConnection(self,connected):
        for l in self.links:
            if l.connected == connected:
                return l
            
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
        self.period = random.uniform(10,120)
        self.phase = random.uniform(10,120)
        self.strength = random.uniform(minstrength,maxstrength)



def loadPopJson(name,gen):
    f = open("Populations\\"+ name + "_Gen_" + str(gen) + ".json", 'r')
    global loadedPop
    loadedPop = jsonpickle.decode(f.read())
    f.close()
    print("Pop: " + name + ", Gen: " + str(gen) + " loaded")
    return loadedPop

def loadPop(name,gen):
    f = open("Populations\\"+ name + "_Gen_" + str(gen) + ".pickle", 'rb')
    global loadedPop
    loadedPop = pickle.load(f)
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

def fitnessSortFunc(e):
    return e.fitness