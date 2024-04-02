from z3 import *
import time
from matplotlib import pyplot as plt

def get_hook_cells(N,i,j,k,o):
    ans = set()
    if o == 0:
        for a in range(i, i+k):
            ans.add((a,j))
        for b in range(j, j+k):
            ans.add((i,b))
    elif o==1:
        for a in range(i, i+k):
            ans.add((a,j))
        for b in range(j, j-k, -1):
            ans.add((i,b))
    elif o==2:
        for a in range(i, i-k,-1):
            ans.add((a,j))
        for b in range(j, j-k,-1):
            ans.add((i,b))
    else:
        for a in range(i, i-k, -1):
            ans.add((a,j))
        for b in range(j, j+k):
            ans.add((i,b))
    return ans

def get_answer(N, grid):

    directions = [(0,1), (1,0), (-1,0), (0,-1)]
    def dfs(i,j):
        if i < 0 or i >= N or j < 0 or j >= N or visited[i][j] or grid[i][j]: return 0
        visited[i][j] = True
        ans = 1
        for dx,dy in directions:
            ans += dfs(i+dx, j+dy)
        return ans

    res = 1
    visited = [[False for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if grid[i][j] == 0 and not visited[i][j]:
                res *= dfs(i,j)
    print(f'\nAnswer is {res}\n')
    return

def show_answer(N, clues, grid):
    clues_dict = {(i-1,j-1):k for i,j,k in clues}
    positive_color = 'blue'
    cmap = plt.matplotlib.colors.ListedColormap(['white', positive_color])
    plt.imshow(grid, cmap=cmap, interpolation='none', vmin=0, vmax=1)
    for i in range(N):
        for j in range(N):
            if (i,j) not in clues_dict:
                plt.text(j, i, str(grid[i][j]), ha='center', va='center', color='black')
            else:
                plt.text(j, i, str(clues_dict[(i,j)]), ha='center', va='center', color='orange')
    plt.xticks([])
    plt.yticks([])
    plt.savefig('Answer')
    plt.close('all')
