# Explanation:

# The depot is responsible for managing a group of vertiports within its assigned region.

# depot also has a unique ID number, which can be used to identify a depot based on the DepotMap. In Tampa Bay Area, only one depot is considered. If more depot are needed, it's easy to expand.

# At the initial stage, each depot is equipped with 50 stages, 15 eVTOLs, 1 pad for takeoff, and 1 pad for landing.

# The reason why Takeoff and Landing Pads (TLOF) are divided into two parts is to reduce the possibility of multiple eVTOLs attempting to use the same TLOF.


from setup import *


class Depot:

    def __init__(self, id, stage, tlof):  
        self.id = id
        self.stage = stage             # available stage for charging
        self.takeoffPad = tlof-1       # available pad for taking off
        self.landPad = 1               # available pad for landing

        self.evtolList = []            # evtol in the deppot 
        self.arrivalList = []          # Record eVTOLs are flying to this depot 


    def requestEvtol(self, ev, did):
        ev.did = did
        ev.destination = vertiportMap[did]
        ev.createRoute(vertiToDepot[did-1])
        ev.status = 1