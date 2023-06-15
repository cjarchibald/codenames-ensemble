import random
import numpy as np
import sys
import os
import joblib
from sklearn.linear_model import LinearRegression
from scipy.interpolate import LinearNDInterpolator
from scipy.interpolate import NearestNDInterpolator
from scipy.interpolate import RBFInterpolator
from scipy.stats.qmc import Halton
import matplotlib.pyplot as plt
from pathlib import Path
import json

def filterEventProb(m, mLeft, byLeft):
    #See if this event is possible, given the current state
    # m is the TurnEvent
    # mLeft is the player's number of cards left
    # byLeft is the number of bystander cards left

    # print(f'**FILTER EVENT PROB for mine={mLeft}, by={byLeft}')
    # m.printEvent()

    #It isn't possible if m.mine is greater than mLeft
    if m.mine > mLeft:
        # print('  0 -> too many of mine')
        return 0.0
    
    #It isn't possible if m.mine equals mLeft and m.bad is not None
    if m.mine == mLeft and m.bad:
        # print('  0 -> all mine + bad')
        return 0.0

    #It isn't possible if m.bad is 'by' and byLeft is 0
    if m.bad == 'by' and byLeft == 0:
        # print('  0 -> no by left')
        return 0.0
    
    #We don't have to check if it is theirs or assassin, because if 
    #there weren't at least 1 of those cards, the game would already be over

    # print('  ', m.p, ' -> unfiltered')
    return m.p

def getEventProbs(pM, mLeft, byLeft):
    #pM is the player's TurnEvent list
    #mLeft is the player's number of cards left
    #byLeft is the number of bystander cards left
    # This function will compute and return a new distribution 
    # over the TurnEvents in pM, given the context, 
    # i.e. restricting ourselves to only possible turnEvents

    x = list(range(36))
    x2 = [i+36 for i in x]
    p_prior = [m.p for m in pM]
    
    #Filter probs by possibility
    mProbsUN = np.asarray([filterEventProb(m, mLeft, byLeft) for m in pM])
    #Renormalize and return
    mProbs = mProbsUN / mProbsUN.sum()
    if np.isnan(mProbs).any():
        print('ERROR, THIS IS WHAT WE HAVE HERE!!!!')
        print('Mine left: ', mLeft)
        print('By Left: ', byLeft)
        for i, m in enumerate(pM):
            m.printEvent()
            print('[', i, '] => Post prob : ', mProbs[i])

    return mProbs

def simulateSolitaireGame(pA, aLeft, bLeft, byLeft):
    # Complete a game from this state, where 
    # pA is player A's TurnEvent lists (distributions over outcomes for single turn)
    # aLeft is the number of cards A has left
    # bLeft is the number of cards B has left
    # byLeft is the number of bystander cards left
    #Return True, num-turns if A wins this game simulation in num-turns turns
    #False, 0 if they lose

    # Create the probabilities to draw from
    AProbs = [a.p for a in pA]
    
    #It is always A's turn
    turnCount = 1

    #Sit in this loop until the game ends and something is returned
    while True:
        #What does A do this turn?
        #Draw their turn result
        AProbs = getEventProbs(pA, aLeft, byLeft)
        turnResult = np.random.choice(pA, p=AProbs)
        aLeft -= turnResult.mine  #Adjust state by how many of their cards they got
        # This happens first, because turn ends if bad thing happens
        if aLeft <= 0:
            # print(' A won normally')
            return True, turnCount #A won
        if turnResult.bad:
            #Something bad happened, adjust state accordingly
            if turnResult.bad == 'theirs':
                bLeft -= 1
            if turnResult.bad == 'by':
                byLeft -= 1
            if turnResult.bad == 'assassin':
                return False, 0

        #If A lost by turning over other things, return False
        #If all the bystanders are turned over, that doesn't matter
        if bLeft == 0:
            return False, 0

        turnCount += 1

def calculatePlayerStats(pA, aLeft, bLeft, byLeft, N):
    #Estimate the win-rate and win-turns for player A, where the inputs are:
    #  - pA is the list of A's TurnEvents
    #  - aLeft is the number of cards A has left
    #  - bLeft is the number of cards B has left
    #  - byLeft is the number of bystander cards left

    Awins = 0
    winTurns = 0
    for i in range(N):
        Awin, winTurn = simulateSolitaireGame(pA, aLeft, bLeft, byLeft)
        winTurns += winTurn
        if Awin:
            Awins += 1

    #Return win-rate and win-time
    if Awins == 0:
        Awins = 1
    return Awins/N, winTurns/Awins

class TurnEvent():
    def __init__(self, mine, bad, P):
        self.mine = mine
        self.bad = bad
        self.p = P

    def printEvent(self):
        print('[TurnEvent] (P =', round(self.p,4), ') Mine: ', self.mine, 'Bad: ', self.bad)

def create_string(arr):
    res = ''
    for num in arr:
        res += str(num)
    return res

def generate_pos_events():
    res = []
    for r in range(10):
        c = 0
        for b in [None, 'theirs', 'by', 'assassin']:
            
            if r == 0 and (b is None):
                c += 1
                continue
            if r == 9 and (b is not None):
                c += 1
                continue

            key = [r, 0, 0, 0]
            if c > 0:
                key[c] = 1
            c += 1
            res.append(create_string(key))
    return res

def create_events(pos_events,probs):
    #We pass in pos_events because order matters
    P = []

    for event, p in zip(pos_events,probs):
        r = int(event[0])
        if int(event[1]) == 1:
            b = "theirs"
        elif int(event[2]) == 1:
            b = "by"
        elif int(event[3]) == 1:
            b = "assassin"
        else:
            b = None

        newEvent = TurnEvent(r, b, p)
        P.append(newEvent)
    return P

