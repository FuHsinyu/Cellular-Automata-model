import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

start = time.clock()  #Program excution time
ims = []
fig = plt.figure()
data = np.ones((150, 150))


def dataInit():
    partyVotes = np.random.choice(
        [0, 1], [150, 150, 3], replace=True,
        p=[0.5, 0.5])  # 150*150 cells, 0 is supporting party 0, 1 is party1
    readNews = np.random.choice(
        [0, 1], [150, 150, 1], replace=True,
        p=[0.7, 0.3])  #Distribution of people who read political medias
    tolerance = np.random.choice(
        [5, 6, 7, 8], [150, 150, 1], replace=True, p=[0.4, 0.3, 0.2, 0.1]
    )  # How taugh for a person to change his opinion: level 5,6,7,8 from easy to difficult
    for x in range(partyVotes.shape[0]):
        for y in range(partyVotes.shape[1]):
            partyVotes[x][y][1] = readNews[x][y]
            partyVotes[x][y][2] = tolerance[x][y]
    return partyVotes


def runMajorityWin(partyVotes):
    for x in range(1, partyVotes.shape[0] - 1):
        for y in range(1, partyVotes.shape[1] - 1):
            data[x][y] = partyVotes[x][y][0]
            opinionChange(partyVotes, x, y)
    #print('data', data)


def opinionChange(partyVotes, x,
                  y):  #0(voting for party 0) -> 1(party 1) or 1 -> 0
    if partyVotes[x][y][0] == 0:
        if sumOfNeighbors(
                partyVotes, x, y
        ) >= partyVotes[x][y][2]:  # if the num of positive neighbors > tolerance, opinion changed
            partyVotes[x][y][0] = 1
    else:
        if 9 - sumOfNeighbors(
                partyVotes, x, y
        ) >= partyVotes[x][y][2]:  # if the num of negative neighbors > tolerance, opinion changed
            partyVotes[x][y][0] = 0


def sumOfNeighbors(partyVotes, x, y):  #calculate the sum of neighbours
    sum1 = 0
    sum2 = 0
    sum3 = 0
    firRowNeighbors = partyVotes[x - 1][y - 1:y + 2]
    secRowNeighbors = partyVotes[x][y - 1:y + 2]
    thrRowNeighbors = partyVotes[x + 1][y - 1:y + 2]

    for x in range(firRowNeighbors.shape[1]):
        sum1 += firRowNeighbors[x][0]
        sum2 += secRowNeighbors[x][0]
        sum3 += thrRowNeighbors[x][0]
    sumOfNeighbors = sum((sum1, sum2, sum3))
    return sumOfNeighbors


def mediaPromotion():
    pass


def animationDraw():  #Save video to working dir
    plt.legend()
    plt.axis('off')
    im_ani = animation.ArtistAnimation(
        fig, ims, interval=700, repeat_delay=2000, blit=True)
    plt.show()
    im_ani.save('votingmodel.mp4', writer=animation.FFMpegWriter())


days = 100
partyVotes = dataInit()
for day in range(days):
    runMajorityWin(partyVotes)
    ims.append((plt.imshow(data, cmap='YlOrBr', interpolation='nearest'), ))
print(partyVotes)
animationDraw()
minElapsed = (time.clock() - start) / 60
print(minElapsed, "mins are consumed")