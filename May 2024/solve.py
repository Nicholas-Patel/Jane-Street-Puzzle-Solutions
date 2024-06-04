# Jane Street Puzzle "Number Cross 4"
# May 2024
# Solution by Nicholas Patel

################
### Solution ###
################
# Formulate problem and solve via z3 (cracked solver) in Python

# Define grid coordinates 1 <= i,j <= N where N = length of grid (=1 for us) and i = row index and j = column index
# Let x_(i,j) = cell value in cell (i,j) from 0 to 9, or -1 if cell (i,j) is shaded
# Let S = {R_1, R_2, ...} define the initial set of bounded regions, where each element R_k = {(i,j): (i,j) in region k} and the R are disjoint/partition the entire NxN grid
# Then, r_(i,j) = the initial region number (k) that cell (i,j) is in
# Let b_(i,j,i',j') = 1 if orthogonally adjacent cells (i,j) and (i',j') are in the same region in the solution, else 0. Note by convention (i,j) < (i',j')

# We then have the following constraints:
# 1. Natural/Value constraints: all x_(i,j) are integers between -1 and 9 inclusive, and all b_(i,j,i',j') are 0 or 1

# 2. Constrain b values: if cell (i,j) or (i',j') is shaded (x=-1) then b=0. 
#                        elif r_(i,j) = r_(i',j') then b=1
#                        else b=0

# 3. Constrain x values: if b_(i,j,i',j') = 1 then x_(i,j) = x_(i',j')
#                        else x_(i,j) != x_(i',j')

# 4. No adjacent shaded cells: for all (i,j) if x_(i,j) = -1 then none of x_(i+1,j), x_(i-1,j), x_(i,j+1). x_(i,j-1) can be -1

# 5. Row constraints: a. row clues, b. no numbers starting with a 0 digit, c. no single digit numbers
#                   for each row in the grid
#                           for every possible continuous sub-row of cells
#                                   if all cells in this sub-row are not -1, and before/efter both ends is a -1 or no cell, then the number formed by concatenating the digits must satisfy the row clue  
#                        
#                           for every element in row
#                                   if the previous element is -1 (or does not exist) then the current cell cannot be 0
#                               
#                           for every element in row
#                                   if the current element is not -1 then at least one of the previous and next elements must not be -1

# 6. Redundant constrains: the entire 2nd and 2nd last columns must not be shaded cells

################
### Imports  ###
################
from z3 import *
import time
from matplotlib import pyplot as plt
import numpy as np

########################
### Helper functions ###
########################

# Row clue functions
def power_func(X, solver, param, i, L, R):
    digits = R-L+1
    number = Sum([X[(i, L+k)]*10**(digits-1-k) for k in range(digits)])
    S = [param**n for n in range(int(np.log(10**8)/np.log(param)))]
    is_in_S = If(Sum([If(number == x, 1, 0) for x in S]) > 0, 1, 0)
    return is_in_S

def fibonacci_func(X, solver, param, i, L, R):
    digits = R-L+1
    number = Sum([X[(i, L+k)]*10**(digits-1-k) for k in range(digits)])
    curr, prev = 1, 1
    fib = []
    while curr <= 10**11:
        fib.append(curr)
        prev,curr = curr,curr+prev
    is_fib = If(Sum([If(number == x, 1, 0) for x in fib]) > 0, 1, 0)
    return is_fib

def multiple_func(X, solver, param, i, L, R):
    digits = R-L+1
    number = Sum([X[(i, L+k)]*10**(digits-1-k) for k in range(digits)])
    quotient = number/param
    is_multiple = If(quotient*param == number, 1, 0)
    return is_multiple

def cube_func(X, solver, param, i, L, R):
    digits = R-L+1
    number = Sum([X[(i, L+k)]*10**(digits-1-k) for k in range(digits)])
    r = Int(f'r_{i}_{L}_{R}')
    is_cube = If(r**3 == number, 1, 0)
    return is_cube

