# Imports
import numpy as np
import mpmath
from matplotlib import pyplot as plt
from scipy.integrate import quad
import scipy.optimize as opt

# Helper functions
def integrand(x):
    return x * np.arccos(((1/x)*(2 - (1/x)))**0.5)

def prob_A_wins_given_g(g):
    return 0.25*g**2 + 2*g**2/np.pi * quad(integrand, 0.5, 1/g)[0]

def f(g):
    return quad(integrand, 0.5, 1/g)[0] + np.pi/8 - np.arccos((g*(2-g))**0.5)/(2*g**2)

# Find a reasonably narrow interval that the root is in
if False:
    N = 1000
    g_vals = np.linspace(0.0001, 1, N)
    g_vals = np.linspace(0.4, 0.6, N)
    probs = [0.] * N
    for i,g in enumerate(g_vals):
        probs[i] = prob_A_wins_given_g(g)
    fig = plt.figure()
    plt.plot(g_vals, probs)
    plt.show()

# Solve for the root
if True:
    g_prime = opt.brentq(f, 0.4, 0.6, xtol = 10**-25)
    P = np.arccos((g_prime*(2-g_prime))**0.5)/np.pi
    print(f'Best g for Erin: {g_prime}')
    print(f'Corresponding P(win) for Aaron: {P}')