from pycx_gui import GUI
from myModel import CAmodel
import matplotlib.pyplot as plt
import numpy as np
import random


def initial_row(initRowLength, density):
    initRow = [0] * initRowLength
    for i in range(initRowLength):
        if (random.random() > density):
            initRow[i] = 0
        else:
            initRow[i] = 1
    return initRow


def count_1(list, initRowLength):
    x = 0
    for i in range(initRowLength):
        if (list[i] == 1):
            x += 1
    return x


r = 1  #range
k = 2  #base
systemSize = r * 2 + 1
initRowLength = 100
densityListXaxis = list()
flowListYaxis = list()
initStateTimes = 10  # R
densityRange = np.linspace(0, 1, 201)
rule = 184
#densityRange = [0.4]
initRow = [0] * initStateTimes
flowVehicleList = [0] * initStateTimes
for density in densityRange:
    for R in range(initStateTimes):
        initRow[R] = initial_row(initRowLength, density)
        model = CAmodel(r, k, rule, initRow[R], systemSize)
        #def __init__(self, range, base, rule, initRow, systemSize):
        runTime = 0  #run times
        flowVehicle = 0
        #flowTime = 50
        while runTime < 1000:  #T
            currentRow = tuple(model.currentRow)
            runTime += 1
            currentRow = model.step()
            if (currentRow[0] == 1):
                if (currentRow[1] == 0):
                    flowVehicle += 1
            #print("current row:", currentRow)
            #rowDraw.append(currentRow)
        flowVehicleList[R] = flowVehicle
    densityListXaxis.append(density)
    flowListYaxis.append(np.mean(flowVehicle))

#np.floor(np.array(rowDraw))
#print(densityListXaxis, flowListYaxis)
#print(rowDraw)
#testArr = np.array([[1, 1, 1, 2, 3, 4], [1, 2, 3, 4, 5, 6]])
#print(np.reshape(rowDraw, (100, 102)))
#model.draw_hw4_bin(rowDraw)
model.draw_hw4(densityListXaxis, flowListYaxis)
