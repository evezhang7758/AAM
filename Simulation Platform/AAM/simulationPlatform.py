from setup import *
from initialization import *
from demandGenerator import *
from assignUserToEvtol import *
from updateEvtolInVertiport import *
from updateEvtolInDepot import *


def  main(uid, seed1, seed2, stateTimer):

    for slot in range(slots):   

        # predict the destination & arrival time of users in one slot. create and add them into vertiport
        # if slot >= 90, jump to the for loop and don't execute predictUserArrivalTimeAndDest()
        if slot < slotForUser:
            interval = time_slot * slot + 6 * 60   
            uid = predictUserArrivalTimeAndDest(vertiportMap, slot, interval, arrivalMatrix, uid, seed1, seed2)
            seed1 += 10000               
            seed2 += 10000 

        # update simulation platform in each minute
        for t in range(time_slot):
            stateTimer += 1

            # update evtol from vertiport to vertiport
            for i in vertiportList:
                usvdList[i] = usvdList[i] + assignUserToEvtol(i, vertiportMap, deportMap, stateTimer)    # assign user to an available evtol
                updateEvtolResult = updateEvtolInVertiport1(i, vertiportMap)
                svdList[i] = svdList[i] + updateEvtolResult["served"]

            # update evtol from vertiport to depot
            for i in vertiportList:
                updateEvtolInVertiport2(i, vertiportMap, deportMap)

                # for performance analysis
                stat_evtols[i].append(len([e for e in vertiportMap[i].evtolList if e.status == 0 or e.status == 1 or e.status == 8]))
                stat_stage[i].append(vertiportMap[i].stage)
                stat_takeoff[i].append(vertiportMap[i].takeoffPad)
                stat_land[i].append(vertiportMap[i].landPad)

            # update evtols in depot
            for j in range(1, len(deportMap)+1):
                updateEvtolInDepot(j, deportMap, vertiportMap)

    
    return svdList, usvdList, stat_evtols, stat_stage, stat_takeoff, stat_land

