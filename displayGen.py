import simObjects as so
import populationManager as pm
import simulations as sim

testPop = pm.loadPopTest("seedingTest", 0)
#sim.playback(0, testPop.getPreview())
testPop.renamePop('saveTest')