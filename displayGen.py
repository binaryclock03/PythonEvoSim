import simObjects as so
import populationManager as pm

testPop = pm.loadPop("LongTest", 1000)
so.playback(0, testPop.creatures)