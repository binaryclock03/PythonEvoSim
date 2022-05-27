from statistics import median
import numpy as np
import matplotlib.pyplot as plt
import csv
import populationManager as pm
from matplotlib.widgets import Slider, Button
import os

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

fig, (ax1, ax2) = plt.subplots(2, 1,figsize=(10, 8))
#fig.subtitle('Fitnesses Per Generation')

plt.subplots_adjust(bottom=0.2)

slider = plt.axes([0.2, 0.1, 0.65, 0.03])
slider = Slider(
    ax=slider,
    label='Generation',
    valmin=0,
    valmax=generations,
    valinit=0,
    valstep = generationsList
)
ax1.grid(True)
fit = ax1.plot(generationsList, bests,generationsList, averages,generationsList, medians)
ax1.set_ylabel('Fitness')

histo = ax2.hist(data[0],100)
ax2.set_xlabel('Fitness')
ax2.set_ylabel('Creatures')

def update(val):
    ax2.clear()
    histo = ax2.hist(data[val],100)
    fig.canvas.draw_idle()
    
def updateFit():
    pass


# register the update function with each slider
slider.on_changed(update)


plt.show()

