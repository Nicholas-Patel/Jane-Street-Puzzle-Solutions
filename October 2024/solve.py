# Jane Street Puzzle "Knight Moves 6" 
# October 2024
# Solution by Nicholas Patel

# Formulate problem and solve via brute force (solves for a sub-optimal solution in < 1 min)

import time


def valid_path_exists(a,b,c,target):

    grid = [
        ['A', 'B', 'B', 'C', 'C', 'C'],
        ['A', 'B', 'B', 'C', 'C', 'C'],
        ['A', 'A', 'B', 'B', 'C', 'C'],
        ['A', 'A', 'B', 'B', 'C', 'C'],
        ['A', 'A', 'A', 'B', 'B', 'C'],
        ['A', 'A', 'A', 'B', 'B', 'C']
    ]
    visited = [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]

    N = 6
    valid = set()
    valid_paths = {}
    cell_score = {'A': a, 'B': b, 'C': c}
    directions = [(1,2), (2,1), (-1,2), (2,-1), (1,-2), (-2,1), (-1,-2), (-2,-1)]

    def dfs(i, j, N, type, curr_path, curr_squares, curr_score, visited, crosses):
        if (i == 0 and j == N-1 and type==1) or (i == N-1 and j == N-1 and type==2): 
            if curr_score == target: 
                valid.add(type)
                valid_paths[type] = ','.join(curr_squares)
            return

        # if crosses > 12:
        #     return
        
        if curr_score > target:
            return
        
        for di,dj in directions:
            r,c = i+di, j+dj
            if 0<=r<N and 0<=c<N and not visited[r][c]:
                visited[r][c] = 1
                curr_path.append(grid[r][c])
                curr_squares.append(chr(ord('a')+c) + str(6-r))
                if grid[i][j] == grid[r][c]:
                    curr_score += cell_score[grid[r][c]]
                else:
                    crosses += 1
                    curr_score *= cell_score[grid[r][c]]

                dfs(r, c, N, type, curr_path, curr_squares, curr_score, visited, crosses)
                
                if grid[i][j] == grid[r][c]:
                    curr_score -= cell_score[grid[r][c]]
                else:
                    crosses -= 1
                    curr_score //= cell_score[grid[r][c]]
                curr_squares.pop()
                curr_path.pop()
                visited[r][c] = 0
    
    visited[N-1][0] = 1
    dfs(N-1, 0, N, 1, ['A'], ['a1'], a, visited, 0)
    visited[N-1][0] = 0
    visited[0][0] = 1
    dfs(0, 0, N, 2, ['A'], ['a6'], a, visited, 0)
    return len(valid) == 2, valid_paths


def factors(x):
    res = []
    for f in range(x, 0, -1):
        if x%f == 0:
            res.append(f)
    return res


def brute_force():
    t0 = time.time()
    triples = []
    for c in [1, 2, 4, 8][::-1]:   # 11, 22, 23, 44, 46
        for k in range(7):
            target = 2024//c - k
            for b in factors(target):
                for a in range(1, 50-b-c, 1):
                    if a!=b and a!=c and b!=c and a+b+c<50:
                        triples.append((a,b,c))
    #triples.sort(key = lambda x: sum(x))
    for a,b,c in triples:
        boo, paths = valid_path_exists(a, b, c, 2024)
        if boo:
            print(f'Time taken: {time.time()-t0} seconds')
            print(f'Paths exist: {boo}')
            print(f'Values: A = {a}, B = {b}, C = {c}')
            print(f'Path from a1 -> f6: {paths[1]}')
            print(f'Path from a6 -> f1: {paths[2]}')
            return
    print(f'Time taken: {time.time()-t0} seconds')
    print('No solution found')


if __name__ == '__main__':
    brute_force()
