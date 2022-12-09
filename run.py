import numpy as np
from math import sqrt, copysign

n = 1000
tail_grid = np.zeros((n, n), dtype=int)
head_grid = np.zeros((n, n), dtype=int)

lines = []
with open("input.txt") as file:
    for line in file:
        lines.append(line.strip("\n"))

# head and tail start at the same position
hx = int(n/2)
hy = int(n/2)
tx = int(n/2)
ty = int(n/2)

head_grid[hx, hy] += 10
tail_grid[tx, ty] += 10

for line in lines:
    move = line.split(" ")
    direction = move[0]
    length = int(move[1])
    
    while length:
        # update head
        # to_update += sign
        
        if direction == "R":
            hx += 1
        elif direction == "L":
            hx -= 1
        elif direction == "D":
            hy += 1
        elif direction == "U":
            hy -= 1
        
        if hx >= n or hy >= n or hx < 0 or hy < 0:
            raise RuntimeError("Too small grid")
        head_grid[hy, hx] += 1
        
        # update tail
        distance = sqrt((hx - tx)**2 + (hy - ty)**2)
        if distance > sqrt(2):
            # move tail
            dx = hx - tx
            dy = hy - ty
            if dx:
                tx += 1 if dx > 0 else -1
            if dy:
                ty += 1 if dy > 0 else -1
            
            if tx >= n or ty >= n or tx < 0 or ty < 0:
                raise RuntimeError("Too small grid")
        
            tail_grid[ty, tx] += 1
        
        length -= 1

if False:
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    im = ax.imshow(tail_grid)
    # im = ax.imshow(head_grid)
    # ax.grid()
    plt.show()

# print(tail_grid)
print(f"First star: {np.sum(np.sum(tail_grid > 0))}")
