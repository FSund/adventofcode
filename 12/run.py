import numpy as np
import matplotlib.pyplot as plt
from astar import astar, find_a_bfs

if __name__ == "__main__":
    lines = []
    with open("input.txt") as file:
        for line in file:
            lines.append(line.strip("\n"))

    # find start and end
    m = len(lines)
    n = len(lines[0])
    start = None
    end = None
    for i in range(m):
        if "S" in lines[i]:
            # start[0] = i
            # start[1] = lines[i].index("S")
            start = (i, lines[i].index("S"))
            # lines[i][start[1]] = "a"
        if "E" in lines[i]:
            # end[0] = i
            # end[1] = lines[i].index("E")
            end = (i, lines[i].index("E"))
            # lines[i][end[1]] = "z"

    height = np.empty((m, n), dtype=int)
    for i in range(m):
        for j in range(n):
            height[i, j] = ord(lines[i][j])

    height[height == ord('S')] = ord('a')
    height[height == ord('E')] = ord('z')

    maze = np.zeros((m, n), dtype=int)

    def heuristic(parent, child):
        # h(n) is a heuristic function that estimates the cost of the
        # cheapest path from n to the goal
        dx = end[0] - child.position[0]
        dy = end[1] - child.position[1]
        
        # L2 norm
        # return (dx ** 2) + (dy ** 2)
        
        # L1 norm -- use this for star 1
        return abs(dx) + abs(dy)
        
        # use this for star 2?
        # return 1

    # star 1
    if False:
        path = astar(maze, height, start, end, viz=False, heuristic=heuristic)
        print(f"Star 1: {len(path[1:])}")
    
    # star 2
    start2 = (end[0], end[1])
    end2 = (start[0], start[1])
    
    if True:
        path = find_a_bfs(maze, height, start2, viz=1)
        # print(path)
        print(f"Star 2: {len(path)-1}")
        
        grid = np.zeros((len(maze), len(maze[0])))
        for p in path:
            grid[p[0], p[1]] += 1
        
        plt.ion()
        fig, ax = plt.subplots()
        im = ax.imshow(grid)
        
        fig, ax = plt.subplots()
        im = ax.imshow(height)
        
        plt.show()
        plt.pause(5)
    
    print(len(height == ord('a')))
