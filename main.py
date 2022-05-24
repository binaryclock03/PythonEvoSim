import simObjects as so
import populationManager as pm

testPop = pm.Population("name")
testPop.addRandomCreatures(100)
testPop.savePop()
testPop = pm.loadPop("name",0)

for x in range(100):

    testPop.nextGenertation(so.sim(10,creatureList=testPop.creatures,graphics=False))

    testPop.savePop()