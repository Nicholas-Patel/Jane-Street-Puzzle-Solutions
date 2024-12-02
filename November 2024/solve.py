# Imports
import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import quad, dblquad

# Helper function
def integrand(b, a):
    return b + (a**2+b**2) * (0.25*np.pi - np.arctan(b/a)) + ((a-1)**2+b**2) * (0.25*np.pi - np.arctan(b/(1-a)))

# Simulate to get a rough estimate of the probability
if 1:
    count, num_sims = 0., 0.
    proportions = []
    N = 10**6
    for _ in range(N):
        a,b = np.random.uniform(low=0, high=1, size=2)
        if (a <= 0.5 and b <= a): 
            num_sims += 1
            c,d = np.random.uniform(low=0, high=1, size=2)
            mid = [(a+c)/2, (b+d)/2]
            m = -1/((d-b)/(c-a)) if d!=b else float("inf")
            if m == float("inf"): count += 1
            elif m != 0:
                x_int = (-mid[1]/m) + mid[0]
                if 0 <= x_int and x_int <= 1: count += 1
            proportions.append(count/num_sims)
    fig = plt.figure()
    plt.plot(proportions)
    plt.show()

# Obtain the probability numerically
if 1:
    prob = 8 * (dblquad(integrand, 0, 0.5, 0, lambda x: x, epsabs=10**-24)[0])
    print(f'Answer: {prob}')
