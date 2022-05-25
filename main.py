import simObjects as so
import populationManager as pm

testPop = pm.Population("fastTest")
testPop.addRandomCreatures(1000)

for x in range(1):
    testPop.nextGenertation(so.fastsim(10, creatureList=testPop.creatures, TPS = 60))
    testPop.savePop()