def square_func(X, solver, param, i, L, R):
    digits = R-L+1
    number = Sum([X[(i, L+k)]*10**(digits-1-k) for k in range(digits)])
    s = Int(f's_{i}_{L}_{R}')
    is_square = If(s**2 == number, 1, 0)
    return is_square

def prime_power_func(X, solver, param, i, L, R):
    digits = R-L+1
    number = Sum([X[(i, L+k)]*10**(digits-1-k) for k in range(digits)])
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 
              59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 
              127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 
              191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 
              257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 
              331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 
              401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 
              467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 
              563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 
              631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 
              709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 
              797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 
              877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 
              967, 971, 977, 983, 991, 997]
    S = set()
    for p1 in primes:
        for p2 in primes:
            if p2*np.log(p1) < np.log(10**11):
                S.add(p1**p2)
    is_in_S = If(Sum([If(number == x, 1, 0) for x in S]) > 0, 1, 0)
    return is_in_S

def digitsum_func(X, solver, param, i, L, R):
    total = Sum([X[(i, j)] for j in range(L, R+1)])
    is_right_sum = If(total == param, 1, 0)
    return is_right_sum

def digitproduct_last_digit_func(X, solver, param, i, L, R):
    product = X[(i,L)]
    for j in range(L+1, R+1):
        product = product * X[(i,j)]
    is_right_last_digit = If(product%10 == param, 1, 0)
    return is_right_last_digit

