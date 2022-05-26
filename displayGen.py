import simObjects as so
import populationManager as pm
import simulations as sim

testPop = pm.Population("genomeTest")
testPop.addRandomCreatures(1)
sim.playback(0, testPop.creatures)