import populationManager as pm

def convertToGenome(creature):
    id = creature.id

    points = creature.points
    links = creature.links

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
    
    genome = "njt" + str(numJoints) + "nlb" + str(numLimbs) + "ljt" + pointGenome + "llb" + linkGenome 
    return genome

def convertFromGenome(genome):
    _, genome = genome.split("njt")
    numJoints, genome = genome.split("nlb")
    numLimbs, genome = genome.split("ljt")
    jointGenome, limbGenome = genome.split("llb")
    
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
        
    pass

if __name__ == '__main__':
    testPop = pm.Population("genomeTest")
    testPop.addRandomCreatures(1)
    for creature in testPop.creatures:
        genome = convertToGenome(creature)
        #print(genome)
        convertFromGenome(genome)