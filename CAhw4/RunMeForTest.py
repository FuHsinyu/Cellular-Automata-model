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
rowDraw = []
T = 1000
densityRange = np.linspace(0, 1, 101)
#densityRange = [0.4, 0.9]
for density in densityRange:
    initRow = initial_row(initRowLength, density)
    rule = 184
    model = CAmodel(r, k, rule, initRow, systemSize)
    #def __init__(self, range, base, rule, initRow, systemSize):
    runTime = 0  #run times
    flowVehicle = 0
    #flowTime = 50
    while runTime < 1000:
        currentRow = tuple(model.currentRow)
        runTime += 1
        currentRow = model.step()
        if (currentRow[0] == 1):
            if (currentRow[1] == 0):
                flowVehicle += 1
        #print("current row:", currentRow)
        rowDraw.append(currentRow)
    densityListXaxis.append(density)
    flowListYaxis.append(flowVehicle)

#np.floor(np.array(rowDraw))
#print(densityListXaxis, flowListYaxis)
#print(rowDraw)

#model.draw_hw4_bin(rowDraw)
model.draw_hw4(densityListXaxis, flowListYaxis)
