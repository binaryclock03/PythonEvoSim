import simObjects as so
import populationManager as pm
import simulations as sim

testPop = pm.loadPop("fastTest", 1310)
sim.playback(0, testPop.getPreview())
