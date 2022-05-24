import simObjects as so
import populationManager as pm


testPop = pm.loadPop("testing",0)

for x in range(10):

    testPop.nextGenertation(so.sim(30,creatureList=testPop.creatures, graphics=False))

    testPop.savePop()