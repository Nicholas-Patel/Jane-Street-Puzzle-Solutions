# Jane Street Puzzle "Hooks 10"
# March 2024
# Solution by Nicholas Patel

# Solution:
# Formulate problem and solve via z3 (cracked solver) in Python

# Define grid coordinates 1 <= i,j <= N where N = length of grid (=9 for us) and i = row and j = column
# Let x_(i,j) = cell value in cell (i,j) from 1-N, or 0 if cell (i,j) is empty, or 0 if the cell is out of the grid
# Define a variable for every possible hook size/position, and the value assigned to it
# Let h_(i,j,k, o) = value assigned to hook with corner at (i,j) and side length k and orientation o
# and B_(i,j,k, o) = 1 if this hook is 'used' else 0

# We then have the following constraints:
# 1. All x_(i,j) are integers between 0 and N inclusive (natural constraint), and x_(i,j) = 0 if (i,j) outside bounds
# 2. x_(i,j) * x_(i+1,j) * x_(i,j+1) * x_(i+1,j+1) = 0 for all 1<=i,j<N (at least one unfilled square in every 2x2 region)
# 3. x_(i,j) = 0 if (i,j) is a clue cell  (clue cells must not be filled)
# 4. x_(i+1,j) + x_(i-1,j) + x_(i,j-1) + x_(i,j+1) = clue_(i,j)  (clue cells must be satisfied)
# 5. A dfs from one filled square should reach all filled squares (the filled cells form a single connected region)
# Exactly partition the grid using hooks:
# 6. For each k between 1 and N:
#       - Exactly one h_(i,j,k,o) can be nonzero, across all i and j and o (ie so every hook shape is used exactly once) --> sum_{all i and j and o} B_(i,j,k,o) = 1 
# 7. The hooks used must span every square exactly once:
#       - For all i,j: sum_{all a,b,c,d where the hook centred at (a,b) with side length c and orientation d contains the point (i,j)} B_(a,b,c,d) = 1
# Validly assign numbers to the hooks:
# 8. The grid has exactly 1 one, 2 twos, ... N Ns. 
# 9. If a hook is used, it contains values 0 or V (for some V>0), and exactly V occurences of that number:
#       - For all (i,j,k,o), if B_(i,j,k,o) = 1, then the hook centred at (i,j) with side length k and orientation o contains 2k-1-V zeros and V of the same value V
#       - That is, the cell sum is h_(i,j,k,o)^2 and every value is either 0 or h_(i,j,k,o)
# Constrain B and h on each other: 
# 10. B_(i,j,k,o) = 1 iff h_(i,j,k,o) > 0 else 0, and h_(i,j,k,o) is between 0 and N inclusive  (for all i,j,k,o)

from helper import *

