import bin.simObjects as so
import bin.populationManager as pm
import bin.simulations as sim

testPop = pm.Population("genomeTest")
testPop.addRandomCreatures(1)
sim.playback(0, testPop.creatures)
