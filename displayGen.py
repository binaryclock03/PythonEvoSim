import simObjects as so
import populationManager as pm

testPop = pm.loadPop("fastTest", 99)
so.sim(30,creatureList=testPop.creatures)