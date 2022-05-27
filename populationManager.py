import jsonpickle
import pickle
import random
import copy
import csv
from math import sqrt,floor
import configs
from typing import *
import os


loadedPop = None

Population = NewType("Population",object)
CreatureCreator = NewType("CreatureCreator",object)
Point = NewType("Point",object)
Link = NewType("Link",object)
PointList = NewType("PointList",list)
LinkList = NewType("LinkList",list)
CreatureCreatorList = NewType("CreatureCreatorList",list)
CreatureIdList = NewType("CreatureIdList",list)

def initNewPop(name:str = None) -> Population:
    if not name:
        name = ''
        for x in range(4):
            name += chr(random.randint(0,255))
    return Population(name) 
 
def loadPopJson(name:str,gen:int) -> Population:
    f = open("Populations\\"+ name + "_Gen_" + str(gen) + ".json", 'r')
    global loadedPop
    loadedPop = jsonpickle.decode(f.read())
    f.close()
    print("Pop: " + name + ", Gen: " + str(gen) + " loaded")
    return loadedPop

def loadPopOld(name:str,gen:int) -> Population:
    f = open("Populations\\"+ name + "_Gen_" + str(gen) + ".pickle", 'rb')
    global loadedPop
    loadedPop = pickle.load(f)
    f.close()
    print("Pop: " + name + ", Gen: " + str(gen) + " loaded")
    return loadedPop

def loadPop(name:str,gen:int) -> Population:
    popPath = 'Populations\\' + name + '\\' + name + "_Gen_" + str(gen) + '.pickle'
    f = open(popPath,'rb')
    newPop = pickle.load(f)
    f.close()
    print("Pop: " + name + ", Gen: " + str(gen) + " loaded")
    return newPop

def clamp(num:float, min_value:float, max_value:float) -> float:
        num = max(min(num, max_value), min_value)
        return num

def sortFunc(e:int) -> int:
    return e[1]

def fitnessSortFunc(e:int) -> int:
    return e.fitness

class Point():
    def __init__(self,pos:tuple,friction:float = None):
        self.pos = pos
        if friction == None:
            self.friction = random.random()
        else:
            self.friction = friction
        self.elasticity = random.random()

class Link():
    def __init__(self,connected:tuple, delta:float = None, dutyCycle:float = None, period:float = None, phase:float = None, strength:int = None):
        self.connected = connected
        if delta == None:
            self.delta = random.uniform(configs.minDelta,configs.maxDelta)
        else:
            self.delta = delta
        if dutyCycle == None:
            self.dutyCycle = random.uniform(configs.minDutyCycle,configs.maxDutyCycle)
        else:
            self.dutyCycle = dutyCycle
        if period == None:
            self.period = random.uniform(configs.minPeriod,configs.maxPeriod)
        else:
            self.period = period
        if phase == None:
            self.phase = random.uniform(configs.minPhase,configs.maxPhase)
        else:
            self.phase = phase
        if strength == None:
            self.strength = random.uniform(configs.minStrength,configs.maxStrength)
        else:
            self.strength = strength

class CreatureCreator():
    def __init__(self,numPoints:int,scale:int,radius:int,id:int = 0,points:PointList = None, links:LinkList = None, parent:int = None) -> None:
        if points == None and links == None:
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
            self.parent = 0
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
        elif points != None and links != None:
            self.numPoints = numPoints
            self.scale = scale
            self.radius = radius
            self.id = id
            self.points = points
            self.links = links
            self.fitness = 0
            self.parent = parent
        else:
            quit("Insufficient Information to create custom creature")
        
    def getLinkByConnection(self,connected:tuple) -> Link:
        for link in self.links:
            if link.connected == connected:
                return link

    def getLinksOfPoint(self,point:Point) -> LinkList:
        connectedLinks = []
        for link in self.links:
            if self.points.index(point) in link.connected:
                connectedLinks.append(link)
        return connectedLinks
    
    def getConnectedPoints(self,point:Point) -> PointList:
        connectedPoints = []
        for l in self.links:
            if self.points.index(point) in l.connected:
                if self.points.index(point) == l.connected[0]:
                    connectedPoints.append(l.connected[1])
                else:
                    connectedPoints.append(l.connected[0])
        return connectedPoints
