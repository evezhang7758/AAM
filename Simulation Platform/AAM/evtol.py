from setup import *

class Evtol:

    # time consumption in differnet phase (min)
    taxiOut = 2              # time spent on taxi out
    taxiIn = 2               # time spent on taxi in
    takeOff = 1              # time spent on take off
    land = 1                 # time spent on land
    unload = 1               # time spent on unloading

    # energy consumption on differnet phase (soc) in a minute
    soc_takeOff = 0.05
    soc_cruise = 0.01
    soc_hover = 0.03
    soc_land = 0.05
    soc_recharge = 0.04

    # required minimal battery 
    reserve = 0.2  

    def __init__(self, id, sid):

        self.id = id
        self.sid = sid           # source id
        self.did = -1            # denote vertiport's id. -1 denotes that evtol is on 表示该evtol目前处于空闲状态，还没接客
        self.destination = vertiportMap[sid] if sid < 1000 else deportMap[sid-1000]

        self.speed = 150         # mph
        self.battery = 140       # kWh
        self.capacity = 4        # evtol can contain up to 4 users
       
        self.distance = 0        # flight distance
        self.cruiseTime = 0      # flight time
        self.soc = 1             # current battery
        self.status = 0          # evtol's initial status

        self.userList = []       # loaded users
        self.clock = 0           # min
        self.v2v = True          # True denotes from vertiport to vertiport, False denotes vertiport to depot

        # performance analysis variable:
        self.wait_takeOff = 0     
        self.wait_land = 0        
        self.wait_stage = 0


    # check whether evtol is full or not
    def notFull(self):
        return self.capacity > len(self.userList)

    
    # based on user's destination, check whether evtol's battery is enough for the next flight
    def isSocOK(self, distance, distanceToDepot):
        self.distance = distance
        # 考虑了hover在半空2min需要的energy消耗，若hover超过了2min使得电量低于reserve，就需要紧急迫降
        return self.soc - self.reserve - (distanceToDepot * 60 / self.speed) * self.soc_cruise >= (self.distance * 60 / self.speed) * self.soc_cruise + self.soc_takeOff + self.soc_land  + 2 * self.soc_hover
    
    # update evtol's distance and cruise time once it gets the first user
    def createRoute(self, distance):
        self.distance = distance
        self.cruiseTime = self.distance * 60 / self.speed   # min
        

    # update evtol's status during simulation process
    def updateStatus(self):
        if self.status < 8:
            self.status += 1
        else: 
            self.status = 0   


    # update loaded passengers' waiting time
    def load(self):
        for u in self.userList:
            u.wait_other += 1

    
    # update evtol's wait time for take off
    def waitForTakeOff(self):
        self.wait_takeOff += 1
        for u in self.userList:
            u.wait_takeOff += 1  


    # update evtol's wait time for landing
    def waitForLand(self):
        self.wait_land += 1
        for u in self.userList:
            u.wait_land += 1  


    def waitForStage(self):
        self.wait_stage += 1

    
    # when evtol arrives to destination, do the following things
    def clear(self):               
        self.userList = []
        self.did = -1
        self.distance = 0
        self.cruiseTime = 0


    