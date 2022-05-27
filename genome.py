from collections import defaultdict
import math
import pickle
import random
from statistics import median

from numpy import average
import populationManager as pm
import simulations as sim

def convertToGenome(creature):
    points = creature.points
    links = creature.links

    genome = b''

    #header
    genome += int(creature.id).to_bytes(4, 'little')
    genome += int(creature.parent).to_bytes(4, 'little')
    genome += int(len(points)).to_bytes(1, 'little')
    genome += int(len(links)).to_bytes(2, 'little')
    genome += int(creature.fitness).to_bytes(3, 'little')
    genome += int(creature.scale).to_bytes(3, 'little')
    
    for point in points:
        genome += int(point.pos[0]/creature.scale*10000).to_bytes(2,'little')
        genome += int(point.pos[1]/creature.scale*10000).to_bytes(2,'little')
        genome += int(point.friction*10000).to_bytes(2,'little')
        #genome += int(point.radius).to_bytes(2,'little')
        genome += int(10).to_bytes(2,'little')

    for link in links:
        genome += int(link.connected[0]).to_bytes(1,'little')
        genome += int(link.connected[1]).to_bytes(1,'little')
        genome += int(link.delta*10000).to_bytes(2,'little')
        genome += int(link.dutyCycle*10000).to_bytes(2,'little')
        genome += int(link.period).to_bytes(2,'little')
        genome += int(link.phase).to_bytes(2,'little')
        genome += int(link.strength/1000).to_bytes(2,'little')

    return genome

def speciesFromGenome(genome):
    pointsLen = int.from_bytes(genome[8:9], 'little')
    return pointsLen

def convertFromGenome(genome):
    id = int.from_bytes(genome[0:4], 'little')
    pid = int.from_bytes(genome[4:8], 'little')
    pointsLen = int.from_bytes(genome[8:9], 'little')
    linksLen = int.from_bytes(genome[9:11], 'little')
    fitness = int.from_bytes(genome[11:14], 'little')
    scale = int.from_bytes(genome[14:17], 'little')

    hdln = 17
    pointsList = []
    for i in range(pointsLen):
        cur = hdln + (i*8)
        x = int.from_bytes(genome[cur:cur+2], 'little')/10000*scale
        y = int.from_bytes(genome[cur+2:cur+4], 'little')/10000*scale
        friction = int.from_bytes(genome[cur+4:cur+6], 'little')/10000
        radius = int.from_bytes(genome[cur+6:cur+8], 'little')
        pointsList.append(pm.Point((x,y), friction))

    linksList = []
    for i in range(linksLen):
        cur = hdln + (pointsLen*8) + (i*12)
        connectedA = int.from_bytes(genome[cur:cur+1], 'little')
        connectedB = int.from_bytes(genome[cur+1:cur+2], 'little')
        delta = int.from_bytes(genome[cur+2:cur+4], 'little')/10000
        dutyCycle = int.from_bytes(genome[cur+4:cur+6], 'little')/10000
        period = int.from_bytes(genome[cur+6:cur+8], 'little')
        phase = int.from_bytes(genome[cur+8:cur+10], 'little')
        strength = int.from_bytes(genome[cur+10:cur+12], 'little')*1000
        linksList.append(pm.Link((connectedA, connectedB), delta, dutyCycle, period, phase, strength))
    
    return pm.CreatureCreator(pointsLen, scale, 10, id = id, points = pointsList, links = linksList, parent = pid)

def genomeSave(population):
    f = open("Populations\\test.bin", 'wb')
    for creature in population.creatures:
        f.write(convertToGenome(creature))
    f.close()
    print("Genome Saving Finished")

def genomeLoad(fileName):
    f = open("Populations\\" + fileName + ".pickle", 'rb')
    creatureGenomeList = pickle.load(f)
    f.close()

    creatures = []
    for creatureGenome in creatureGenomeList:
        creatures.append(convertFromGenome(creatureGenome))
    
    population = pm.Population("GenomeLoaded")
    population.addCreatures(creatures)
    print("Genome Loading Finished")
    return population

def compareGenomes(genomeList):
    d = defaultdict(list)
    variationPerSpecies = {}
    for genome in genomeList:
        species = speciesFromGenome(genome)
        d[species].append(hex(int.from_bytes(genome[17:], 'little')))
    
    for key in d:
        length = len(d[key][0])
        numCreatures = len(d[key])
        values = [0]*length
        for index in range(length):
            frequency = defaultdict(int)
            for genome in d[key]:
                gene = genome[index]
                frequency[gene] += 1
            for gene in frequency:
                prob = frequency[gene]/len(d[key])
                values[index] += prob*math.log2(1/prob)
        variationPerSpecies[key] = (average(values),numCreatures)
    
    return variationPerSpecies

    



if __name__ == '__main__':
    testPop = pm.loadPopOld("LUCE",1005)

    # testPop = pm.Population("ree")
    # testPop.addRandomCreatures(10000)

    creatures = testPop.creatures
    genomes = []
    for creature in creatures:
        genomes.append(convertToGenome(creature))

    print(compareGenomes(genomes))
