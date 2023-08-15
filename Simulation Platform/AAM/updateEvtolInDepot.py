# update evtols in depot or evtol from depot to vertiport
def updateEvtolInDepot(id, deportMap, vertiportMap):

    dpt = deportMap[id]        

    if len(dpt.evtolList) > 0:
        for e in dpt.evtolList:

            # ready
            if e.status == 0:   
                continue

            elif e.status == 1:  
                e.destination.arrivalList.append(e)
                e.updateStatus()
                dpt.stage += 1   
            
            # taxi out
            elif e.status == 2:   
                e.clock += 1
                if e.clock >= e.taxiOut:
                    if dpt.takeoffPad == 1:
                        dpt.takeoffPad -= 1
                        e.clock = 0
                        e.updateStatus()
                    else:
                        e.clock += 1
                        e.waitForTakeOff()

            # take off
            elif e.status == 3:   
                e.soc -= e.soc_takeOff
                dpt.takeoffPad += 1  
                e.updateStatus()

            # cruise
            elif e.status == 4:   
                if e.cruiseTime <= 0:
                    if e.destination.landPad == 1:   
                        e.updateStatus()
                        e.destination.landPad -= 1
                    else:
                        e.soc -= e.soc_hover
                        e.waitForLand()
                else:
                    e.cruiseTime -= 1
                    e.soc -= e.soc_cruise

            # land
            elif e.status == 5:   
                e.soc -= e.soc_land
                e.destination.landPad += 1   
                e.updateStatus()

            # taxi in
            elif e.status == 6:   
                e.clock += 1
                if e.clock >= e.taxiIn:
                    if e.destination.stage == 1:
                        e.destination.stage -= 1
                        dpt.evtolList.remove(e)
                        e.destination.arrivalList.remove(e)
                        e.destination.evtolList.append(e)
                        e.sid = e.did
                        e.clear()
                        e.v2v = True
                        e.status = 0
                        e.clock = 0
                    else:
                        e.clock += 1
                        e.waitForStage()

            # recharge
            elif e.status == 8:   
                e.soc += e.soc_recharge
                if e.soc >= 1:
                    e.soc = 1
                    e.updateStatus()               