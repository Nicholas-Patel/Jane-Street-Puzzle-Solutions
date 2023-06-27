# Jane Street Puzzle "Arc-edge Acreage"

# Solution: 

# Define a shape as a set of vertices
# If an enclosed thing has area exactly 32, the shape must have area 32 also
# So, we can find all shapes with area 32, then for each shape, the number of things which have area 32 is just nC0.5n where n=numEdges

# So we need to find the number of polygons with area 32 in the 7x7 grid
# First find all such unique polygons
# Second find number of ways each unique polygon can fit into the 7x7 grid
# Total polygons = sumproduct of the above


import numpy as np
import math


def backtrack_polygons(start, visited, shape):
    # Start at a point. Keep going until either we reach start (found valid loop) or cant continue/reached a diff previous point(break)

    x_end, y_end = shape[-1]

    # Add solution if its valid and has the correct area
    if (x_end, y_end) == start and len(shape) > 1:
        if find_area(shape[:-1]) == Area_Needed:
            counts[len(shape)-1] = counts.get(len(shape)-1, 0) + 1
        return
    
    # Else look for more
    else:
        for dx, dy in directions:
            x_new, y_new =  x_end + dx, y_end + dy
            if 0 <= x_new <= N_sides and 0 <= y_new <= N_sides:
                if (x_new, y_new) == start or (x_new, y_new) not in visited:
                    visited.add((x_new, y_new))
                    shape.append((x_new, y_new))
                    backtrack_polygons(start, visited, shape)
                    shape.pop()
                    visited.remove((x_new, y_new))
    return

def find_area(x_y):
    # Given a polygon shape find the area enclosed via shoelace formula
    x_y = np.array(x_y)
    x_y = x_y.reshape(-1,2)
    x = x_y[:,0]
    y = x_y[:,1]
    S1 = np.sum(x*np.roll(y,-1))
    S2 = np.sum(y*np.roll(x,-1))
    area = .5*np.absolute(S1 - S2)
    return area

def find_perms(shape_counts):
    # Find the total number of unique shapes
    total = 0
    for perimeter, count in shape_counts.items():
        num = count // (2*perimeter)
        num *= math.comb(perimeter, perimeter//2)
        total += num
    print(f"Total is {total}")
    return total


# Solve the specific problem
N_sides = 7
Area_Needed = 32
directions = [(1,1), (1,-1), (-1,1), (-1,-1)]
counts = {}
unique_shapes = []

for i in range(N_sides+1):
    for j in range(N_sides+1):
        start = (i,j)
        visited = set([(i,j)])
        backtrack_polygons((i,j), visited, [(i,j)])


final_answer = find_perms(counts)