class Population():
    def __init__(self,popName:str,genNum:int = 0) -> None:
        self.popName = popName
        self.genNum = genNum

        self.avgFitness = 0
        self.topFitness = 0

        self.creatures = []

        self.lastId = 1
    
    def savePop(self,name:str = None) -> None:
        nameToUse = None
        if name:
            nameToUse = name
        else:
            nameToUse = self.popName
            
        popPath = 'Populations\\' + nameToUse + '\\' 
        if not os.path.isdir(popPath):
            os.mkdir(popPath)
        popPath = 'Populations\\' + nameToUse + '\\' + nameToUse + "_Gen_" + str(self.genNum) + '.pickle'
        f = open(popPath,'wb')
        pickle.dump(self,f)
        f.close()
        print("Saving Finished")

    def renamePop(self,name:str) -> None:
        popPath = 'Populations\\' + self.popName + '\\'
        if os.path.isdir(popPath):
            files = os.listdir(popPath)
            if files:
                popPath = 'Populations\\' + self.popName + '\\' + self.popName + "_Gen_" + str(self.genNum) + '.pickle'
                for x in range(len(files)-1):
                    tempPop = loadPop(self.popName,x)
                    tempPop.name = name
                    tempPop.savePopTest(name)
                summaryPath = 'Populations\\' + self.popName + '\\' + self.popName + '_summary.csv'  
                self.popName = name
                summaryDestination = 'Populations\\' + self.popName + '\\' + self.popName + '_summary.csv'
                os.rename(summaryPath,summaryDestination)
                
                
                            
    def addCreatures(self,creatures:CreatureCreatorList) -> None:
        self.creatures.extend(creatures)

    def addRandomCreatures(self,amount:int,scale:int = 100,radius:int = 10) -> None:
        for i in range(amount):
            self.creatures.append(CreatureCreator(random.randrange(configs.minPoints,configs.maxPoints),scale,radius,self.lastId))
            self.lastId += 1
    
    def savePopJson(self) -> None:
        f = open("Populations\\"+ self.popName + "_Gen_" + str(self.genNum) + ".json", 'w+')
        f.writelines(jsonpickle.encode(self, indent = 2))
        f.close()
        print("Saving Json Finished")

    def savePopOld(self) -> None:
        f = open("Populations\\"+ self.popName + "_Gen_" + str(self.genNum) + ".pickle", 'wb')
        pickle.dump(self,f)
        f.close()
        print("Saving Finished")

    def getCreatures(self) -> CreatureCreatorList:
        return self.creatures
    
    def getBestCreature(self) -> CreatureCreator:
        for c in self.creatures:
            if self.topFitness == c.fitness:
                return c

    def getMedianCreature(self) -> CreatureCreator:
        for c in self.creatures:
            if self.medianFitness == c.fitness:
                return c
    
    def sortCreatures(self) -> None:
        self.creatures.sort(key=fitnessSortFunc)

    def getPreview(self) -> None:
        self.sortCreatures()
        sample = []

        for x in range(0,len(self.creatures),len(self.creatures)//4):
            sample.append(self.creatures[x])
        for x in range(len(self.creatures)-1,len(self.creatures)-10,-1):
            sample.append(self.creatures[x])

        return sample
    
    def keepTopPercent(self,topPercent:float) -> None:
        self.sortCreatures()
        toKill = []
        for x in range(int(len(self.creatures)*(1-topPercent))):
            toKill.append(self.creatures[x].id)
        self.killSpecified(toKill)

    def linkMutation(self,creature:CreatureCreator) -> None:
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

    def pointMutation(self,creature:CreatureCreator) -> None:

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

            #Average the properties of links that will be merged into its counter part connected to merger
            commonPoints = list(set(creature.getConnectedPoints(merger)).intersection(set(creature.getConnectedPoints(mergee))))
            mergerLinks = creature.getLinksOfPoint(merger)
            mergeeLinks = creature.getLinksOfPoint(mergee)
            mergeeIndex = creature.points.index(mergee)

            # for l in range(len(mergeeLinks)): #broken
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
            #Add new Point
            invalid = True
            attempts = 0
            while invalid:
                pos = (random.random()*creature.scale,random.random()*creature.scale)
                if len(creature.points) > 0:
                    for y in creature.points:
                        invalid = False
                        if sqrt(((y.pos[0] - pos[0])**2 + (y.pos[1] - pos[1])**2)) < creature.radius:
                            invalid = True
                else:
                    invalid = False
                attempts += 1
                if attempts > 1000:
                    print("New Point could not be added")
                    break
            creature.points.append(Point(pos))
            #Connect New Point
            linksToMake = random.randrange(1,len(creature.points))
            possibleConnections = []
            for x in range(len(creature.points)-1):
                possibleConnections.append(tuple((x,len(creature.points)-1)))
            for x in range(linksToMake):
                newConnection = random.choice(possibleConnections)
                creature.links.append(Link(newConnection))
            
        else:
            #Choose random point and find connected links
            pointToRemove = random.choice(creature.points)
            linksToRemove = creature.getLinksOfPoint(pointToRemove)
            index = creature.points.index(pointToRemove)
            #Remove point and its links
            creature.points.remove(pointToRemove)
            for link in linksToRemove:
                creature.links.remove(link)
            #rebuild creature
            for l in creature.links:
                if l.connected[0] > index:
                    l.connected = (l.connected[0] - 1,l.connected[1])                  
                if l.connected[1] > index:
                    l.connected = (l.connected[0],l.connected[1]- 1)
                
    def nextGeneration(self,simResults:list, bottomPercent:float = 0.5, topPercent:float = 0.1,keepParent:bool = False) -> None:
        #Give each creature there fitness result
        for creature in self.creatures:
            for creatureResult in simResults:
                if creatureResult[0] == creature.id:
                    creature.fitness = creatureResult[1]

        #Create a list of all fitnesses
        fitnessList = []
        for c in simResults:
            fitnessList.append(c[1])            

        #Sort the results in ascending order according to the fitness of each creature
        simResults.sort(key=sortFunc)

        #Record the highest fitness of the current generation
        self.topFitness = simResults[-1][1]

        #Calculate and record the average fitness of the current Generation
        simResultIds = []
        sum = 0
        for x in simResults:
            sum += x[1]
            simResultIds.append(x[0])
        self.avgFitness = sum/len(simResults)

        #Calculate and record the median fitness of the current Generation
        originalLen = len(simResults)
        bottom = floor(len(simResults)*bottomPercent)
        self.medianFitness = simResults[bottom][1]

        toKill = []
        toMutate = []

        #Mark bottom 50% for termination
        for c in range(bottom):
            toKill.append(simResults[c][0])
            simResultIds.remove(simResults[c][0])
        
        #Mark 'flats' for termination
        for c in range(len(simResults)):
            if simResults[c][2] and simResults[c][0] not in toKill:
                toKill.append(simResults[c][0])
                simResultIds.remove(simResults[c][0])

         #Terminate undesirables
        self.killSpecified(toKill)

        #Determine how many creatures are in the top 20% remaining (original top 10%)
        top = int(len(simResults)*(topPercent/bottomPercent))


        if top >= len(simResultIds) and not keepParent:
            self.mutateSpecified(simResultIds,2) #If less creatures than 10% the original amount do this
        elif top >= len(simResultIds) and keepParent:
            self.mutateSpecified(simResultIds,1,keepParent=True)
        else:
            #Mark top 10% to be mutated
            for c in range(top):
                toMutate.append(simResultIds[c])
            for c in toMutate:
                simResultIds.remove(c)

            #Create 2 mutated offspring for each of the top 10%
            self.mutateSpecified(toMutate,2)

            toMutate.clear()

            #Mark Remainder to be mutated
            for c in simResultIds:
                toMutate.append(c)
            #Create 1 mutated offspring for each of rest
            self.mutateSpecified(toMutate,1)

        #Fill the remaining spots with random creatures
        self.addRandomCreatures(originalLen-len(self.creatures))

        #Summary to be logged at the end of each generation
        summary = "\nGeneration: " + str(self.genNum) + " Avg: " + str(self.avgFitness) + " Best: " + str(self.topFitness) + " Median: " + str(self.medianFitness)
        print(summary)

        #Makes sure that the data cvs is cleared at generation 0
        if self.genNum == 0:
             f = open("Populations\\"+ self.popName + "_summary.csv", 'w+')
             f.close()

        #Write fitness list to cvs file
        f = open("Populations\\"+ self.popName + "_summary.csv", 'a')
        csv.writer(f).writerow(fitnessList)
        f.close()

        #Increments generation counter for the next generation
        self.genNum += 1

    def killSpecified(self,toKill:CreatureIdList) -> None:
        fuck = []
        for i,c in enumerate(self.creatures):
            if c.id in toKill:
                fuck.append(i)
        for i in sorted(fuck,reverse=True):
            del self.creatures[i]
        
    def mutateSpecified(self,toMutate:CreatureIdList,offspringPer:int,keepParent:bool = False) -> None:
        
        tempCreatures = []
        tempToMutate = []
        
        #Create Copies if needed
        if keepParent:
            for c in self.creatures:
                if c.id in toMutate:
                        cpy = copy.deepcopy(c)
                        cpy.parent = c.id
                        cpy.id = self.lastId
                        tempToMutate.append(self.lastId)
                        tempCreatures.append(cpy)
                        self.lastId += 1
            toMutate.clear()
            self.creatures.extend(tempCreatures)
            toMutate.extend(tempToMutate)

        else:  
            for c in self.creatures:
                if c.id in toMutate:
                    if offspringPer > 1:
                        #for cc in range(offspringPer-1): #Only works for 1 or 2 
                        cpy = copy.deepcopy(c)
                        cpy.parent = c.id
                        cpy.id = self.lastId
                        tempToMutate.append(self.lastId)
                        tempCreatures.append(cpy)
                        self.lastId += 1
                        
            self.creatures.extend(tempCreatures)
            toMutate.extend(tempToMutate)

        #Preform Basic Mutations
        for c in self.creatures:
            if c.id in toMutate:
                c.parent = c.id
                c.id = self.lastId
                
                self.lastId += 1
                                
                for p in c.points:
                    p.pos = (clamp(p.pos[0]+random.uniform(-1,1),0,c.scale*1.5),clamp(p.pos[1]+random.uniform(-1,1),0,c.scale*1.5))
                    
                    p.friction = clamp(p.friction + random.uniform(-1,1),configs.minFriction,configs.maxFriction)
                    
                    p.elasticity = clamp(p.elasticity + random.uniform(-1,1),0,1)

                for l in c.links:
                
                    l.delta = clamp(l.delta + random.uniform(-0.015,0.015),configs.minDelta,configs.maxDelta)

                    l.dutyCycle = clamp(l.dutyCycle + random.uniform(-0.008,0.008),configs.minDutyCycle,configs.maxDutyCycle)

                    l.period = clamp(l.period + random.uniform(-0.06,0.06),configs.minPeriod,configs.maxPeriod)

                    l.phase = clamp(l.phase + random.uniform(-0.06,0.06),configs.minPhase,configs.maxPhase)

                    l.strength = clamp(l.strength + random.uniform(-(configs.maxStrength-configs.minStrength)/100,(configs.maxStrength-configs.minStrength)/100),configs.minStrength,configs.maxStrength)

                if configs.advancedMutationChance < 0.05:
                    if random.random() < 0.5:
                        self.pointMutation(c)
                    else:
                        self.linkMutation(c)