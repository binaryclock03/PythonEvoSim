import simObjects as so
import populationManager as pm
import simulations as sim

testPop = pm.loadPop("seedingTest", 200)
sim.playback(0, testPop.getPreview())
