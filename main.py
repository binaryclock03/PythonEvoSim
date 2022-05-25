import simObjects as so
import populationManager as pm

if __name__ == '__main__':
    testPop = pm.Population("fastTest")
    testPop.addRandomCreatures(1000)
    testPop.savePop()
    testPop = pm.loadPop("fastTest",0)

    for x in range(1000):
        testPop.nextGenertation(so.fastsim(10, creatureList=testPop.creatures, TPS = 60))
        testPop.savePop()