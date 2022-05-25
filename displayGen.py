import simObjects as so
import populationManager as pm

testPop = pm.loadPop("fastTest", 10)
so.playback(30, [testPop.getBestCreature()])