from dataclasses import dataclass
from functools import cache
import numpy as np
from datetime import datetime
from pathlib import Path
from collections import OrderedDict
import heapq
from collections import deque

def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines

@cache
def step_once(map: tuple[tuple[int]], positions: tuple[tuple[int, int]]):
    """
    0 == free space
    1 == wall
    2 == reachable position
    
    - Count number of reachable positions
    - Make new map
    - Add reachable positions to new map
    - Return new map
    - Return number of reachable positions
    """
    neighbors = (
        ( 1,  0), ( 0,  1), # down and right
        (-1,  0), ( 0, -1), # up and left
    )
    
    n = 0
    out_of_bounds = []
    new_map = np.copy(map)
    new_map[new_map == 2] = 0
    new_positions = []
    for (x, y) in positions:
        for (dx, dy) in neighbors:
            x = x + dx
            y = y + dy
            
            # Skip if out of bounds
            if (x > (len(map) - 1) or x < 0 
                or y > (len(map[0]) - 1) or y < 0
            ):
                out_of_bounds.append((x, y))
                continue
        
            # check free space
            if map[x][y] != 0:
                continue
            
            # # check if 
            # if (x,y) in positions:
            #     continue
            
            # check if already reachable
            if new_map[x][y] == 2:
                continue
            
            n += 1
            new_map[x][y] = 2
            new_positions.append((x,y))
        
        # n += count_plots(map, positions, n_steps - 1)
    
    new_map = tuple(tuple(row) for row in new_map)
    new_positions = tuple(new_positions)
    return n, new_map, out_of_bounds, new_positions

def star2(filename, iterations):
    lines = get_input(filename)
    
    map = np.zeros((len(lines), len(lines[0])), dtype=int)
    positions = []
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] == ".":
                map[i,j] = 0
            elif lines[i][j] == "#":
                map[i,j] = 1
            elif lines[i][j] == "S":
                map[i,j] = 2
                positions.append((i,j))
    positions = tuple(positions)
    map = tuple(tuple(row) for row in map)
    maps = dict()
    for i in range(iterations):
        n, map, out_of_bounds, positions = step_once(map, positions)
        if map in maps:
            print(f"Found loop at iteration {i}")
            break
        maps[map] = i

def tests():
    pass
    

if __name__ == "__main__":
    tests()
    
    ans = star2("example.txt", 100)
    # print(f"example star 2: {ans}")
    # assert ans == 167409079868000
    
    ans = star2("input.txt", 500)  
    # print(f"star 2: {ans}")
    # assert ans == 132186256794011
