from setup import *

def assignUserToEvtol(i, vertiportMap, deportMap, stateTimer):

    # record user not being served
    unserved_user = []         

    # Traverse users who arrived before the current time.
    users = [u for u in vertiportMap[i].userList if u.arrivalTime <= stateTimer]

    if len(users) > 0:

        # Check the eVTOL in the following statuses in turn.
        checkList = [e for e in vertiportMap[i].evtolList if e.status == 1]
        checkList += [e for e in vertiportMap[i].evtolList if e.status == 0]
        checkList += [e for e in vertiportMap[i].evtolList if e.status == 8]

        for u in users:
            
            for e in checkList:

                # Check the eVTOL in the load status (==1). If it meets the following conditions, assign the user to it.
                if e.status == 1 and e.did == u.did and e.notFull() and ((len(e.userList) == 1 and e.userList[0].wait_other < los1) or (len(e.userList) > 1 and e.userList[0].wait_other < los1 and e.userList[-1].wait_other < los2)):
                    vertiportMap[i].userList.remove(u)
                    e.userList.append(u)
                    u.eid = e.id
                    if u.did in vertiportMap[i].waitMap:  
                        vertiportMap[i].updateWaitMap(u.did, vertiportMap[i].waitMap.get(u.did)-1)

                    # data collection for model simulation:
                    collectUserDate(u.id, i, u.eid, u.wait_evtol)
                    break

                # Check the eVTOLs in the ready status (==0). If there are available eVTOLs, assign the user to one of them.
                if e.status == 0:   
                    vertiportMap[i].userList.remove(u)
                    e.userList.append(u)
                    u.eid = e.id
                    e.did = u.did
                    e.destination = vertiportMap[e.did]
                    e.createRoute(distanceMatrix[i-1][u.did-1])
                    e.updateStatus()
                    if u.did in vertiportMap[i].waitMap:  
                        vertiportMap[i].updateWaitMap(u.did, vertiportMap[i].waitMap.get(u.did)-1)
                   
                    # data collection for model simulation:
                    collectUserDate(u.id, i, u.eid, u.wait_evtol)
                    break

                # otherwise, check evtol in charge status(==8)
                if e.status == 8 and e.isSocOK(distanceMatrix[i-1][u.did-1], vertiToDepot[u.did-1]):   
                    vertiportMap[i].userList.remove(u)
                    e.userList.append(u)
                    u.eid = e.id
                    e.did = u.did
                    e.destination = vertiportMap[e.did]
                    e.createRoute(distanceMatrix[i-1][u.did-1])
                    e.status = 1
                    if u.did in vertiportMap[i].waitMap:  
                        vertiportMap[i].updateWaitMap(u.did, vertiportMap[i].waitMap.get(u.did)-1)
                    
                    # data collection for model simulation:
                    collectUserDate(u.id, i, u.eid, u.wait_evtol)
                    break
            
            # if a passenger fail to be assigned, add his waiting time
            if u.eid == -1: 
                u.wait_evtol += 1

                # violate LoS3
                if u.wait_evtol >= 15:
                    vertiportMap[i].userList.remove(u)
                    unserved_user.append(u)
                    if u.did in vertiportMap[i].waitMap:  
                        vertiportMap[i].updateWaitMap(u.did, vertiportMap[i].waitMap.get(u.did)-1)

                # wait time is no less than 5 min, request an evtol from depot
                elif u.wait_evtol > 5:   
                    if u.hasAssigned == False:
                        depot = deportMap[vertiportMap[i].dpid-1000]  
                        avail_evtols = [e for e in depot.evtolList if e.status == 0]

                        if u.did in vertiportMap[i].waitMap: 
                            u.hasAssigned = True
                            vertiportMap[i].waitMap.update({u.did:vertiportMap[i].waitMap.get(u.did)+1})

                            # If there are more than a multiple of 4 users waiting for the same eVTOL, request one more.
                            if vertiportMap[i].waitMap.get(u.did) % 4 == 1:  
                                if len(avail_evtols) > 0:
                                    depot.requestEvtol(avail_evtols[0], i)
                                else:
                                    u.hasAssigned = False
                                    vertiportMap[i].waitMap.update({u.did:vertiportMap[i].waitMap.get(u.did)-1})


                        elif len(avail_evtols) > 0:  
                            depot.requestEvtol(avail_evtols[0], i)
                            u.hasAssigned = True
                            vertiportMap[i].waitMap.update({u.did : 1})


    return unserved_user