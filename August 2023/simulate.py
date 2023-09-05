######################################
### Jane Street August 2023 Puzzle ###
###         Single-Cross 2         ###    
######################################

# Nicholas Patel

# Simulation approach: 
# - see how probability changes with D, P = f(D)
# - ascertain whether D > 1 or D <= 1 and get rough estimate of optimal D
# - range of D looks like it'll affect the math, ie P = f(D) piecewise

# Imports and setup
import numpy as np
from matplotlib import pyplot as plt
import random
import math
rng = np.random.default_rng()

# Helper functions
def findProb(D):
    N = 10**5
    count = 0.
    for _ in range(N):
        u = np.random.uniform(low=-1,high=1)
        theta = np.random.uniform(low=0,high=2*np.pi)
        x = random.uniform(0,1) + D * ((1.- u**2)**0.5) * np.cos(theta)
        y = random.uniform(0,1) + D * ((1.- u**2)**0.5) * np.sin(theta)
        z = random.uniform(0,1) + D * u
        boo = isAdjacent(x,y,z)
        if boo: count += 1
    return count/N

def isAdjacent(d,e,f):
    n = abs(math.floor(d)) + abs(math.floor(e)) + abs(math.floor(f))
    return n==1

# Plot approximation/curve of Probability against D
if True:
    N = 100
    D_vals = []
    probs = []
    for d in np.linspace(0.5, 1.4, N):
        p = findProb(d)
        D_vals.append(d)
        probs.append(p)
    plt.figure()
    plt.xlabel('D')
    plt.ylabel('P = f(D)')
    plt.plot(D_vals, probs)
    plt.show()

