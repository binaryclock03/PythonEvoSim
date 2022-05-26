import time
import simObjects as so
import populationManager as pm
import simulations as sim

seeding = True

if __name__ == '__main__':
    print("Generating First Population")
    if seeding:
        testPop = pm.Population("seedingTest")
        testPop.addRandomCreatures(10000)
        print("Saving First Population")
        testPop.savePop()

        print("Seeding")
        for x in range(5):
            startTime = time.time()
            testPop.nextGenertation(sim.fastsim(10, creatureList=testPop.creatures, TPS = 60))
            endTime = time.time()
            print("Elapsed time for simulating generation: " + str(endTime - startTime))

            startTime = time.time()
            testPop.savePop()
            endTime = time.time()
            print("Elapsed time for saving generation: " + str(endTime - startTime))

        testPop.keepTopPercent(0.1)

        print("Begining generations")
        for x in range(1000):
            startTime = time.time()
            testPop.nextGenertation(sim.fastsim(10, creatureList=testPop.creatures, TPS = 60),bottomPercent=0.5,topPercent=0.5)
            endTime = time.time()
            print("Elapsed time for simulating generation: " + str(endTime - startTime))

            startTime = time.time()
            testPop.savePop()
            endTime = time.time()
            print("Elapsed time for saving generation: " + str(endTime - startTime))

    else:
        testPop = pm.Population("fastTest")
        testPop.addRandomCreatures(100)
        print("Saving First Population")
        testPop.savePop()
    
        print("Begining generations")
        for x in range(1000):
            startTime = time.time()
            testPop.nextGenertation(sim.fastsim(10, creatureList=testPop.creatures, TPS = 60))
            endTime = time.time()
            print("Elapsed time for simulating generation: " + str(endTime - startTime))

            startTime = time.time()
            testPop.savePop()
            endTime = time.time()
            print("Elapsed time for saving generation: " + str(endTime - startTime))
