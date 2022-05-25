import time
import simObjects as so
import populationManager as pm

if __name__ == '__main__':
    print("Generating First Population")
    testPop = pm.Population("fastTest")
    testPop.addRandomCreatures(100)
    print("Saving First Population")
    testPop.savePop()

    print("Begining generations")
    for x in range(1000):
        startTime = time.time()
        testPop.nextGenertation(so.fastsim(10, creatureList=testPop.creatures, TPS = 60))
        endTime = time.time()
        print("Elapsed time for simulating generation: " + str(endTime - startTime))

        startTime = time.time()
        testPop.savePop()
        endTime = time.time()
        print("Elapsed time for saving generation: " + str(endTime - startTime))
