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


def get_critical_density_flow(densityList, flowVehicleList):
    #resultDict = dict()
    maxFlowVehicle = max(flowVehicleList)
    for i in range(len(densityList)):
        #resultDict[densityList[i]]=flowVehicleList[i]
        if (maxFlowVehicle == flowVehicleList[i]):
            break
    return densityList[i], flowVehicleList[i]


r = 1  #range
k = 2  #base
systemSize = r * 2 + 1
initRowLength = 100
densityListXaxis = list()
flowListYaxis = list()
densityRange = np.linspace(0, 1, 51)  #set intervel of densityList
rule = 184
criticalDenList = list()
TList = [1000]  #set TList as T
#For Q6
#TList = range(10, 60, 1)
for T in TList:  # T
    initStateTimes = 10  # R
    #densityRange = [0.4,[0.9]] # for Qestion 2
    initRow = [0] * initStateTimes
    flowVehicleList = [0] * initStateTimes
    for density in densityRange:
        for R in range(initStateTimes):
            initRow[R] = initial_row(initRowLength, density)
            model = CAmodel(r, k, rule, initRow[R], systemSize)
            runTime = 0  #run times
            flowVehicle = 0
            while runTime < T:  #T
                currentRow = tuple(model.currentRow)
                runTime += 1
                currentRow = model.step()
                if (currentRow[0] == 1):
                    if (currentRow[1] == 0):
                        flowVehicle += 1
            flowVehicleList[R] = flowVehicle
        densityListXaxis.append(density)
        flowListYaxis.append(np.mean(flowVehicle))
#For Q6 get critical density and flow figure
#    criticalDen, criticalFlow = get_critical_density_flow(
#        densityListXaxis, flowListYaxis)
#    print("critical density is:", criticalDen, "critical flow is:",
#          criticalFlow)
#    criticalDenList.append(criticalDen)
#model.draw_hw4_criticalDensity_T(criticalDenList, TList)

#draw normal density-flow figure
model.draw_hw4(densityListXaxis, flowListYaxis)
