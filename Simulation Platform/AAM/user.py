# This class is for passenger. 

# The simulation system will save the information of passenger, such as their id, destination, arrival time and the evtol they take.
# When no available evtol in the vertiport, a boolean variable, hasAssiged, is used to denotes whether a waiting passenger get a requested evtol.


class User:
    # __slots__ = ['id','destination','arriveTime','waitOutOfVehicle','waitInVehicle','eid','holdTimeForTaxiOut','holdTimeForTaxiIn','holdTimeForLand']
    
    def __init__(self, id, did, arrivalTime):
        self.id = id                       # user id                   
        self.eid = -1                      # evtol id (-1 if not assigned yet)
        self.did = did                     # the id of the location where the user wants to go
        self.arrivalTime = arrivalTime     # the time at which the user arrives at the starting location
        self.hasAssigned = False           # FALSE denotes to fail to request an available evtol form depot; TRUE denotes there is incoming evtol

        # system performance analysis：
        self.wait_evtol = 0                # the time spent waiting for an available EVTOL
        self.wait_other = 0                # the time spent waiting for other passengers
        self.wait_takeOff = 0
        self.wait_land = 0
        self.wait_unload = 0