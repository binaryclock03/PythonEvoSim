import simObjects as so
import populationManager as pm


testPop = pm.loadPop("testing",0)

for x in range(10):

    testPop.nextGenertation(so.sim(30,creatureList=testPop.creatures))

    testPop.savePop()



#print(so.simNoGraphics(10, 10))