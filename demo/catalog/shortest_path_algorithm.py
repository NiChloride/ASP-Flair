import copy

def shortestPath(listOfLocations, listOfDictionary,fromMWGOC):
    listOfDistances = []
    lOL = copy.deepcopy(listOfLocations)
    lOD = copy.deepcopy(listOfDictionary)
    num = len(lOL)
    bestOrder = lOL
    for i in range ((1+num)*num//2):
        lOL.append(lOL[0])
        lOL.pop(0)
        lOD.append(lOD[0])
        lOD.pop(0)
        listOfDistances.append(calculateDistance(lOL, lOD, fromMWGOC))
        if(calculateDistance(lOL, lOD, fromMWGOC)==min(listOfDistances)):
            bestOrder = lOL

    return bestOrder



def calculateDistance (orderedListOfLocation,orderedListOfDictionary,fromMWGOC): 
    oLD = copy.deepcopy(orderedListOfDictionary)
    oLL = copy.deepcopy(orderedListOfLocation)
    distance = fromMWGOC[oLL[0]]
    
    for i in range(len(oLL)-1) :
        distance += oLD[i][oLL[i+1]]
    distance += fromMWGOC[oLL[len(oLL)-1]]
    return distance





fromMWGOC = {"NLC":12.54, "PCC":4.68, "SKWC":15.32} #keeps the distances to different locations

fromNLC = {"MWGOC":12.54,"PCC":9.92, "SKWC":2.96}
fromSKWC = {"MWGOC":15.32,"NLC":2.96,"PCC":12.88}
fromPCC = {"MWGOC":4.68,"NLC":9.92,"SKWC":12.88}

needToGo = [fromNLC, fromSKWC, fromPCC]
orderedListOfLocation = ["NLC", "SKWC", "PCC"]

print(shortestPath(orderedListOfLocation,needToGo,fromMWGOC))



