import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import cdist # for euclidean distance calculation
from setup import vertiportList


data = np.load('../inputs/v_coords.npy')
x = [i[0] for i in data]
y = [i[1] for i in data]
center = sum(x)/len(x), sum(y)/len(y)


def depotDistance():
    vvdist = cdist(np.append(data, values=np.array([[center[0], center[1]]]), axis=0), np.append(data, values=np.array([[center[0], center[1]]]), axis=0), 'euclidean')  # 计算点与点之间的欧式距离
    vvdist = np.around(vvdist/1609, 2)


# vertiToDepot list contains distances between vertiports and the depot
def neigborVertiport():
    vertiToDepot = np.load('../inputs/verti_depot_dist.npy')
    dist = np.load('../inputs/dist.npy')

    # 设想：为每个机场设置附近的机场list，用来提高evtol转移的效率。list按照距离该vertiport的距离由近到远
    near_vtp= {}
    for i in vertiportList:
        near_vtp[i] = []

    for row, valueList in enumerate(dist):
        tmp = {}
        for col, val in enumerate(valueList):
            if((val <= vertiToDepot[row] or val <= 10) and val != 0):
                tmp[col+1] = val
        if(len(tmp) > 0):
            tmp = sorted(tmp.items(), key=lambda kv:(kv[1], kv[0]))
            for i in tmp:
                near_vtp[row+1].append(i[0])



def depotVisualization():
    params = {
        'figure.figsize': '15, 8'   # '''adjust Windows size'''
    }
    plt.rcParams.update(params)

    plt.scatter(x, y)
    for i in range(1, 31):
        plt.annotate(i, xy=(x[i-1], y[i-1]), xytext=(x[i-1]+0.1, y[i-1]+0.1))

    plt.plot(center[0], center[1], marker='o', color = 'red')
    plt.annotate(
    "center", xy=center, xytext=(-10, 15),
    textcoords='offset points', ha='right', va='bottom',
    bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    plt.show()