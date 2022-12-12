import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
import time

lines = []
with open("input.txt") as file:
    for line in file:
        lines.append(line.strip("\n"))

# find start and end
m = len(lines)
n = len(lines[0])
start = [0, 0]
end = [0, 0]
for i in range(m):
    if "S" in lines[i]:
        start[0] = i
        start[1] = lines[i].index("S")
        # lines[i][start[1]] = "a"
    if "E" in lines[i]:
        end[0] = i
        end[1] = lines[i].index("E")
        # lines[i][end[1]] = "z"

height = np.empty((m, n), dtype=int)
for i in range(m):
    for j in range(n):
        height[i, j] = ord(lines[i][j])

# print(lines)

# print(np.max(np.max(height)))
# print(np.min(np.min(height)))

# height[height == ord('S')] = ord('a')
# height[height == ord('E')] = ord('z')

# print(np.max(np.max(height)))
# print(np.min(np.min(height)))

pos_grid = np.zeros((m, n), dtype=bool)
pos_grid[start[0], start[1]] += 1

plt.ion()
fig, ax = plt.subplots()
im = ax.imshow(pos_grid, vmin=0, vmax=1)

# plt.imshow()
# plt.show()

def find_next_position(height, i, j, end):
    dx = end[0] - i
    dy = end[1] - j
    l = sqrt(dx**2 + dy**2)
    dx = float(dx) / l
    dy = float(dy) / l
    
    if abs(dx) > abs(dy):
        return round(i + dx), j
    elif abs(dy) > abs(dx):
        return i, round(j + dy)
    elif abs(dx) == abs(dy):
        return round(i + dx), j
        
    raise RuntimeError

class Node:
    n = None
    m = None
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.children = []

Node.n = n
Node.m = m

i = start[0]
j = start[1]
while True:
    i, j = find_next_position(height, i, j, end)
    print([i, j])
    
    pos_grid[i, j] += 1
    im.set_data(pos_grid)
    fig.canvas.flush_events()
    time.sleep(0.01)
    
    if i == end[0] and j == end[1]:
        break
