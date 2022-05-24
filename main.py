import simObjects as so
import populationManager as pm

testPop = pm.Population("fastTest")
testPop.addRandomCreatures(1000)
testPop.savePop()
testPop = pm.loadPop("fastTest",0)

for x in range(1000):
    testPop.nextGenertation(so.fastsimthing(10,creatureList=testPop.creatures))
    testPop.savePop()