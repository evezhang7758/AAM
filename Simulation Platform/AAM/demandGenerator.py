# Generate potential demand based on a binomial distribution based on summation of three normal distribution
# one centered at 8 hours (8:00 am) with a standard deviation of 2 hours, another centered at 16 hours (4:00 pm) 
# with a standard deviation of 2 hours, and a third centered at 12 hours (noon) with a standard deviation of 6 hours.



from setup import *
from user import *

def predictUserArrivalTimeAndDest(vertiportMap, slot, interval, arrivalMatrix, uid, seed1, seed2):

    for i in vertiportList:
        count = arrivalMatrix[i-1][slot]    # demand for each 10 minutes
        if count == 0:
            continue

        # generate arrival interval for each user
        # prox_arrivalInterval是一个list，包含user到达的时间间隔
        prox_arrivalInterval = poisson_arr(count, seed1)   
        prox_arrivalTime = [interval + sum(prox_arrivalInterval[0:ind]) for ind in range(1, count+1)]  
        dest_prob = list(pair_weight[i-1,:])  # example: dest_prob = [0.0, 0.15, 0.06, ..., ]


        # generate a destination for each user
        for c in range(count):
            vid = generateDestination(dest_prob, seed2)     
            newUser = User(uid, vertiportList[vid], prox_arrivalTime[c])
            vertiportMap[i].userList.append(newUser)
            uid += 1
            seed2 += 1
        seed1 += 1

    return uid


# Random generate destination based on probability
def generateDestination(dest_prob, seed):
    np.random.seed(seed)
    random = np.random.rand()    # return a random float
    prob_ac = [sum(dest_prob[0:i]) for i in range(1, len(dest_prob)+1)]
    
    vid = dest_prob.index(max(dest_prob))   # return a vertiport id
    for k, v in enumerate(prob_ac):
        if random <= v:
            return k         # return a destination vertiport id
    
    return vid


# Generate a possion arrival process for each slot
def poisson_arr(count, seed):
    np.random.seed(seed)
    return np.random.poisson(lam = time_slot/(count+1), size = count).tolist()
