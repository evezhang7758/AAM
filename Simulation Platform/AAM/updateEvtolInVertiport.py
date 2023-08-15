from setup import *

# Update eVTOL flying from one vertiport to another vertiport

def updateEvtolInVertiport1(i, vertiportMap):

    served_user = []           
    statUserInEV= []                   # statistic how many passengers are in evtol
    waitTakeOffList = []               # wait time for an available pad for taking off
    waitLandList = []                  # wait time for an available pad for landing
    waitStageList = []                 # wait time for an available stage pad

    origi_vtp = vertiportMap[i]        # origi_vtp: original vertiport
    evtols = [e for e in origi_vtp.evtolList if e.v2v == True]

    if len(evtols) > 0:
        for e in evtols:

            # ready
            if e.status == 0:          
                continue

            # load
            elif e.status == 1:        
                e.load()
                if e.notFull() == False or e.userList[0].wait_other >= los1 or (len(e.userList) > 1 and e.userList[-1].wait_other >= los2):
                    e.destination.arrivalList.append(e)  
                    e.updateStatus()
                    origi_vtp.stage += 1   

            # taxi out
            elif e.status == 2:   
                e.clock += 1
                if e.clock >= e.taxiOut:     
                    if origi_vtp.takeoffPad == 1:
                        e.clock = 0
                        e.updateStatus()  
                        origi_vtp.takeoffPad -= 1
                    else:
                        e.waitForTakeOff()

            # take off   
            elif e.status == 3:   
                e.soc -= e.soc_takeOff
                e.updateStatus()
                origi_vtp.takeoffPad += 1  

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
                e.updateStatus()
                e.destination.landPad += 1 
            
            # taxi in
            elif e.status == 6:   
                e.clock += 1
                if e.clock >= e.taxiIn:
                    if e.destination.stage > 0:
                        e.clock = 0
                        e.updateStatus()
                        e.destination.stage -= 1
                    else:
                        e.waitForStage()
            
            # unload
            elif e.status == 7:   
                for u in e.userList:
                    served_user.append(u)
                    inVehicleWait.append(u.wait_other)
                
                statUserInEV.append(len(e.userList))
                waitTakeOffList.append(e.wait_takeOff)
                waitStageList.append(e.wait_stage)
                waitLandList.append(e.wait_land)

                origi_vtp.evtolList.remove(e)
                e.destination.arrivalList.remove(e)
                e.destination.evtolList.append(e)
                e.sid = e.did
                e.clear()
                e.updateStatus()

            # charge
            elif e.status == 8:   
                e.soc += e.soc_recharge
                if e.soc >= 1:
                    e.soc = 1
                    if vertiportMap[e.sid].landPad == 0:
                        e.did = vertiportMap[e.sid].dpid
                        e.destination = deportMap[e.did-1000]
                        e.createRoute(vertiToDepot[e.sid-1])
                        e.v2v = False
                        e.status = 1
                        vertiportMap[e.sid].stage += 1
                
    return {"served": served_user, "occu": statUserInEV, "takeoff": waitTakeOffList, "unload": waitStageList, "landing": waitLandList}



# Update eVTOL flying from one vertiport to depot
def updateEvtolInVertiport2(i, vertiportMap, deportMap):

    origi_vtp = vertiportMap[i]        # origi_vtp: original vertiport
    dest_dpt = deportMap[vertiportMap[i].dpid - 1000]       

    evtols = [e for e in origi_vtp.evtolList if e.v2v == False]

    if len(evtols) > 0:
        for e in evtols:

            # ready
            if e.status == 1:
                dest_dpt.arrivalList.append(e)
                e.updateStatus()

            # taxi out
            elif e.status == 2:   
                e.clock += 1
                if e.clock >= e.taxiOut:     
                    if origi_vtp.takeoffPad == 1:
                        e.clock = 0
                        e.updateStatus()
                        origi_vtp.takeoffPad -= 1
                    else:
                        e.waitForTakeOff()

            # take off           
            elif e.status == 3:   
                e.soc -= e.soc_takeOff
                e.updateStatus()
                origi_vtp.takeoffPad += 1  

            # cruise
            elif e.status == 4:   
                if e.cruiseTime <= 0:
                    if dest_dpt.landPad == 1:
                        e.updateStatus()
                        dest_dpt.landPad -= 1
                    else:
                        e.soc -= e.soc_hover
                        e.waitForLand()
                else:
                    e.cruiseTime -= 1
                    e.soc -= e.soc_cruise
            
            # land
            elif e.status == 5:   
                e.soc -= e.soc_land
                e.updateStatus()
                dest_dpt.landPad += 1
            
            # taxi in
            elif e.status == 6:   
                e.clock += 1
                if e.clock >= e.taxiIn:
                    if dest_dpt.stage >= 1:
                        origi_vtp.evtolList.remove(e)  
                        dest_dpt.arrivalList.remove(e)
                        dest_dpt.evtolList.append(e)   
                        e.clock = 0
                        e.sid = vertiportMap[i].dpid
                        e.clear()
                        e.status = 8
                        dest_dpt.stage -= 1
                    else:
                        e.waitForStage()