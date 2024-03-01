# Simple simulation to estimate the required probability

# Imports
from numpy import random as random
from matplotlib import pyplot as plt

# Setup
count, points = 0, 0
proportions = []
N = 10**5

# Solve
for _ in range(N):
    count += 1
    a, b, c, d = random.uniform(size = 4)
    r = 0.5 * ((a-c)**2 + (b-d)**2)**0.5
    x_c = (a+b)/2
    if 0.5*(a+c) + r > 1 or 0.5*(a+c) - r < 0 or 0.5*(b+d) + r > 1 or 0.5*(b+d) - r < 0:
        points += 1
    proportions.append(points/count)

# Display results
f1 = plt.figure()
plt.plot(proportions[N//10000:])
print("Best estimate: ", proportions[-1])

plt.ion(); plt.show(block = False)
input("Press enter to close"); plt.close('all')


