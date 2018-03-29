import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
#   Human   0 =Dead         Mosquitoes  0   =Dead/None Mos
#           1 =Suscepitable             4   =No hungry, infected
#           2 =Infected                 8   =No hungry, iminfected
#           3 =Immune                   12  =Hungry, infectd
#                                       16  =Hungry, iminfected
start = time.clock()

#Parameters
proOfHumanInfected = 0.3  #suscepitable human + infected mos, the pro of Human
proOfMosBecomeInfected = 0.3  #the pro of Mos bite human. infected human, iminfected mos,
deathRateOfMos = 0.0005
deathRateOfInfectedHuman = 0.0005  #Also born a baby
bornRateOfMos = 0.05
immuneRate = 0.1

#Non parameters
almostInfetedManCount = 0
infetedManCount = 0

#recoverRate
pararametrDict = {
    "proOfHumanInfected": proOfHumanInfected,
    "proOfMosBecomeInfected": proOfMosBecomeInfected,
    "deathRateOfMos": deathRateOfMos,
    "deathRateOfInfectedHuman": deathRateOfInfectedHuman,
    "bornRateOfMos": bornRateOfMos,
    "immuneRate": immuneRate
}
#map = [[[1, 12], [1, 8], [1, 12], [3, 12],
#        [0, 12]], [[1, 8], [4, 8], [0, 12], [2, 12],
#                   [2, 12]], [[2, 12], [2, 12], [3, 16], [1, 12], [2, 12]],
#       [[0, 4], [1, 4], [0, 12], [1, 12], [0, 0]], [[3, 12], [0, 16], [1, 12],
#                                                    [4, 8], [2, 16]]]

#universe[1:6, 1:6] = map
#universeList = np.ndarray.tolist(universe)

humanDist = np.random.choice(
    [0, 1, 2, 3], [100, 100, 2], replace=True, p=[0.05, 0.8, 0.1, 0.05])
mosDis = np.random.choice(
    [0, 4, 8, 12, 16], [100, 100, 1],
    replace=True,
    p=[0.2, 0.2, 0.2, 0.2, 0.2])
for x in range(mosDis.shape[0]):
    for y in range(mosDis.shape[1]):
        humanDist[x][y][1] = mosDis[x][y][0]
universe = np.copy(humanDist)
universeList = np.ndarray.tolist(universe)
ims = []
fig = plt.figure()


def humanInfect(x, y):
    for z in range(1, len(universe[x][y])):
        sumHumanMos = universe[x][y][0] + universe[x][y][z]
        if (sumHumanMos == 13):  #weakman + hungry infect mos
            if (np.random.rand() < pararametrDict["proOfHumanInfected"]):
                universe[x][y][0] = 2  #infectedman
        if (universe[x][y][0] in range(
                1, 4)):  #p chance to die and born another people
            if (np.random.rand() < pararametrDict["deathRateOfInfectedHuman"]):
                if (np.random.rand() < 0.5):
                    universe[x][y][0] = 1
                    #death is equal to born sucespitable
                else:
                    #print(pararametrDict["deathRateOfInfectedHuman"])
                    universe[x][y][0] = 3
                    #death is equal to born immune


def mosquitoeState(x, y):
    for z in range(1, len(universe[x][y])):
        sumHumanMos = universe[x][y][0] + universe[x][y][z]
        if (np.random.rand() < pararametrDict["deathRateOfMos"]):
            universe[x][y][z] = 0
        if (sumHumanMos == 18):  #infectman + hungry iminfect mos
            if (np.random.rand() < pararametrDict["proOfMosBecomeInfected"]):
                universe[x][y][z] = 12  #infectedmos
        elif (universe[x][y][z] == 0):  #Chance to born Mos
            if (np.random.rand() < pararametrDict["bornRateOfMos"]):
                universe[x][y][z] == 16  #Mos born to be Hungry and iminfect


def mosquitoeWalk(x, y):
    #global universeList
    for z in range(1, len(universe[x][y])):
        quarterList = np.random.randint(0, 5, 1)
        if (quarterList[0] == 0):
            if (universeList[x - 1][y][-1] == 0):
                universeList[x - 1][y][-1] = universe[x][y][z]
            else:
                universeList[x - 1][y].append(universe[x][y][z])
        elif (quarterList[0] == 1):
            if (universeList[x][y + 1][-1] == 0):
                universeList[x][y + 1][-1] = universe[x][y][z]
            else:
                universeList[x][y + 1].append(universe[x][y][z])
        elif (quarterList[0] == 2):
            if (universeList[x + 1][y][-1] == 0):
                universeList[x + 1][y][-1] = universe[x][y][z]
            else:
                universeList[x + 1][y].append(universe[x][y][z])
        elif (quarterList[0] == 3):
            if (universeList[x][y - 1][-1] == 0):
                universeList[x][y - 1][-1] = universe[x][y][z]
            else:
                universeList[x][y - 1].append(universe[x][y][z])
        else:  #mos did not move to another cell
            continue
        universeList[x][y][z] = 0
    return universeList


def pltDraw():
    plt.imshow(data, cmap='YlOrBr')
    plt.show()


def animationDraw():
    plt.legend()
    plt.axis('off')
    im_ani = animation.ArtistAnimation(
        fig, ims, interval=700, repeat_delay=2000, blit=True)
    plt.text(
        0,
        0,
        'White = dead/none Gold = Suscepitable Orange=Infected Brown=immune',
        color="white",
        bbox={
            'facecolor': 'black',
            'alpha': 0.5,
            'pad': 10
        })
    plt.show()
    im_ani.save('universe.mp4', writer=animation.FFMpegWriter())


def statisticDraw():
    plt.ylim([0, 1])
    plt.xlabel("Time")
    plt.ylabel("Prevalence")
    #plt.title("")
    plt.grid()
    plt.plot(prevalenceResultInPercentage, "r^")
    plt.show()
    plt.savefig("prevalenceResults")


loops = 200
prevalenceResultInPercentage = list()
for loop in range(loops):
    prevalence = 0
    infetedManCount = 0
    for x in range(1, universe.shape[0] - 1):
        for y in range(1, universe.shape[1] - 1):
            humanInfect(x, y)
            mosquitoeState(x, y)
            universeList = np.ndarray.tolist(universe)
            mosquitoeWalk(x, y)
    universe = np.copy(universeList)
    #Save data and visulize data
    data = np.zeros((len(universe), len(universe[1])))
    for i in range(0, len(universe)):
        for j in range(0, len(universe[1])):
            data[i][j] = universe[i][j][0]
            if (data[i][j] == 2):
                infetedManCount += 1
    prevalence = infetedManCount / 10000
    prevalenceResultInPercentage.append(prevalence)
    #if (loop == (int(loops * 9 / 10))):
    #    if (data[i][j] == 2):
    #        almostInfetedManCount += 1
    #if (loop == (loops - 1)):  #At last loop, count the prevalence
    #    if (data[i][j] == 2):
    #        infetedManCount += 1
    #ims.append((plt.imshow(data, cmap='YlOrBr', interpolation='nearest'), ))
#print('Almost prevalence', almostInfetedManCount / 10000)
#print('prevalence', infetedManCount / 10000)
#animationDraw()
statisticDraw()
#excution time in mins
minElapsed = (time.clock() - start) / 60
print(minElapsed, "mins are consumed")
