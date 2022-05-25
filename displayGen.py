import simObjects as so
import populationManager as pm

testPop = pm.loadPop("fastTest", 5)
so.playback(30, testPop.creatures)