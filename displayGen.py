import simObjects as so
import populationManager as pm
import simulations as sim

testPop = pm.loadPop("LongTest", 1000)
sim.playback(0, testPop.getPreview())