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

def visualize_path(grid):
    for row in range(len(grid)):
        line = []
        for col in range(len(grid[0])):
            if grid[row][col] == 0:
                line.append(".")
            elif grid[row][col] == 1:
                line.append("#")
            elif grid[row][col] == 2:
                line.append("o")
        print("".join(line))

def flood_fill(_im, start_pos=(0, 0), fill_value=2):
    im = np.copy(_im)
    pos = start_pos
    stack = [pos]
    while len(stack) > 0:
        pos = stack.pop()
        im[pos] = fill_value
        for delta in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_pos = (pos[0] + delta[0], pos[1] + delta[1])
            if new_pos[0] < 0 or new_pos[0] >= im.shape[0] or new_pos[1] < 0 or new_pos[1] >= im.shape[1]:
                # out of bounds
                continue
            if im[new_pos] == 0:
                stack.append(new_pos)
    return im

def star1(filename):
    lines = get_input(filename)
    directions = {
        "R": (0, 1),  # right
        "D": (1, 0),  # down
        "L": (0, -1),  # left
        "U": (-1, 0),  # up
    }
    
    grid = np.zeros((20, 20), dtype=int)
    pos = [0,0]
    for line in lines:
        direction, length, color = line.split(" ")
        for i in range(int(length)):
            # pos += directions[direction]
            pos[0] += directions[direction][0]
            pos[1] += directions[direction][1]
            # print(pos)
            if pos[0] >= grid.shape[0] or pos[1] >= grid.shape[1]:
                # add row to the end
                grid = np.vstack((grid, np.zeros((1, grid.shape[1]), dtype=bool)))
                # add column to the end
                grid = np.hstack((grid, np.zeros((grid.shape[0], 1), dtype=bool)))
            if pos[0] < 0 or pos[1] < 0:
                # add row to the beginning
                grid = np.vstack((np.zeros((1, grid.shape[1]), dtype=bool), grid))
                # add column to the beginning
                grid = np.hstack((np.zeros((grid.shape[0], 1), dtype=bool), grid))
                
                # fix pos
                pos[0] += 1
                pos[1] += 1

            grid[pos[0], pos[1]] = True
    
    grid = np.pad(grid, pad_width=1)
    grid = flood_fill(grid, (0, 0))
    # visualize_path(grid)
    
    vol = grid.shape[0] * grid.shape[1] - np.sum((grid == 2))
    return vol

def tests():
    pass

if __name__ == "__main__":
    tests()

    ans = star1("example.txt")
    print(f"example star 1: {ans}")
    assert ans == 62, f"wrong answer: {ans}"
    
    ans = star1("input.txt")
    print(f"star 1: {ans}")
    # assert ans == 1044
    # # 1078 too high
    # # 1077 too high
    
    # ans = star2("example.txt")
    # print(f"example star 2: {ans}")
    # assert ans == 94
    
    # ans = star2("input.txt")
    # print(f"star 2: {ans}")
    # # # assert example == 145
    
    # # 7792 too low
    