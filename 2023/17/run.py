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

def visualize_path(grid, path):
    for row in range(len(grid)):
        line = []
        for col in range(len(grid[0])):
            if (row, col) in path:
                line.append("X")
            elif grid[row][col] == 0:
                line.append("#")
            else:
                line.append(".")
        print("".join(line))

def shortest_path_with_constraints(grid, target=None):
    rows, cols = len(grid), len(grid[0])
    start = (0, 0, 0, 0)  # (row, col, direction, consecutive_moves)
    queue = [(0, start, [])]  # (total cost, current node, current path)
    visited = set()
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    if target is None:
        target = (rows - 1, cols - 1)

    while queue:
        cost, (row, col, direction, consecutive_moves), path = heapq.heappop(queue)

        if (row, col, direction, consecutive_moves) in visited:
            continue
        
        visited.add((row, col, direction, consecutive_moves))

        if row == target[0] and col == target[1]:
            return cost, path + [(row, col)]
        
        for i in range(len(directions)):
            new_row = row + directions[i][0]
            new_col = col + directions[i][1]
            new_direction = i

            if 0 <= new_row < rows and 0 <= new_col < cols and new_direction != (direction + 2) % 4:
                new_cost = cost + grid[new_row][new_col]
                new_consecutive_moves = consecutive_moves + 1 if direction == new_direction else 1
                
                if new_consecutive_moves <= 3:
                    new_path = path + [(row, col)]  # Append current position to the path
                    heapq.heappush(queue, (new_cost, (new_row, new_col, new_direction, new_consecutive_moves), new_path))


def ultra_crucible(grid, target=None):
    rows, cols = len(grid), len(grid[0])
    # start = (0, 0, 0, 0)  # (row, col, direction, consecutive_moves)
    # queue = [(0, start, ())]  # (total cost, current node, current path)
    
    queue = [
        # (total cost, current node, current path)
        (0, (0,0,0,0), ()),  # right
        (0, (0,0,1,0), ()),  # down
    ]
    visited = set()
    max_consecutive_moves = 10
    min_consecutive_moves = 4
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    if target is None:
        target = (rows - 1, cols - 1)

    while queue:
        cost, (row, col, direction, consecutive_moves), path = heapq.heappop(queue)
        # print(f"{row = }, {col = }, {path = }")
        # print(f"{consecutive_moves = }, {path = }")

        if (row, col, direction, consecutive_moves) in visited:
            # if (row, col, path) in visited:
            continue
        
        visited.add((row, col, direction, consecutive_moves))
        # visited.add((row, col, path))

        if row == target[0] and col == target[1]:
            return cost, path + ((row, col),)
        
        # need to move a minimum of 4 times in the same direction before it can turn
        # can to move a maximum of 10 times in the same direction before it must turn
        for i in range(len(directions)):
            new_row = row + directions[i][0]
            new_col = col + directions[i][1]
            new_direction = i

            if 0 <= new_row < rows and 0 <= new_col < cols and new_direction != (direction + 2) % 4:
                new_cost = cost + grid[new_row][new_col]
                new_consecutive_moves = consecutive_moves + 1 if direction == new_direction else 1
                
                new_path = path + ((row, col),)
                
                # can only change direction if consecutive moves is between min_consecutive_moves and max_consecutive_moves
                if new_direction != direction:
                    if min_consecutive_moves <= consecutive_moves <= max_consecutive_moves:
                        heapq.heappush(queue, (new_cost, (new_row, new_col, new_direction, new_consecutive_moves), new_path))
                else:  # new_direction == direction
                    if new_consecutive_moves <= max_consecutive_moves:
                        heapq.heappush(queue, (new_cost, (new_row, new_col, new_direction, new_consecutive_moves), new_path))


def to_int(_lines):
    lines = []
    for line in _lines:
        lines.append([])
        for c in line:
            lines[-1].append(int(c))
            
    return lines

def star1(filename):
    lines = get_input(filename)
    lines = to_int(lines)
    # print(lines)
    
    cost, path = shortest_path_with_constraints(lines)
    # for node in path:
    #     print(node)
    return cost

def star2(filename):
    lines = get_input(filename)
    lines = to_int(lines)
    # print(lines)
    
    cost, path = ultra_crucible(lines)
    cost2 = 0
    for node in path[1:]:
        cost2 += lines[node[0]][node[1]]
    assert cost == cost2, f"wrong cost: {cost} != {cost2}"
    return cost

def tests():
    # grid = [
    #     [1, 2, 3, 4],
    #     [5, 6, 7, 8],
    #     [9, 10, 11, 12],
    #     [13, 14, 15, 16]
    # ]
    # print(shortest_path_with_constraints(grid))
    
    lines = get_input("example.txt")
    lines = to_int(lines)
    cost, path = shortest_path_with_constraints(lines, target=(0,8))  # (0, 8) fails
    # assert cost == 29, f"wrong cost: {cost}"
    # print(f"{cost = }")
    # visualize_path(lines, path)
    # print(f"{path=}")
    cost = []
    for node in path[1:]:
        cost += [lines[node[0]][node[1]]]
        # print(f"{node}, cost: {cost}, total cost: {sum(cost)}")
    
    # from example
    p = [
        (0,0),
        (0,1),
        (0,2),
        (1,2),
        (1,3),
        (1,4),
        (1,5),
        (0,5),
        (0,6),
        (0,7),
        (0,8),
        (1,8),
        (2,8),
        (2,9),
        (2,10),
        (3,10),
        (4,10),
        (4,11),
        (5,11),
        (6,11),
        (7,11),
        (7,12),
        (8,12),
        (9,12),
        (10,12),
        (10,11),
        (11,11),
        (12,11),
        (12,12),
    ]
    lines = get_input("example.txt")
    lines = to_int(lines)
    cost, path = shortest_path_with_constraints(lines, target=(1,5))
    for i in range(len(path)):
        assert path[i] == p[i], f"wrong path: {path[i]} != {p[i]}"
        
    cost, path = shortest_path_with_constraints(lines)
    assert cost == 102, f"wrong cost: {cost}"
    # visualize_path(lines, path)
    # for i in range(len(path)):
    #     assert path[i] == p[i], f"wrong path at step {i}: {path[i]} != {p[i]}"
    
    # visualize_path(lines, path)
    
    
    lines = get_input("example.txt")
    lines = to_int(lines)
    cost, path = ultra_crucible(lines)
    visualize_path(lines, path)
    assert cost == 94, f"wrong cost: {cost}"
    
    lines = [
        "111111111111", 
        "999999999991", 
        "999999999991", 
        "999999999991", 
        "999999999991", 
    ]
    lines = to_int(lines)
    cost, path = ultra_crucible(lines)
    print()
    visualize_path(lines, path)
    
    # assert cost == 71, f"wrong cost: {cost}"

if __name__ == "__main__":
    tests()

    ans = star1("example.txt")
    print(f"example star 1: {ans}")
    assert ans == 102, f"wrong answer: {ans}"
    
    ans = star1("input.txt")
    print(f"star 1: {ans}")
    assert ans == 1044
    # 1078 too high
    # 1077 too high
    
    ans = star2("example.txt")
    print(f"example star 2: {ans}")
    assert ans == 94
    
    ans = star2("input.txt")
    print(f"star 2: {ans}")
    # # assert example == 145
    
    # 7792 too low
    