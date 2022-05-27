"""
=================
Multiple subplots
=================

Simple demo with multiple subplots.

For more options, see :doc:`/gallery/subplots_axes_and_figures/subplots_demo`.

.. redirect-from:: /gallery/subplots_axes_and_figures/subplot_demo
"""

from statistics import median
import numpy as np
import matplotlib.pyplot as plt
import csv
import populationManager as pm

pop = pm.loadPop("öHÓÛ",0)

#Collect data
data = []
f = open("Populations\\"+ pop.popName + '\\' + pop.popName + "_summary.csv", 'r')
raw = csv.reader(f)
for row in raw:
    if row:
        r = []
        for x in row:
            r.append(int(float(x)))
        data.append(r)
f.close()

#Analysis
bests = []
for row in data:
    bests.append(max(row))

averages = []
for row in data:
    sum = 0
    for num in row:
        sum += num
    averages.append(sum/len(row))

medians = []
for row in data:
    medians.append(median(row))

generations = len(medians)
generationsList = range(generations)

fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle('Fitnesses Per Generation')

ax1.plot(generationsList, bests)
ax1.plot(generationsList, averages)
ax1.plot(generationsList, medians)
ax1.set_ylabel('Fitness')

#ax2.plot(x2, y2, '.-')
#ax2.set_xlabel('time (s)')
#ax2.set_ylabel('Undamped')

plt.show()
