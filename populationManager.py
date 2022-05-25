from operator import pos
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

    def linkMutation(self,creature):
        coin = random.random()

        availableConnections = []
            
        #Find all possible connections
        for x in range(len(creature.points)):
                for y in range(x+1,(len(creature.points))):
                    availableConnections.append((x,y))

        #Find empty connections           
        for connection in creature.links:
            if connection.connected in availableConnections:
                availableConnections.remove(connection.connected)
        

        if coin > 0.5 and len(availableConnections) > 0:
            #Replace Link
            #print('Replaced Link')
            creature.links.remove(random.choice(creature.links))
            creature.links.append(Link(random.choice(availableConnections)))
        elif coin > 0.25 and len(availableConnections) > 0:
            #Make new Link
            #print('Added New Link')
            creature.links.append(Link(random.choice(availableConnections)))
        elif coin < 0.25:
            #Remove Random Link
            #print('Removed Link')
            creature.links.remove(random.choice(creature.links))

    def pointMutation(self,creature):

        possibleMergingPairs = []
        
        merger = None
        mergee = None

        for p in creature.points:
                    #Finds the distance of other points to the current point 'p' and valid merging pairs.
            for t in creature.points:
                if p != t:
                    distance = sqrt((p.pos[0]-t.pos[0])**2 + (p.pos[1]-t.pos[1])**2)
                    if distance < creature.scale/10:
                        possibleMergingPairs.append(((p,t)))
                        if not (set(creature.getConnectedPoints(t)).issubset(set(creature.getConnectedPoints(p))) or set(creature.getConnectedPoints(p)).issubset(set(creature.getConnectedPoints(t)))):
                            possibleMergingPairs.remove((p,t))
                    
        #Pick random valid merging pair
        if len(possibleMergingPairs) > 0:
            
            mergingPair = random.choice(possibleMergingPairs)
            #Determine merger and mergee
            if set(creature.getConnectedPoints(mergingPair[1])).issubset(set(creature.getConnectedPoints(mergingPair[0]))):
                merger = mergingPair[0]
                mergee = mergingPair[1]
            elif set(creature.getConnectedPoints(mergingPair[0])).issubset(set(creature.getConnectedPoints(mergingPair[1]))):
                merger = mergingPair[1]
                mergee = mergingPair[0]
        
            #Average the properties of both points and give it to merger
            merger.pos = ((merger.pos[0]+mergee.pos[0])/2,(merger.pos[1]+mergee.pos[1])/2) 
            merger.friction = (merger.friction + mergee.friction)/2
            merger.elasticity = (merger.elasticity + mergee.elasticity)/2

            #Averge the properties of links that will be merged into its counter part connected to merger
            commonPoints = list(set(creature.getConnectedPoints(merger)).intersection(set(creature.getConnectedPoints(mergee))))
            mergerLinks = creature.getLinksOfPoint(merger)
            mergeeLinks = creature.getLinksOfPoint(mergee)
            mergeeIndex = creature.points.index(mergee)

            # for l in range(len(mergeeLinks)):
            #     mergerLinks[l].delta = (mergerLinks[l].delta + mergeeLinks[l].delta)/2
            #     mergerLinks[l].dutyCycle = (mergerLinks[l].dutyCycle + mergeeLinks[l].dutyCycle)/2
            #     mergerLinks[l].period = (mergerLinks[l].period + mergeeLinks[l].period)/2
            #     mergerLinks[l].phase = (mergerLinks[l].phase + mergeeLinks[l].phase)/2
            #     mergerLinks[l].strength = (mergerLinks[l].strength + mergeeLinks[l].strength)/2

            #Remove mergee and its links
            creature.points.remove(mergee)
            for l in mergeeLinks:
                creature.links.remove(l)
            
            #Rebuild Creature
            for l in creature.links:
                if l.connected[0] > mergeeIndex:
                    l.connected = (l.connected[0] - 1,l.connected[1])                  
                if l.connected[1] > mergeeIndex:
                    l.connected = (l.connected[0],l.connected[1]- 1)

        elif random.random() > 0.5:
            #Add New Point
            pass
        else:
            #Remove Random Point
            pass
                
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

    #Start of mess

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

        #Preform Basic Mutations
        for c in self.creatures:
            if c.id in toMutate:
                c.id = self.lastId
                self.lastId += 1
                                
                for p in c.points:
                    p.pos = (clamp(p.pos[0]+random.uniform(-1,1),0,c.scale*1.5),clamp(p.pos[1]+random.uniform(-1,1),0,c.scale*1.5))
                    
                    p.fritction = clamp(p.friction + random.uniform(-1,1),0,1)
                    
                    p.elasticity = clamp(p.elasticity + random.uniform(-1,1),0,1)

                for l in c.links:
                
                    l.delta = clamp(l.delta + random.uniform(-0.015,0.015),0.5,2)

                    l.dutyCycle = clamp(l.dutyCycle + random.uniform(-0.008,0.008),0.1,0.9)

                    l.period = clamp(l.period + random.uniform(-0.06,0.06),10,120)

                    l.phase = clamp(l.phase + random.uniform(-0.06,0.06),10,120)

                    l.strength = clamp(l.strength + random.uniform(-(maxstrength-minstrength)/100,(maxstrength-minstrength)/100),minstrength,maxstrength)

                if random.random() < 0.05:
                    if random.random() < 0.5:
                        self.pointMutation(c)
                    else:
                        self.linkMutation(c)

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
    def getLinksOfPoint(self,point):
        connectedLinks = []
        for l in self.links:
            if self.points.index(point) in l.connected:
                connectedLinks.append(l)
        return connectedLinks
    
    def getConnectedPoints(self,point):
        connectedPoints = []
        for l in self.links:
            if self.points.index(point) in l.connected:
                if self.points.index(point) == l.connected[0]:
                    connectedPoints.append(l.connected[1])
                else:
                    connectedPoints.append(l.connected[0])
        return connectedPoints

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