def createDetProbVector(n,a):
    #Create a random successful agent
    p = np.zeros(n)

    for i in range(1,9):
        p[4*i-1] = np.random.randint(low=1, high=6*i*i) #i right
        p[4*i] = np.random.randint(low=0,high=2*i)    #i right 1 blue
        if a > 0:
            p[4*i-2] = 0.5*np.random.randint(low=0,high=2*a) #i right 1 assassin

    p = p/np.sum(p)
    return p

def createRandomProbVector(n):
    #Default high value
    # S = 7
    S = np.random.randint(low=1,high=9)

    #scaler for high value for good things
    # m = 4
    m = np.random.randint(low=2, high=6)

    #scaler for high value for getting one right
    # w = 9
    w = np.random.randint(low=2,high=12)

    #high value for all the assassins
    # A = 2
    A = np.random.randint(low=1, high=8)
    h = S*np.ones(n)
    #Default high for all stats is 2, besides those listed
    h[0] = m*S   #1 Blue
    h[1] = m*S   #1 Bystander
    h[3] = w*S+1   #1 Correct

    for i in range(1,9):
        h[4*i-1] = m*S   #i Correct 
        h[4*i] = m*S   #i Correct & 1 Blue
        h[4*i+1] = m*S   #i Correct & 1 Bystander

    ai = 2
    while ai < 36:
        h[ai] = A
        ai += 4

    low = np.zeros(n)
    low[3] = 1

    valid = False
    while not valid:
        p = np.random.randint(low,high=h,size=n)

        if np.sum(p) > 0:
            valid = True
    p = p/np.sum(p)
    return p

def save_stats_v_colt(M, N, colt):
    #M is the number of points to evaluate and plot
    #N is the number of samples to use to estimate the stats
    #This function will create a new plot
    colt_vals = []   #COLT ratings
    winr_vals = []   #WIN RATE values
    wint_vals = []   #WIN TIME values

    pos_events = generate_pos_events()

    for m in range(M):
        #Create a random A prob vector
        if m > 50: #How many good vectors to do
            pA = createRandomProbVector(36)
        else:
            pA = createDetProbVector(36,m)
        eA = create_events(pos_events, pA)

        #Get the stats for the player probability between them
        aLeft = 9
        bLeft = 8
        byLeft = 7

        Awr, Awt = calculatePlayerStats(eA, aLeft, bLeft, byLeft, N)

        winr_vals.append(Awr)
        wint_vals.append(Awt)

        #Add the COLT rating for this data point   
        Acolt = colt.predict(pA.reshape(1,-1))[0]
        print('<', m, '>[', Awr, ' | ', Awt, '] => ', Acolt, ' colt')
        colt_vals.append(Acolt)

    tosave = dict()
    tosave["colt"] = colt_vals
    tosave["winr"] = winr_vals
    tosave["wint"] = wint_vals

    with open("colt.json", "w") as outfile:
        json.dump(tosave, outfile)

def load_colt_stats():

    with open("colt.json", "r") as openfile:
        coltstats = json.load(openfile)

    winr_vals = np.asarray(coltstats["winr"])
    wint_vals = np.asarray(coltstats["wint"])
    colt_vals = np.asarray(coltstats["colt"])

    return winr_vals, wint_vals, colt_vals

def plot_stats_rbf(winr_vals, wint_vals, colt_vals):
    wr_norm = np.linalg.norm(winr_vals)
    wt_norm = np.linalg.norm(wint_vals)

    wrv = winr_vals / wr_norm
    wtv = wint_vals / wt_norm

    x = np.stack((wrv,wtv)).T

    #Create the interpolator of the colt values
    interp = RBFInterpolator(x, colt_vals,smoothing=1,kernel='gaussian',epsilon=1)

    #Set up bounds for plotting
    minwinr = 0.0 / wr_norm
    maxwinr = 1.0 / wr_norm
    minwint = 1.0 / wt_norm
    maxwint = 15.0 / wt_norm

    xgrid = np.mgrid[minwinr:maxwinr:50j, minwint:maxwint:50j]
    pgrid = np.mgrid[(minwinr*wr_norm):(maxwinr*wr_norm):50j, (minwint*wt_norm):(maxwint*wt_norm):50j]
    xflat = xgrid.reshape(2, -1).T
    yflat = interp(xflat)
    ygrid = yflat.reshape(50,50)

    ax = plt.gca()
    fig = plt.gcf()
    plt.rcParams.update({'font.size': 22})
    pp = ax.pcolormesh(*pgrid, ygrid, shading='auto')

    def format_coord(x, y):
        x0, x1 = ax.get_xlim()
        y0, y1 = ax.get_ylim()
        col = int(np.floor((x-x0)/float(x1-x0)*50))
        row = int(np.floor((y-y0)/float(y1-y0)*50))
        if col >= 0 and col < 50 and row >= 0 and row < 50:
            z = ygrid[col, row]
            return 'x=%1.4f, y=%1.4f, z=%1.4f, (rc = %1.1f, %1.1f)' % (x, y, z, row, col)
        else:
            return 'x=%1.4f, y=%1.4f' % (x, y)

    ax.format_coord = format_coord
    plt.show()



if __name__ == "__main__":
    #Load the learned CoLT model weights
    colt_model = joblib.load("sklinear36model-nobias-11-04-2022.joblib")

    #Uncomment to generate the colt and win rate x win time data
    # save_stats_v_colt(500,1000,colt_model)
    wr, wt, ct = load_colt_stats()

    #This will plot out Figure 3 from the paper.
    plot_stats_rbf(wr,wt,ct)