def palindrome_func(X, solver, param, i, L, R):
    digits = R-L+1
    if param == 0:    # palindrome
        match = Sum([If(X[(i, L+k)] != X[(i, R-k)], 1, 0) for k in range(digits//2)])
    elif param == -1: # one less than palindrome
        match = Sum([If(X[(i, L+k)] != X[(i, R-k)], 1, 0) for k in range(1, digits//2)]) + If(X[(i, L)] != X[(i, R)] + 1, 1, 0)
    else:             # one more than palindrome
        number = Sum([X[(i, L+k)]*10**(digits-1-k) for k in range(digits)]) - 1
        match = Sum([If((number/10**(digits-1-k))%10 != (number/10**k)%10, 1, 0) for k in range(digits//2)])
    is_palindrome = If(match > 0, 0, 1)
    return is_palindrome

# Extract answer from solution
def get_answer(grid):
    res = 0
    for row in grid:
        sub = [str(i) for i in row]
        sub = ''.join(sub).split('-1')
        for x in sub:
            if x: res += int(x)
    print(f'Answer: {res}')
    return

# Check the answer is indeed vald (not including row clues)
def check_answer(grid, regions):
    failed = 0
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            for di,dj in directions:
                r,c = i+di, j+dj
                if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
                    if grid[i][j] == -1 and grid[r][c] == -1: failed += 1
                    if regions[i][j] == regions[r][c] and grid[i][j] != -1 and grid[r][c] != -1 and grid[i][j] != grid[r][c]: failed += 1
                    if regions[i][j] != regions[r][c] and grid[i][j] == grid[r][c]: failed += 1
        sub = [str(d) for d in grid[i]]
        sub = ''.join(sub).split('-1')
        for x in sub:
            if x: 
                if str(x)[0] == "0": failed += 1
                if len(str(x)) == 1: failed += 1
    if failed == 0: print("\nValid solution!")
    else: print("\nInvalid solution")
    return failed == 0

########################
###  Solve function  ###
########################
def solve(N, regions, row_clues, row_clues_to_include = None, known = None, show = True):
    
    # Setup
    start_time = time.time()
    if row_clues_to_include is None: row_clues_to_include = list(range(1,N+1))

    # Create variables
    X = {(i,j): Int(f'X_{i}_{j}') for i in range(1,N+1) for j in range(1,N+1)}
    b = {}
    for i in range(1,N+1):
        for j in range(1,N+1):
            if i+1<=N:
                b[(i,j,i+1,j)] = Int(f'b_{i}_{j}_{i+1}_{j}')
            if j+1<=N:
                b[(i,j,i,j+1)] = Int(f'b_{i}_{j}_{i}_{j+1}')
    
    # Add constraints
    solver = Solver()

    # Constraint 1:
    for i in range(1,N+1):
        for j in range(1,N+1):
            if known and known[i-1][j-1] != -1:
                solver.add(X[(i,j)] == known[i-1][j-1])
            else:
                solver.add(X[(i,j)] >= -1, X[(i,j)] <= 9)
    for index in b:
        solver.add(b[index] >= 0, b[index] <= 1)

    # Constraint 2:
    for i,j,i_prime,j_prime in b:
        solver.add(Implies(Or(X[(i,j)] == -1, X[(i_prime, j_prime)] == -1), b[(i,j,i_prime,j_prime)] == 0))
        if regions[i-1][j-1] == regions[i_prime-1][j_prime-1]:
            solver.add(Implies(And(X[(i,j)] != -1, X[(i_prime, j_prime)] != -1), b[(i,j,i_prime,j_prime)] == 1))
        else:
            solver.add(b[(i,j,i_prime,j_prime)] == 0)

    # Constraint 3:
    for i,j,i_prime,j_prime in b:
        solver.add(Implies(b[(i,j,i_prime,j_prime)] == 1, X[(i,j)] == X[(i_prime, j_prime)]))
        solver.add(Implies(b[(i,j,i_prime,j_prime)] == 0, X[(i,j)] != X[(i_prime, j_prime)]))

    # Constraint 4:
    for i in range(1,N+1):
        for j in range(1,N+1):
            if i+1<=N:
                solver.add(Not(And(X[(i,j)] == -1, X[(i+1,j)] == -1)))
            if j+1<=N:
                solver.add(Not(And(X[(i,j)] == -1, X[(i,j+1)] == -1)))

    # Constraint 5:
    hint_funcs = {"power": power_func,
                  "fibonacci": fibonacci_func,
                  "multiple": multiple_func,
                  "cube": cube_func,
                  "palindrome": palindrome_func,
                  "square": square_func,
                  "digitsum": digitsum_func,
                  "digitproduct_last_digit": digitproduct_last_digit_func,
                  "prime_raised_prime": prime_power_func}
    for i in range(1, N+1):

        # 5a. 
        if i in row_clues_to_include:
            for hint_type, param in row_clues[i-1]:
                func = hint_funcs[hint_type]
                # Left bound at the start, right bound anywhere >= left
                for right in range(1,N):
                    num_shaded = Sum([If(X[(i,j)]==-1, 1, 0) for j in range(1,right+1)])
                    solver.add(Implies(And(num_shaded == 0, X[(i,right+1)] == -1), func(X, solver, param, i, 1, right) == 1))
                num_shaded = Sum([If(X[(i,j)]==-1, 1, 0) for j in range(1,N+1)])
                solver.add(Implies(num_shaded == 0, func(X, solver, param, i,  1, N) == 1))
                # Left bound not at the start, right bound not at end
                for left in range(2, N+1):
                    for right in range(left, N):
                        num_shaded = Sum([If(X[(i,j)]==-1, 1, 0) for j in range(left,right+1)])
                        solver.add(Implies(And(num_shaded == 0, X[(i, right+1)] == -1, X[(i, left-1)] == -1), func(X, solver, param, i, left, right) == 1))
                # Left bound not at start, right bound at end
                for left in range(2, N+1):
                    num_shaded = Sum([If(X[(i,j)]==-1, 1, 0) for j in range(left,N+1)])
                    solver.add(Implies(And(num_shaded == 0, X[(i, left-1)] == -1), func(X, solver, param, i, left, N) == 1))
        
        # 5b. 
        solver.add(X[(i,1)] != 0)
        for j in range(2, N+1):
            solver.add(Implies(X[(i, j-1)] == -1, X[(i, j)] > 0))

        # 5c.
        solver.add(Implies(X[(i, 1)] != -1, X[(i,2)] != -1))
        solver.add(Implies(X[(i, N)] != -1, X[(i, N-1)] != -1))
        for j in range(2, N):
            solver.add(Implies(X[(i, j)] != -1, Or(X[(i, j-1)] != -1, X[(i, j+1)] != -1)))

    # Constraint 6:
    for j in [2, N-1]:
        for i in range(1, N+1):
            solver.add(X[(i,j)] != -1)

    # Solve and print solution if it exists
    if solver.check() == sat:
        model = solver.model()
        print("Satisfiable! Model")
        print(f'Time taken: {(time.time() - start_time)/60.0: .2f} minutes \n')
        if show: print("X grid:")
        grid = [[0 for _ in range(N)] for _ in range(N)]
        for i in range(1, N+1):
                for j in range(1, N+1):
                    value = model[X[(i,j)]].as_long()
                    if show: print(f'{value:2}', end=' ')
                    grid[i-1][j-1] = value
                if show: print()
        B = check_answer(grid, regions)
        if B: get_answer(grid)
    else:
        print("Unsatisfiable!")
        print(f'Time taken: {(time.time() - start_time)/60.0: .2f} minutes \n')
    return


###################
### Solve grids ###
###################

# Example grid
if False:
    N = 5
    regions = [[1, 2, 3, 4, 5],
               [1, 2, 3, 5, 5],
               [1, 2, 3, 3, 5],
               [1, 2, 2, 3, 5],
               [1, 2, 2, 3, 3]]
    row_clues = [[("power", 7)], 
                 [("fibonacci", None)], 
                 [("multiple", 5)],
                 [("cube", None)],
                 [("palindrome", 0)]]
    show = True
    solve(N, regions, row_clues, show = True)

# Actual problem
if True:
    N = 11
    regions = [[ 1,  1,  1,  2,  2,  2,  3,  3,  4,  4,  4],
               [ 1,  5,  5,  5,  2,  2,  3,  4,  4,  4,  6],
               [ 1,  5,  5,  2,  2,  2,  3,  4,  4,  4,  6],
               [ 1,  5,  5,  2,  2,  7,  7,  4,  6,  6,  6],
               [ 1,  5,  2,  2,  4,  4,  7,  4,  6,  8,  6],
               [ 1,  4,  4,  4,  4,  4,  4,  4,  8,  8,  9],
               [10,  4,  4,  4,  4, 11, 11,  4,  8,  8,  8],
               [10, 10, 12,  4, 12, 11, 11,  4,  4,  8,  4],
               [10, 10, 12, 12, 12, 11, 11,  4,  4,  4,  4],
               [10, 12, 12, 10, 10, 10, 11,  4,  4,  4, 13],
               [10, 10, 10, 10, 10, 11, 11, 11,  4,  4, 13]]

    row_clues = [[("square", None)], 
                 [("palindrome", 1)], 
                 [("prime_raised_prime", None)],
                 [("digitsum", 7)],
                 [("fibonacci", None)],
                 [("square", None)], 
                 [("multiple", 37)], 
                 [("palindrome", 0), ("multiple", 23)],
                 [("digitproduct_last_digit", 1)],
                 [("multiple", 88)], 
                 [("palindrome", -1)]]
    
    known =   [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
               [-1, -1, -1, -1, -1, -1, -1,  4, -1, -1, -1],
               [-1, -1, -1, -1, -1, -1, -1,  4, -1,  8, -1],
               [ 1,  4,  4,  4, -1,  4,  4,  4,  8,  8,  9],
               [ 7,  4,  4,  4,  4, -1,  7,  4,  8,  8,  8],
               [ 7,  7, -1, -1, -1,  7,  7, -1,  9,  8,  9],
               [-1, -1, -1, -1, -1, -1, -1,  9,  9,  9,  9],
               [-1, -1, -1, -1, -1, -1, -1,  9,  9,  9,  2],
               [-1, -1, -1, -1, -1, -1, -1,  3,  9,  9,  2]]

    show = True
    solve(N, regions, row_clues, known = known, show = True)
