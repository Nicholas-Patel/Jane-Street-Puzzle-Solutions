# Jane Street Puzzle: July 2023
# Solution by Nicholas Patel
# See the word doc. for the approach, this is just a script checking
# whether my solution was valid (and getting the answer from the solution)

# Let 0 denote no constraint on the number of elements in the grid given
# Let 1 denote shaded and 0 denote unshaded in the solution

constraints = [[6,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,6],
               [6,0,0,0,0,0,0,0,0,8,12,0,0,0,0,0,0,0,0,6],
               [0,0,0,10,10,0,0,0,0,0,0,0,0,0,0,12,12,0,0,0],
               [0,0,0,10,0,0,10,10,0,0,0,0,11,11,0,0,4,0,0,0],
               [0,0,0,0,0,0,10,0,0,0,0,0,0,11,0,0,0,0,0,0],
               [0,15,0,0,0,0,0,0,0,3,4,0,0,0,0,0,0,0,3,0],
               [0,4,0,0,0,0,0,0,0,6,5,0,0,0,0,0,0,0,12,0],
               [0,0,0,0,0,0,9,0,0,0,0,0,0,8,0,0,0,0,0,0],
               [0,0,0,15,0,0,9,9,0,0,0,0,8,8,0,0,8,0,0,0],
               [0,0,0,1,9,0,0,0,0,0,0,0,0,0,0,1,7,0,0,0],
               [4,0,0,0,0,0,0,0,0,12,8,0,0,0,0,0,0,0,0,4],
               [4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4]]

solution = [[0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,1],
            [0,0,1,0,1,1,1,1,0,0,1,1,1,1,1,1,0,1,1,1],
            [0,1,0,0,0,0,0,0,1,0,1,1,1,1,1,1,0,0,0,0],
            [1,0,1,1,1,1,1,0,0,1,0,0,0,0,0,0,1,1,1,1],
            [0,0,1,1,1,1,1,0,1,0,1,1,0,0,0,1,0,0,0,0],
            [0,0,0,0,0,0,0,1,0,0,1,1,0,1,0,1,0,1,1,1],
            [1,1,0,0,1,1,1,0,1,1,0,0,1,0,1,0,0,0,0,0],
            [1,1,0,0,1,1,1,0,1,1,0,0,1,0,1,0,1,1,1,1],
            [0,0,1,0,1,1,1,0,1,1,0,1,0,0,1,0,1,1,1,1],
            [0,0,0,1,0,0,0,0,0,0,1,0,1,0,0,1,0,0,0,0],
            [1,1,0,0,1,1,1,1,1,1,0,0,0,1,0,0,1,0,1,1],
            [1,1,0,0,1,1,1,1,1,1,0,0,0,0,1,1,0,0,1,1]]


class funcs:

    # Setup
    def __init__(self):
        self.m, self.n = len(constraints), len(constraints[0])
        assert self.m == len(solution) and self.n == len(solution[0])
        self.visited = set()
        self.region = set()
        self.numbers = set()
        self.directions = [(1,0), (0,1), (-1,0), (0,-1)]

    # Helper functions

    def isRectangle(self, points):
        area = len(points)
        left, right, top, bottom = float("inf"), 0, float("inf"), 0
        for x,y in points:
            left = min(left, y)
            right = max(right, y)
            top = min(top, x)
            bottom = max(bottom, x)
        return area == (right - left + 1)*(bottom - top + 1)

    def isConsistent(self, nums):
        if len(nums) > 2: return False
        for x in nums:
            if x != 0 and len(self.region) != x:
                return False
        return True

    def search_region(self, x, y):
        self.visited.add((x,y))
        self.region.add((x,y))
        self.numbers.add(constraints[x][y])
        for dx, dy in self.directions:
            r,c = x + dx, y + dy
            if 0 <= r < self.m and 0 <= c < self.n and (r,c) not in self.visited and solution[x][y] == solution[r][c]:
                self.search_region(r,c)

    def isValid(self, solution):
        for x in range(self.m):
            for y in range(self.n):
                if (x,y) not in self.visited:
                    self.region = set()
                    self.numbers = set()
                    self.search_region(x,y)
                    if not self.isConsistent(self.numbers): return False
                    if solution[x][y] == 1 and not self.isRectangle(self.region): return False
        return True
    
    def getAnswer(self, solution):
        ans = 1
        for r in range(len(solution)):
            ans *= sum([1 for x in solution[r] if x == 0])
        return ans


# Solve nd print answer
f = funcs()
valid = f.isValid(solution)
answer = f.getAnswer(solution)
print(f'\n#####################\nSolution valid: {valid}\nAnswer = {answer}\n#####################\n')
