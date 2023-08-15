import numpy as np
import pandas as pd

# simulation background settings:

time_slot = 15                 # time slot T (min) for user generation
startTime = 60*6                # simulation start time
endTime = 60*21                 # simulation end time
slots = 64                      # the first 90 slots from 6am to 9pm will generate user, the last 6 slots from 9pm to 10pm don't generate user
slotForUser = (endTime - startTime) / time_slot
print(slotForUser)
los1 = 10                       # first passenger's in-vehicle waiting time threshold
los2 = 5                        # last passenger's in-vehicle waiting time threshold
los3 = 15                       # out-of-vehicle waiting time threshold
vertiportList = range(1, 31)    # indexs for vertiports: 1,2,3,...,29,30
vertiportMap = {}               # key is vertiport index, value is vertiport
deportMap = {}                  # key is depot index, value is depot
eid = 1                         # evtol id
dpid = 1001                     # depot id, start from 1001
uid = 1                         # user id


# distance matrix between vertiport pairs
distanceMatrix = np.load('../inputs/dist.npy')    


# load input file for vertiport
arrivalMatrix = []
for vtp in vertiportList: 
    arrivalList = np.load('../inputs/Demand/arr_v' + str(vtp) + '.npy')    
    arrivalList = list(arrivalList)
    arrivalList = [i for i in arrivalList if i in range(startTime, endTime+1)]   
    countList, bins = np.histogram(arrivalList, bins=60, range=(360, 1260))    # countList contains # user in each slot 
    arrivalMatrix.append(countList)    # number of user in each slot. arrivalMatrix是一个二维数组，统计每个机场在每个slot中的到达人数  


# demand in each vertiport
demand = [sum(i) for i in arrivalMatrix]


# Generate destination probability based on vertiport pair demand
pair_weight = np.load('../inputs/pair_weight.npy')   #pair_weight is a matrix including the probability between one vertiport to other
dest_prob = []


# distance list from each vertiport to depot
vertiToDepot = np.load('../inputs/verti_depot_dist.npy')
dist = np.load('../inputs/dist.npy')

# collect user infomation(uid, vid, uid, destination, arrivalTime) for model simulation
user_id = []
user_vid = []
user_eid = []
outOfVehicleWait = []
inVehicleWait = []

def collectUserDate(uid, vid, eid, wait_evtol):
    user_id.append(uid)
    user_vid.append(vid)
    user_eid.append(eid)
    outOfVehicleWait.append(wait_evtol)