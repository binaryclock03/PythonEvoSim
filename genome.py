import pickle
import time
import populationManager as pm

def convertToGenome(creature):
    id = creature.id

    points = creature.points
    links = creature.links
    id = creature.id

    numJoints = len(points)
    numLimbs = len(links)

    linkGenome = ""
    for link in links:
        a, b = link.connected
        linkGenome += "OAla" + str(a) + "lb" + str(b) + "Bde" + str(int(1000*link.delta)) + "dc" + str(int(1000*link.dutyCycle)) + "pe" + str(int(1000*link.period)) + "pa" + str(int(1000*link.phase)) + "st" + str(int(1000*link.strength))
    
    pointGenome = ""
    for point in points:
        x, y = point.pos
        pointGenome += "OAxp" + str(int(1000*x)) + "yp" + str(int(1000*y)) + "fr" + str(int(1000*point.friction)) + "rd" + str(int(10))
    
    genome = "cid" + str(id) + "njt" + str(numJoints) + "nlb" + str(numLimbs) + "ljt" + pointGenome + "llb" + linkGenome 
    return genome

def convertFromGenome(genome):
    _, genome = genome.split("cid")
    id, genome = genome.split("njt")
    numJoints, genome = genome.split("nlb")
    numLimbs, genome = genome.split("ljt")
    jointGenome, limbGenome = genome.split("llb")
    
    links = []
    limbGenomeList = limbGenome.split("O")
    del limbGenomeList[0]
    for linkGenome in limbGenomeList:
        _,linkGenome = linkGenome.split("Ala")
        a,linkGenome = linkGenome.split("lb")
        a = int(a)
        b,linkGenome = linkGenome.split("Bde")
        b = int(b)
        delta,linkGenome = linkGenome.split("dc")
        delta = int(delta)/1000
        dutyCycle,linkGenome = linkGenome.split("pe")
        dutyCycle = int(dutyCycle)/1000
        period,linkGenome = linkGenome.split("pa")
        period = int(period)/1000
        phase,strength = linkGenome.split("st")
        phase = int(phase)/1000
        strength = int(strength)/1000
        links.append(pm.Link((a,b), delta = delta, dutyCycle=dutyCycle, period=period, phase=phase, strength=strength))
    
    points = []
    jointGenomeList = jointGenome.split("O")
    del jointGenomeList[0]
    for pointGenome in jointGenomeList:
        _,pointGenome = pointGenome.split("Axp")
        x,pointGenome = pointGenome.split("yp")
        x = int(x)/1000
        y,pointGenome = pointGenome.split("fr")
        y = int(y)/1000
        friction,radius = pointGenome.split("rd")
        friction = int(friction)/1000
        radius = int(radius)
        points.append(pm.Point((x,y), friction = friction))

    creature = pm.CreatureCreator(numJoints, 100, 15, id=id, points=points, links=links)
    return creature

def genomeSave(creatures):
    creatureGenomeList = []
    for creature in creatures:
        creatureGenomeList.append(convertToGenome(creature))

    f = open("Populations\\test.pickle", 'wb')
    pickle.dump(creatureGenomeList,f)
    f.close()
    print("Genome Saving Finished")

def genomeLoad():
    pass

if __name__ == '__main__':
    testPop = pm.Population("genomeTest")
    testPop.addRandomCreatures(10000)

    startTime = time.time()
    testPop.savePop()
    endTime = time.time()
    print("Elapsed time for saving generation: " + str(endTime - startTime))

    startTime = time.time()
    genomeSave(testPop.creatures)
    endTime = time.time()
    print("Elapsed time for saving generation: " + str(endTime - startTime))
    