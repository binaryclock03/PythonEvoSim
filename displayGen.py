import simObjects as so
import populationManager as pm

testPop = pm.loadPop("fastTest", 10)
so.playback(0, testPop.creatures)