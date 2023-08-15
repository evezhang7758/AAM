# Explanation:

# Each vertiport has a unique ID number, which can be used to identify a vertiport based on the VertiportMap.

# At the initial stage, each vertiport is equipped with 5 stages, 5 eVTOLs, 1 pad for takeoff, and 1 pad for landing.

# The reason why Takeoff and Landing Pads (TLOF) are divided into two parts is to reduce the possibility of multiple eVTOLs attempting to use the same TLOF.

# waitMap records passengers who wait for more than 5 minutes and have requested an evtol from depot.
 

class Vertiport:

    def __init__(self, id, dpid, stage, tlof):  
        self.id = id
        self.dpid = dpid                  # depot id
        self.stage = stage                # available stage for charging
        self.takeoffPad = tlof-1          # available pad for taking off
        self.landPad = 1                  # available pad for landing
        
        self.evtolList = []               # evtol in vertiport
        self.userList = []                # arriving passenger in vertiport
        self.arrivalList = []             # Record eVTOLs are flying to this vertiport 
        self.waitMap = {}                 # key is combination of destination vertiport id and nth ，value denote how many waiting passenger

    
    def updateWaitMap(self, did, val):
        self.waitMap.update({did : val})
        if self.waitMap.get(did) == 0:
            self.waitMap.pop(did)
