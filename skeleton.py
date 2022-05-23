import random as random
from math import sqrt

def genSkeleton(numPoints,scale,radius):
    
    points = []
    links = []
    
    #Create List of Points
    for x in range(numPoints):
        invalid = True
        i = 0
        while invalid:
            pos = (random.random()*scale,random.random()*scale)
            if len(points) > 0:
                for y in points:
                    invalid = False
                    if sqrt(((y[0] - pos[0])**2 + (y[1] - pos[1])**2)) < radius:
                        invalid = True
            else:
                invalid = False
            i += 1
            if i > 1000:
                quit("Point Generation Failed")
        points.append(pos)
    
    #Generate All Possible Links
    for x in range(numPoints):
        for y in range(x+1,(numPoints)):
            links.append((x,y))
    
    #Simplification
    for x in range(numPoints-3):
        links.pop(random.randrange(0,len(links)))

    return points,links