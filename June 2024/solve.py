# Jane Street Puzzle "Altered States 2"
# June 2024
# Solution by Nicholas Patel

################
### Solution ###
################
# Formulate problem and solve via z3 (cracked solver) in Python
# Not guaranteed optimal, but we can add constraints to force certain states to be found

# Define grid coordinates 1 <= i,j <= N where N = length of grid (=5 for us) and i = row index and j = column index
# Let x_(i,j) = cell value in cell (i,j) from 1 ('a') to 26 ('z')
# Let W denote the set of all US states 
# Let b(i, j, w, p, e) = 1 if the sub-word w[p:] can be written starting at cell (i,j) given that we are allowed e errors, else 0
# Let u(w) = 1 if the final grid includes word w, else 0
# Let c(w) be the coefficient of word w in the objective function
# We then seek to maximise P = sum of u(w)*c(w)

# We have the following constraints:
# 1. Natural/Value constraints: all x_(i,j) are integers between 1 and 26 inclusive, and all b(i, j, w, p, e) and u(w) are binary (0 or 1)

# 2. Constrain b values on the x values: use the recursive relation, which depends on the pair of Booleans (e, x_(i,j) == w[p]) 
#                                        Base case (p = len(w)-1): b = 1 if x_(i,j) == w[p], if x_(i,j) != w[p] then b = e
#                                        Recursive step (p < len(w)-1):
#                                           if x_(i,j) != w[p], b(i, j, w, p, e) = 1 iff e>0 and sum of b(i', j', w, p+1, 0) for all adjacent (i',j') is > 1
#                                           if x_(i,j)  = w[p], b(i, j, w, p, e) = 1 iff sum of b(i', j', w, p+1, e) for all adjacent (i',j') is > 1

# 3. Constrain u values: u(w) = 1 if sum(b(i, j, w, 0, 1)) > 0, else 0

# 4. Constrain P on the u values: P = sum u(w) * c(w)

# 5. Constraints to meet certain targets: P > 200M


################
### Imports  ###
################
from z3 import *
import time
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


########################
###  Solve function  ###
########################
def solve(N, solve, state_pops, state_arrays, guess = None, exclude = []):
    
    # Setup
    start_time = time.time()
    solver = Solver() if solve == 'satisfy' else Optimize()

    # Define variables
    X = {(i,j): Int(f'X_{i}_{j}') for i in range(1,N+1) for j in range(1,N+1)}
    b = {}
    for i in range(1,N+1):
        for j in range(1,N+1):
            for w in state_pops:
                for p in range(len(w)):
                    for e in range(2):
                        b[(i,j,w,p,e)] = Int(f'b_{i}_{j}_{w}_{p}_{e}')
    u = {}
    for w in state_pops:
        u[w] = Int(f'u_{w}')
    P = Int('P')


    # Add constraints

    # Constraint 0:
    if guess:
        for i in range(N):
            for j in range(N):
                if guess[i][j] != '':
                    v = ord(guess[i][j]) - ord('a') + 1
                    solver.add(X[(i+1,j+1)] == v)
                for c in exclude:
                    v = ord(c) - ord('a') + 1
                    solver.add(X[(i+1,j+1)] != v)

    # Constraint 1:
    for i in range(1,N+1):
        for j in range(1,N+1):
            solver.add(And(X[(i,j)] >= 1, X[(i,j)] <= 26))
            for w in state_pops:
                for p in range(len(w)):
                    for e in range(2):
                        if p == len(w) - 1:
                            if e == 1:
                                solver.add(b[(i,j,w,p,e)] == 1)
                            if e == 0:
                                solver.add(b[(i,j,w,p,e)] == If(X[(i,j)] == state_arrays[w][p], 1, 0))
                        else:
                            solver.add(b[(i,j,w,p,e)] >= 0, b[(i,j,w,p,e)] <= 1)
    for w in state_pops:
        solver.add(u[w] >= 0, u[w] <= 1)

    # Constraint 2:
    directions = [(1,0), (0,1), (-1,0), (0,-1), (1,1), (1,-1), (-1, 1), (-1,-1)]
    for i in range(1,N+1):
        for j in range(1,N+1):
            for w in state_pops:
                for p in range(len(w)-1, -1, -1):
                    for e in range(2):
                        adjacent = [(i+di,j+dj) for di,dj in directions if 1 <= i+di <= N and 1 <= j+dj <= N]
                        if p < len(w) - 1:
                            if e == 0:
                                solver.add(Implies(X[(i,j)] != state_arrays[w][p], 
                                                b[(i, j, w, p, e)] == 0))
                                solver.add(Implies(X[(i,j)] == state_arrays[w][p], 
                                                b[(i, j, w, p, e)] == If(Sum([b[(r, c, w, p+1, 0)] for r,c in adjacent]) > 0, 1, 0)))
                            if e == 1:
                                solver.add(Implies(X[(i,j)] != state_arrays[w][p], 
                                                b[(i, j, w, p, e)] == If(Sum([b[(r, c, w, p+1, 0)] for r,c in adjacent]) > 0, 1, 0)))
                                solver.add(Implies(X[(i,j)] == state_arrays[w][p], 
                                                b[(i, j, w, p, e)] == If(Sum([b[(r, c, w, p+1, 1)] for r,c in adjacent]) > 0, 1, 0)))

    # Constraint 3:
    for w in state_pops:
        solver.add(u[w] == If(Sum([b[(i, j, w, 0, e)] for i in range(1,N+1) for j in range(1,N+1) for e in range(2)]) > 0, 1, 0))

    # Constraint 4:
    P = Sum([state_pops[w]*u[w] for w in state_pops])
    if solve == 'optimise': solver.maximize(P)
    elif N > 3: solver.add(P > 200_000_000) #165_379_868

    # Check if there is a solution
    if solver.check() == sat:
        model = solver.model()
        print("\nSolution found!")
        print(f'Time taken: {(time.time() - start_time)/60.0: .2f} minutes \n')
        print("Solution grid")
        res = ""
        for i in range(1, N+1):
            for j in range(1, N+1):
                value = model[X[(i,j)]].as_long()
                c = chr(value-1+ord('a'))
                res += c
                print(f'{c:2}', end=' ')
            print()
        print("\nSolution: ", res)
        print("Objective Function Value: ", model.eval(P).as_long())
        print("States reached: ")
        for w in state_pops:
            if model[u[w]].as_long(): print(" - ", w)
        print()

    else:
        print("\nNo solution found.")
        print(f'Time taken: {(time.time() - start_time)/60.0: .2f} minutes \n')



