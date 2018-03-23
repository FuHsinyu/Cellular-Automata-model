from CAhw1 import Model
import numpy as np
import scipy.misc as smp
import matplotlib.pyplot as plt
import matplotlib as mpl
import random
from matplotlib import colors


class CAmodel(Model):
    def __init__(self, range, base, rule, initRow, systemSize):
        #1,2,r,initRow change row to row
        Model.__init__(self)
        self.k = base
        self.r = range
        self.rule = self.build_rule_set(rule, base, systemSize)
        self.N = systemSize
        self.initRow = initRow
        self.currentRow = initRow
        self.rowLength = len(self.currentRow)
        self.ruleLength = len(self.rule)
        #self.kn = pow(self.k, self.N)

    def binToDec(self, val, base):
        decVal = 0
        valSize = len(val)
        for i in val:
            valSize = valSize - 1
            decVal = decVal + pow(base, valSize) * i
        return decVal

    def step(self):
        start = 0
        end = start + self.N
        prevState = self.currentRow
        self.currentRow = []
        prevState.insert(0, prevState[-1])
        prevState.append(prevState[1])
        while start < self.rowLength:
            preSizeVal = prevState[start:end:1]
            self.currentRow.append(
                self.rule[self.ruleLength - self.binToDec(preSizeVal, self.k) -
                          1])
            start += 1
            end += 1
        return self.currentRow

    def draw_hw4(self, xAxis, yAxis):
        plt.rcdefaults()
        plt.plot(xAxis, yAxis, "r^")
        plt.grid(True)
        #plt.yscale("log")
        plt.xlabel('Density')
        plt.ylabel('Flow')
        plt.title('the fundamental diagram of traffic flow')
        plt.show()

    def draw_hw4_bin(self, yAxis):
        plt.rcdefaults()
        #cmap = colors.ListedColormap(['white', 'blue', 'grey'])
        #norm = colors.BoundaryNorm(bounds, cmap.N)
        plt.imshow(yAxis, interpolation='nearest')  #, cmap=cmap, norm=norm)
        plt.grid(True)
        #plt.yscale("log")
        plt.xlabel('Density')
        plt.ylabel('Flow')
        plt.title('the fundamental diagram of traffic flow')
        plt.show()

    def draw_hw4_criticalDensity_T(slef, criticalDenList, TList):
        plt.rcdefaults()
        #objects = []
        #xtickList = range(256)
        #xAxis = np.arange(start=0, stop=len(cycleLenList), step=1)  #
        #print(xAxis)
        plt.plot(
            TList,
            criticalDenList,
            #align='center',
            #alpha=0.5,
            "r^",
            #ms=10,
            #color="blue",
            #edgecolor="yellow",
            #bottom=0
        )
        #plt.xticks(xAxis, xtickList)
        plt.grid(True)
        plt.yscale("log")
        plt.xlabel('Rules')
        plt.ylabel('Cycle Length')
        plt.title('1D Cellular Automata')
        plt.show()

    def draw(self, cycleLenList):
        plt.rcdefaults()
        objects = []
        xtickList = range(256)
        xAxis = np.arange(start=0, stop=len(cycleLenList), step=1)  #
        print(xAxis)
        plt.plot(
            xAxis,
            cycleLenList,
            #align='center',
            #alpha=0.5,
            "r^",
            ms=10,
            #color="blue",
            #edgecolor="yellow",
            #bottom=0
        )
        plt.xticks(xAxis, xtickList)
        plt.grid(True)
        plt.yscale("log")
        plt.xlabel('Rules')
        plt.ylabel('Cycle Length')
        plt.title('1D Cellular Automata')
        plt.show()

    def build_rule_set(self, rule, base, systemSize):
        Length = pow(base, systemSize)
        ruleSet = list(map(int, list(np.base_repr(rule, base))))
        extraLength = Length - len(ruleSet)
        zeroList = [0] * extraLength
        ruleSet = zeroList + ruleSet
        #print(ruleSet)
        return ruleSet

    def check_rule(self, prevState_with_neighbors):
        return self.rule[binToDec(prevState_with_neighbors, self.k)]

    def get_random_table(self, loop):

        randomRuleSetDict = dict()
        #print("lambda is:", lam)

        for j in range(loop):
            lam = random.random()
            randomRuleSet = [
                0
            ] * self.ruleLength  #random table method to generate lambda
            for i in range(self.ruleLength):
                if (random.random() > (lam)):
                    randomRuleSet[i] = 1
            randomRuleSetDict[lam] = randomRuleSet
        print(randomRuleSetDict)
        return randomRuleSetDict

    def get_table_work_through(self, loop):
        randomRuleSet2 = [1] * self.ruleLength
        lam2 = 0
        randomRuleSet2Dict = dict()
        for i in range(loop):
            #print(lam2)
            #print(randomRuleSet2)
            newLam2 = random.random()
            if (newLam2 > lam2):
                for n in range(self.ruleLength):
                    if (randomRuleSet2[n] == 1):
                        randomRuleSet2[n] = random.randrange(2)
            else:
                for n in range(self.ruleLength):
                    if (randomRuleSet2[n] == 0):
                        randomRuleSet2[n] = random.randrange(2)
            randomRuleSet2Dict[lam2] = randomRuleSet2
            lam2 = newLam2
        print("dict", randomRuleSet2Dict)
        return randomRuleSet2Dict
