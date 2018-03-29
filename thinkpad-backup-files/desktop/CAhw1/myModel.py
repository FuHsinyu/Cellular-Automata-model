from CAhw1 import Model
import numpy as np
import scipy.misc as smp
import matplotlib.pyplot as plt


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

    def draw(self, cycleLenList):
        plt.rcdefaults()
        objects = []
        xAxis = np.arange(start=0, stop=len(cycleLenList), step=1)  #
        print(xAxis)
        plt.bar(
            xAxis,
            cycleLenList,
            align='center',
            alpha=0.5,
            color="silver",
            edgecolor="yellow")
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