###################
### Solve grids ###
###################

# Process state data
census_data = pd.read_csv("census.csv", names = ['Rank1', 'Rank2', 'State', 'Pop_2020', 'Pop_2010', 'Change', 'Pct_Change'], header = 0)
census_data = census_data[census_data['Rank1'].notnull()][['State', 'Pop_2020']]
census_data.set_index('State', inplace = True)
census_data = census_data['Pop_2020'].to_dict()
state_pops, state_arrays = {}, {}
for S in census_data:
    s = S.lower().replace(' ', '')
    state_arrays[s] = [ord(c) - ord('a') + 1 for c in s]
    state_pops[s] = int(census_data[S].replace(',', ''))

# Basic heuristics to help guess the middle row
if False:
    counts = {}
    weighted_by_pop = {}
    letter_counts = {chr(i + ord('a')): 0 for i in range(26)}
    for w in state_pops:
        for c in w: letter_counts[c] = letter_counts.get(c, 0) + 1
        for i in range(len(w)-1):
            pair = ''.join(sorted(w[i:i+2]))
            counts[pair] = counts.get(pair, 0) + 1
            weighted_by_pop[pair] = weighted_by_pop.get(pair, 0) + state_pops[w]
    sorted_pairs = sorted(list(counts.items()), key = lambda x: -x[1])
    sorted_weighted = sorted(list(weighted_by_pop.items()), key = lambda x: -x[1])
    sorted_letter_counts = sorted(list(letter_counts.items()), key = lambda x: x[1])
    top_pairs = sorted_pairs[:min(10, len(sorted_pairs))]
    top_weighted = [x[0] for x in sorted_weighted[:min(10, len(sorted_weighted))]]
    bottom_letters = sorted_letter_counts[:min(10, len(sorted_letter_counts))]
    print(f'Top pairs by frequency: {top_pairs}')
    print(f'Top pairs by weight: {top_weighted}')
    print(f'Bottom letters by frequency: {bottom_letters}')

# Example grid
if False:
    N = 3
    solve(N, 'satisfy', state_pops, state_arrays)

# Actual problem
if True:
    N = 5
    guess = None
    exclude = ['q', 'j', 'z', 'b', 'f', 'x']
    solve(N, 'satisfy', state_pops, state_arrays, guess, exclude)

    # Valid: esuhktchrctaioatsnlyenero, P = 168,154,932
    # guess = [[ '',  '',  '',  '',  ''],
    #          [ '',  '',  '',  '',  ''],
    #          [ '', 'a', 'i', 'o',  ''],
    #          [ '',  '', 'n',  '',  ''],
    #          [ '',  '',  '',  '',  '']]

    # Valid: knohrigrtclaieacsnorwilca, P = 168,813,371
    # guess = [[ '',  '',  '',  '',  ''],
    #          [ '',  '',  '',  '',  ''],
    #          [ '', 'a', 'i', 'e',  ''],
    #          [ '',  '', 'n',  '',  ''],
    #          [ '',  '',  '',  '',  '']]
    