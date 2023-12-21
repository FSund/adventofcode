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

def find_area_bfs(map, start, max_steps):
    visited = set() # to keep track of already visited nodes
    # bfs_traversal = list()  # the BFS traversal result
    queue = list()  # queue
    # parent = {}  # dict
    
    total_area = 0
    n_steps = 0
    
    # push the root node to the queue and mark it as visited
    queue.append(start)
    visited.add(start)
    
    # label = map[start[0], start[1], start[2]]
    
    adjacent = (
        ( 1,  0), ( 0,  1), # down and right
        (-1,  0), ( 0, -1), # up and left
    )
    
    # loop until the queue is empty
    while queue:
        # pop the front node of the queue and add it to bfs_traversal
        current_pos, current_steps = queue.pop(0)
        # bfs_traversal.append(current_pos)
        
        # start at max, subtract 1 for each neighbor with matching label
        current_area = 4
        
        # check all the neighbour nodes of the current node
        for translation in adjacent:
            pos = (
                current_pos[0] + translation[0],
                current_pos[1] + translation[1],
            )
            
            # Make sure within range
            if (pos[0] > (map.shape[0] - 1) or pos[0] < 0 
                or pos[1] > (map.shape[1] - 1) or pos[1] < 0
            ):
                continue
        
            # only check free space
            if map[pos[0],pos[1]] != 0:
                continue

            # update area
            current_area -= 1

            # if the neighbour nodes are not already visited, 
            # push them to the queue and mark them as visited
            if pos not in visited:
                visited.add((pos, current_pos[1]))
                queue.append((pos, current_pos[1] + 1))
                # parent[pos] = current_pos

        total_area += current_area

    # print(f"{total_area = }")

    return total_area

final_map = None

@cache
def count_plots(map: tuple[tuple[int]], start: tuple[int, int], n_steps: int):
    if n_steps == 0:
        final_map[start[0], start[1]] = 3
        return 1
    
    neighbors = (
        ( 1,  0), ( 0,  1), # down and right
        (-1,  0), ( 0, -1), # up and left
    )
    
    n = 0
    for neighbor in neighbors:
        pos = (
            start[0] + neighbor[0],
            start[1] + neighbor[1],
        )
        
        # Make sure within range
        if (pos[0] > (len(map) - 1) or pos[0] < 0 
            or pos[1] > (len(map[0]) - 1) or pos[1] < 0
        ):
            continue
    
        # only check free space
        if map[pos[0]][pos[1]] != 0:
            continue
        
        n += count_plots(map, pos, n_steps - 1)
    
    return n

def star1(filename, n_steps=64):
    lines = get_input(filename)
    map = np.zeros((len(lines), len(lines[0])), dtype=int)
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] == "S":
                map[i,j] = 2
                start = (i,j)
            elif lines[i][j] == "#":
                map[i,j] = 1
            elif lines[i][j] == ".":
                map[i,j] = 0
    hashable_map = tuple(tuple(row) for row in map)
    
    global final_map
    final_map = map
    
    n = count_plots(hashable_map, start, n_steps)
    
    m = np.sum(final_map == 3) + 1
    
    return m

def tests():
    pass
    

if __name__ == "__main__":
    tests()

    ans = star1("example.txt", n_steps=6)
    print(f"example star 1: {ans}")
    assert ans == 16, f"wrong answer: {ans}"
    
    ans = star1("input.txt", n_steps=64)
    print(f"star 1: {ans}")
    # assert ans == 16, f"wrong answer: {ans}"
    
    # ans = star1("input.txt")
    # print(f"star 1: {ans}")
    # assert ans == 495298
    
    # ans = star2("example.txt")
    # print(f"example star 2: {ans}")
    # assert ans == 167409079868000
    
    # ans = star2("input.txt")  
    # print(f"star 2: {ans}")
    # assert ans == 132186256794011
