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


class Knot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        

knots = [Knot(int(n/2), int(n/2)) for i in range(10)]
tail_grid = np.zeros((n, n), dtype=int)
tail_grid[knots[-1].y, knots[-1].x] += 5

head_grid = np.zeros((n, n), dtype=int)
head_grid[knots[0].y, knots[0].x] += 10

for line in lines:
    move = line.split(" ")
    direction = move[0]
    length = int(move[1])
    
    while length:
        # update head
        if direction == "R":
            knots[0].x += 1
        elif direction == "L":
            knots[0].x -= 1
        elif direction == "D":
            knots[0].y += 1
        elif direction == "U":
            knots[0].y -= 1

        try:
            head_grid[knots[0].y, knots[0].x] += 1
        except:
            raise RuntimeError("Too small grid")

        for head, tail in zip(knots[:-1], knots[1:]):
            # update position
            distance = sqrt((head.x - tail.x)**2 + (head.y - tail.y)**2)
            if distance > sqrt(2):
                # move tail
                dx = head.x - tail.x
                dy = head.y - tail.y
                if dx:
                    tail.x += 1 if dx > 0 else -1
                if dy:
                    tail.y += 1 if dy > 0 else -1
        
        try:
            tail_grid[knots[-1].y, knots[-1].x] += 1
        except:
            raise RuntimeError("Too small grid")
        
        length -= 1

if False:
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    # im = ax.imshow(tail_grid)
    im = ax.imshow(head_grid)
    # ax.grid()
    plt.show()

print(f"Second star: {np.sum(np.sum(tail_grid > 0))}")