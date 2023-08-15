from setup import *
from vertiport import *
from depot import *
from evtol import *


seed1 = 1                   # random seed used in demandGenerator
seed2 = 100                 # random seed used in demandGenerator

# vertiport configuration:  
ini_stage = []
ini_tlof = []
ini_evs = []
for i in vertiportList:
    ini_stage.append(5)     
    ini_tlof.append(2)      
    ini_evs.append(5)       


# initialize vertiport and evtol：
for vtp in vertiportList:  
    vertiportMap[vtp] = Vertiport(vtp, dpid, ini_stage[vtp-1], ini_tlof[vtp-1])  # dpid denotes depot ID
    for i in range(ini_evs[vtp-1]):   
        newEVTOL = Evtol(eid + i, vtp) 
        vertiportMap[vtp].evtolList.append(newEVTOL)
    eid += ini_evs[vtp-1] 
    vertiportMap[vtp].stage -= ini_evs[vtp-1]


# initialize depot:
deportMap[1] = Depot(dpid, 50, 2)   
for i in range(30):   
    newEVTOL = Evtol(eid + i, dpid) 
    deportMap[1].evtolList.append(newEVTOL)
eid += 30
deportMap[1].stage -= 30


# for simulation platform performance analysis:
svdList = {}              # record how many user being served
usvdList = {}             # record how many user not being served
stat_evtols = {}          # statistic the number of available evtol in simulation process
stat_stage = {}           # statistic the number of available stage for charging in simulation process
stat_takeoff = {}         # statistic the number of available pad for taking off in simulation process
stat_land = {}            # statistic the number of available pad for landing in simulation process

for i in vertiportList:
    svdList[i] = []
    usvdList[i] = []
    stat_evtols[i] = []
    stat_stage[i] = []     
    stat_takeoff[i] = []
    stat_land[i] = []

