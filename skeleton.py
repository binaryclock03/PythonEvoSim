import random as random

def genSkeleton(numPoints,scale):
    
    points = []
    links = []
    
    #Create List of Points
    for x in range(numPoints):
        points.append((random.random()*scale,random.random()*scale))
    
    #Generate All Possible Links
    for x in range(numPoints):
        for y in range(x+1,(numPoints)):
            links.append((x,y))
    
    #Simplification
    for x in range(numPoints-3):
        links.pop(random.randrange(0,len(links)))
        
    return points,links

