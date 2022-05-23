import random as random

points = []
links = []
numPoints = 4

#Create List of Points
for x in range(numPoints):
    points.append((random.random(),random.random()))

#Generate All Possible Links
for x in range(numPoints):
    for y in range(x+1,(numPoints)):
        links.append((x,y))

#Simplification
for x in range(numPoints-3):
    links.pop(random.randrange(0,len(links)))

