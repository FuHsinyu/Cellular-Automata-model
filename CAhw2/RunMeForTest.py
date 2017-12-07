from pycx_gui import GUI
from myModel import CAmodel
import matplotlib.pyplot as plt
import numpy as np
import random


def initial_row(rowLength):
    initRow = [0] * rowLength
    for i in range(rowLength):
        initRow[i] = random.randrange(2)
    return initRow


initRow = initial_row(100)
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
model.get_random_table(10)
model.get_table_work_through(10)
model.draw(cycleLenList)
