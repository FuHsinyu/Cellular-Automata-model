from pycx_gui import GUI
from myModel import CAmodel
import matplotlib.pyplot as plt
import numpy as np
import random
#change digit in line 18 and run to get a FAST TESTING RESULT
initRow = [0] * 100
for i in range(100):
    initRow[i] = random.randrange(2)
r = 1  #range
systemSize = r * 2 + 1
k = 2  #base
rule = 0  #decimal rule initilized
cycleLenList = []  #final cycle length recording list
cycleReachedBool = False  #booleanB
resultDict = dict()  #hash results with respect to rules
while rule < 6:  #By changing these for FAST TEST
    model = CAmodel(r, k, rule, initRow, systemSize)
    #def __init__(self, range, base, rule, initRow, systemSize):
    runTime = 0  #run times
    while runTime < 10e4:
        currentRow = tuple(model.currentRow)
        if currentRow not in resultDict:
            resultDict[currentRow] = runTime
            #print(resultDict)
        else:
            cycleLenList.append(runTime - resultDict[currentRow])
            cycleReachedBool = True
            break
        runTime += 1
        model.step()
    if not cycleReachedBool:
        cycleLenList.append(-1)
    rule += 1  #
    cycleReachedBool = False
    resultDict.clear()
model.draw(cycleLenList)