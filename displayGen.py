import simObjects as so
import populationManager as pm

testPop = pm.loadPop("LongTest", 3532)
so.playback(30, [testPop.getBestCreature()])