def solve(N, clues, fact_positive):

    start_time = time.time()

    # Create variables
    orientation_map = {0: (1, 1), 1: (1,-1), 2: (-1,-1), 3: (-1,1)}
    X = [[Int(f'X_{i}_{j}') for j in range(N+2)] for i in range(N+2)]
    H = {(i, j, k, o): Int(f'H_{i}_{j}_{k}_{o}') for i in range(1,N+1) for j in range(1,N+1) for k in range(1, N+1) for o in range(4) if 0 < i + orientation_map[o][0]*(k-1) <= N and 0 < j + orientation_map[o][1]*(k-1) <= N}
    B = {(i, j, k, o): Int(f'B_{i}_{j}_{k}_{o}') for i in range(1,N+1) for j in range(1,N+1) for k in range(1, N+1) for o in range(4) if 0 < i + orientation_map[o][0]*(k-1) <= N and 0 < j + orientation_map[o][1]*(k-1) <= N}

    # Add constraints
    solver = Solver()

    # Constraint 1:
    for i in range(1,N+1):
        for j in range(1,N+1):
            solver.add(X[i][j] >= 0, X[i][j] <= N)
    for i in range(N+2):
        for j in range(N+2):
            if i == 0 or i > N or j == 0 or j > N:
                solver.add(X[i][j] == 0)

    # Constraint 2:
    for i in range(1, N):
        for j in range(1, N):
            solver.add(X[i][j] * X[i+1][j] * X[i][j+1] * X[i+1][j+1] == 0)

    # Constraints 3 and 4:
    for i,j,S in clues:
        solver.add(X[i][j] == 0)
        solver.add(X[i+1][j] + X[i-1][j] + X[i][j-1] + X[i][j+1] == S)
    
    # Constraint 5:
    nonzero = (N * (N+1))//2
    num_arcs_needed = nonzero - 1
    arcs1 = Sum([If(And(X[i][j]>0, X[i+1][j]>0), 1, 0) for i in range(1,N) for j in range(1,N+1)])
    arcs2 = Sum([If(And(X[i][j]>0, X[i][j+1]>0), 1, 0) for i in range(1,N+1) for j in range(1,N)])
    solver.add(arcs1 + arcs2 >= num_arcs_needed)
    contributors = []
    visited = set()
    directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    def dfs(a, b):
        visited.add((a,b))
        contributors.append(X[a][b])
        for dx, dy in directions: 
            if (1 <= a+dx <= N) and (1 <= b+dy <= N) and ((a+dx,b+dy) not in visited):
                contributors.append(If(X[a+dx][b+dy]>0, dfs(a+dx,b+dy), 0))
        return 0
    dfs(*fact_positive)
    cc = Sum([If(v>0,1,0) for v in contributors])
    solver.add(cc == nonzero)

    # Constraint 6:
    for k in range(1,N+1):
        b_variables = [B[i, j, k, o] for i in range(1,N+1) for j in range(1,N+1) for o in range(4) if 0 < i + orientation_map[o][0]*(k-1) <= N and 0 < j + orientation_map[o][1]*(k-1) <= N]
        solver.add(Sum(b_variables) == 1)

    # Constraint 7:
    for i in range(1,N+1):
        for j in range(1,N+1):
            b_variables  = [B[a, b, k, o] for a in range(1,N+1) for b in range(1,N+1) for k in range(1,N+1) for o in range(4) if 0 < a + orientation_map[o][0]*(k-1) <= N and 0 < b + orientation_map[o][1]*(k-1) <= N and ((i,j) in get_hook_cells(N,a,b,k,o))]
            solver.add(Sum(b_variables) == 1)
    
    # Constraint 8:
    for val in range(1, N+1):
        right_number = [If(X[i][j] == val, 1, 0) for i in range(1,N+1) for j in range(1,N+1)]
        solver.add(Sum(right_number) == val)
    
    # Constraint 9:
    for i in range(1, N+1):
        for j in range(1, N+1):
            for o in range(4):
                hor_dir, ver_dir = orientation_map[o]
                for k in range(1, N+1):
                    if 0 < i + hor_dir*(k-1) <= N and 0 < j + ver_dir*(k-1) <= N:
                        included = [X[a][b] for a,b in get_hook_cells(N,i,j,k,o) if (0 < a <= N) and (0 < b <= N)]
                        solver.add(Implies(
                            B[i,j,k,o] == 1, Sum(included) == (H[i,j,k,o])*(H[i,j,k,o])
                        ))
                        for var in included:
                            solver.add(Implies(
                                B[i,j,k,o] == 1, Or(var == 0, var == H[i,j,k,o])
                            ))
    
    # Constraint 10:
    for i in range(1,N+1):
        for j in range(1,N+1):
            for o in range(4):
                hor_dir, ver_dir = orientation_map[o]
                for k in range(1, N+1):
                    if 0 < i + hor_dir*(k-1) <= N and 0 < j + ver_dir*(k-1) <= N:
                        solver.add(H[i, j, k, o] >= 0, H[i, j, k, o] <= N)
                        solver.add(B[i, j, k, o] >= 0, B[i, j, k, o] <= 1)
                        solver.add(Implies(B[i, j, k, o] == 0, H[i, j, k, o] == 0))
                        solver.add(Implies(H[i, j, k, o] == 0, B[i, j, k, o] == 0))
                        solver.add(Implies(B[i, j, k, o] > 0, H[i, j, k, o] > 0))
                        solver.add(Implies(H[i, j, k, o] > 0, B[i, j, k, o] > 0))

    # Solve and print solution if it exists
    if solver.check() == sat:
        model = solver.model()
        print("Satisfiable! Model")
        print(f'Time taken: {(time.time() - start_time)/60.0: .2f} minutes \n')
        print("X grid:")
        grid = [[0 for _ in range(N)] for _ in range(N)]
        for i in range(1, N+1):
                for j in range(1, N+1):
                    value = model[X[i][j]].as_long()
                    print(f'{value:2}', end=' ')
                    grid[i-1][j-1] = value
                print()
        get_answer(N, grid)
        show_answer(N, clues, grid)
    else:
        print("Unsatisfiable!")
    return


# Example grid
if False:
    N = 5
    clues = [(1,1,0), (2,3,9), (2,5,7), (3,1,8), (4,3,15), (4,5,12), (5,1,10)]
    solve(N, clues, [4,1])

# Full grid
if True:
    N = 9
    clues = [(1,2,18), (1,7,7), (2,5,12), (3,3,9), (3,8,31), (5,2,5), (5,4,11), (5,6,22), (5,8,22), (7,2,9), (7,7,19), (8,5,14), (9,3,22), (9,8,15)]
    solve(N, clues, [3,9])