import simObjects as so
import populationManager as pm

testPop = pm.loadPop("name", 100)
so.sim(30,creatureList=testPop.creatures)