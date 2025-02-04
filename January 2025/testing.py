# Formulate problem and solve via z3 (cracked sat solver) in Python
# Nicholas Patel, 26 January 2025

from z3 import *
import time

def list_nums_with_distinct(factor):
    res = []
    for mult in range(1, (10**9)//factor):
        x = mult * factor
        s = str(x)
        padded = "0"*(9-len(s)) + s
        if len(set(padded)) == 9:
            res.append(padded)
    return res

def solve_possible(N, possible):
    
    # Setup
    start_time = time.time()
    solver = Solver()

    # Define variables
    X = {(i,j): Int(f'X_{i}_{j}') for i in range(1,N+1) for j in range(1,N+1)}
    Counts = {d: Int(f'{d}') for d in range(N+1)}
    Numbers = {i: Int(f'Number_{i}') for i in range(1,N+1)}

    # Add constraints
    for i in range(1,N+1):
        for j in range(1,N+1):
            solver.add(And(X[(i,j)] >= 0, X[(i,j)] <= N))
        solver.add(And(Numbers[i] > 0, Numbers[i] <= 987654321))
        solver.add(Numbers[i] == Sum([(10**(N-j))*X[(i,j)] for j in range(1,N+1)]))
    for i in range(1,N+1):
        for j in range(1,N+1):
            for r in range(i+1,N+1):
                solver.add(X[(i,j)] != X[(r,j)])
            for c in range(j+1,N+1):
                solver.add(X[(i,j)] != X[(i,c)])
    L = 3
    for i in range(N//L):
        for j in range(N//L):
            for x in range(L*i+1,L*i+1+L):
                for y in range(L*j+1,L*j+1+L):
                    for r in range(L*i+1,L*i+1+L):
                        for c in range(L*j+1,L*j+1+L):
                            if (x,y) != (r,c):
                                solver.add(X[(x,y)] != X[(r,c)])
    for d in range(N+1):
        solver.add(Sum([If(X[(i,j)] == d, 1, 0) for i in range(1,N+1) for j in range(1,N+1)]) == Counts[d])
        solver.add(Or(Counts[d] == 0, Counts[d] == N))
    for i in range(1,N+1):
        solver.add(Sum([If(Numbers[i] == int(possible[k]), 1, 0) for k in range(len(possible))]) == 1)

    known = [(1,8,2), (2,9,5), (3,2,2), (4,3,0), (6,4,2), (7,5,0), (8,6,2), (9,7,5)]
    for i,j,v in known:
        solver.add(X[(i,j)] == v)
        
    # Check if there is a solution
    if solver.check() == sat:
        model = solver.model()
        print("\nSolution found!")
        print(f'Time taken: {(time.time() - start_time)/60.0: .2f} minutes \n')
        print("Solution grid")
        res = [[0 for _ in range(N+1)] for _ in range(N+1)]
        for i in range(1, N+1):
            for j in range(1, N+1):
                value = model[X[(i,j)]].as_long()
                res[i-1][j-1] = value
                print(value, end=' ')
            print()
    else:
        print("\nNo solution found.")
        print(f'Time taken: {(time.time() - start_time)/60.0: .2f} minutes \n')


if False:
    possible = list_nums_with_distinct(333667)    
    N = 9
    solve_possible(N, possible)
    # 3 9 5 0 6 1 7 2 8 
    # 0 6 1 7 2 8 3 9 5 
    # 7 2 8 3 9 5 0 6 1 
    # 9 5 0 6 1 7 2 8 3 
    # 2 8 3 9 5 0 6 1 7 
    # 6 1 7 2 8 3 9 5 0 
    # 8 3 9 5 0 6 1 7 2 
    # 5 0 6 1 7 2 8 3 9 
    # 1 7 2 8 3 9 5 0 6 

if False:
    possible = list_nums_with_distinct(333667)    
    possible = [x for x in possible if int(x)%41 == 0]
    N = 9
    solve_possible(N, possible)

if True:
    possible = list_nums_with_distinct(333667)    
    possible = [x for x in possible if int(x)%37 == 0]
    N = 9
    solve_possible(N, possible)
