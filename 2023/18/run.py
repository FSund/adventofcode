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
    
    print(f"grid shape: {grid.shape}")
    vol = grid.shape[0] * grid.shape[1] - np.sum((grid == 2))
    return vol

def find_vertices_and_edges(lines):
    pos = [0,0]
    verts = []
    edge_points = []
    for line in lines:
        direction, length = get_instruction(line)
        
        for i in range(length):
            pos[0] += direction[0]
            pos[1] += direction[1]
            edge_points.append(tuple(pos))
        
        # pos[0] += direction[0] * length
        # pos[1] += direction[1] * length
        verts.append(tuple(pos))
    
    # append manhattan movement to the start to avoid diagonal line at the end
    # verts.append((verts[0][0] + pos[0], verts[0][1]))
    
    # add start
    length = pos[0] + pos[1]
    direction = (
        1 if pos[0] < 0 else -1,
        1 if pos[1] < 0 else -1,
    )
    for i in range(length):
        pos[0] += direction[0]
        pos[1] += direction[1]
        edge_points.append(tuple(pos))
    
    verts.append(tuple(pos))
    assert pos[0] == 0 and pos[1] == 0, f"wrong end pos: {pos}"
    
    print(len(edge_points))
    
    return verts

def find_vertices(lines):
    pos = [0,0]
    verts = [tuple(pos)]  # add start
    for line in lines:
        direction, length = get_instruction(line)
        
        pos[0] += direction[0] * length
        pos[1] += direction[1] * length
        verts.append(tuple(pos))

    # # add start
    # verts.append(verts[0])
    
    return verts

def find_vertices2(lines):
    pos = [0,0]
    verts = [tuple(pos)]  # add start
    previous_dir_name = None
    for line in lines:
        direction, dir_name, length = get_instruction_and_dir_name(line)
        
        pos[0] += direction[0] * length
        pos[1] += direction[1] * length
        
        # check next move
        if previous_dir_name is not None:
            if previous_dir_name == "R" and dir_name == "D":
                pos[1] += 1
            elif previous_dir_name == "D" and dir_name == "L":
                pos[0] += 1
            elif previous_dir_name == "L" and dir_name == "U":
                pos[1] -= 1
            elif previous_dir_name == "U" and dir_name == "R":
                pos[0] -= 1
            elif previous_dir_name == "R" and dir_name == "U":
                pos[1] -= 1
            elif previous_dir_name == "D" and dir_name == "R":
                pos[0] -= 1
            elif previous_dir_name == "L" and dir_name == "D":
                pos[1] += 1
            elif previous_dir_name == "U" and dir_name == "L":
                pos[0] += 1
            else:
                raise Exception(f"wrong direction: {previous_dir_name} -> {dir_name}")
        
        verts.append(tuple(pos))

    # # add start
    # verts.append(verts[0])
    
    return verts

def find_vertices_and_extra(lines):
    pos = [0,0]
    verts = [tuple(pos)]  # add start
    down_moves = 0
    left_moves = 0
    for line in lines:
        direction, length = get_instruction(line)
        
        pos[0] += direction[0] * length
        pos[1] += direction[1] * length
        verts.append(tuple(pos))
        
        if direction[0] == 1:
            down_moves += length
        elif direction[1] == -1:
            left_moves += length

    # # add start
    # verts.append(verts[0])
    
    return verts, down_moves, left_moves

def calculate_area(points):
    total_area = 0
    n = len(points)

    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]

        # Check if the line segment is vertical
        if x1 == x2:
            # Calculate area contribution of this segment
            height = y2 - y1
            total_area += x1 * height

    return abs(total_area) // 2  # Divide by 2 to get the actual area


def code_to_instruction(code):
    length = eval(f"0x{code[:5]}")
    direction = eval(f"0x{code[-1]}")
    
    return length, direction

def get_instruction(line):
    direction, length, code = line.split(" ")
    code = code[2:-1]
    length, direction = code_to_instruction(code)
    
    # 0 means R, 1 means D, 2 means L, and 3 means U
    d = {
        0: ( 0, 1),  # right
        1: ( 1, 0),  # down
        2: ( 0,-1),  # left
        3: (-1, 0),  # up
        
    }
    return d[direction], length

def get_instruction_and_dir_name(line):
    direction, length, code = line.split(" ")
    code = code[2:-1]
    length, direction = code_to_instruction(code)
    
    # 0 means R, 1 means D, 2 means L, and 3 means U
    d = {
        0: ( 0, 1),  # right
        1: ( 1, 0),  # down
        2: ( 0,-1),  # left
        3: (-1, 0),  # up
        
    }
    dir_name = {
        0: "R",
        1: "D",
        2: "L",
        3: "U",
    }
    return d[direction], dir_name, length

def shoelace_formula(points):
    """
    https://en.wikipedia.org/wiki/Shoelace_formula
    """
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    A = 1/2 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
    return int(A)
    
    # max_x = max(x)
    # min_x = min(x)
    # min_y = min(y)
    # max_y = max(y)
    # return int(A) + (max_x - min_x) + (max_y - min_y) + 1

def trapezoid_area(points):
    """
    https://en.wikipedia.org/wiki/Trapezoid
    """
    a = 0
    for i in range(len(points) - 1):
        x1 = points[i][0]
        y1 = points[i][1]
        x2 = points[i+1][0]
        y2 = points[i+1][1]
        a += (y1 + y2)*(x1 - x2)
    
    return int(abs(a) / 2)

def plot_path(points):
    import matplotlib.pyplot as plt
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    if points[0] != points[-1]:
        x.append(points[0][0])
        y.append(points[0][1])
    plt.plot(x, y, linewidth=1)
    plt.show()

def star2(filename):
    lines = get_input(filename)
    # verts = find_vertices(lines)
    verts, down_moves, left_moves = find_vertices_and_extra(lines)
    plot_path(verts)
    area = shoelace_formula(verts)
    # area = trapezoid_area(verts)
    # area = calculate_enclosed_area(verts)
    return area + down_moves + left_moves + 1

def tests():
    assert get_instruction("R 6 (#70c710)") == ((0,1), 461937)
    assert get_instruction("D 5 (#0dc571)") == ((1,0), 56407)
    assert get_instruction("L 5 (#8ceee2)") == ((0,-1), 577262)
    assert get_instruction("U 2 (#caa173)") == ((-1,0), 829975)
    
    ans = [
        "#70c710 = R 461937",
        "#0dc571 = D 56407",
        "#5713f0 = R 356671",
        "#d2c081 = D 863240",
        "#59c680 = R 367720",
        "#411b91 = D 266681",
        "#8ceee2 = L 577262",
        "#caa173 = U 829975",
        "#1b58a2 = L 112010",
        "#caa171 = D 829975",
        "#7807d2 = L 491645",
        "#a77fa3 = U 686074",
        "#015232 = L 5411",
        "#7a21e3 = U 500254",
    ]
    for a in ans:
        l, r = a.split(" = ")
        r = r.split(" ")[1]
        length, direction = code_to_instruction(l[1:])
        assert length == int(r), f"wrong length: {length} != {r}"
    
    assert code_to_instruction("000000")[0] == 0
    assert code_to_instruction("000010")[0] == 1
    assert code_to_instruction("000100")[0] == 16
    assert code_to_instruction("0000f0")[0] == 15
    
    points = [
        (0, 0),
        (0, 1),
        (1, 1),
        (1, 0),
    ]
    a = shoelace_formula(points)
    assert a == 4, f"wrong area: {a} != 4"
    points = [
        (0, 0),
        (0, 10),
        (10, 10),
        (10, 0),
    ]
    a = shoelace_formula(points) 
    assert a == 100 + 10 + 10 + 1, f"wrong area: {a} != 120"
    points = [
        (0, 0),
        (0, 10),
        (0, 20),
        (10, 20),
        (10, 10),
        (10, 0),
    ]
    a = shoelace_formula(points)
    assert a == 231, f"wrong area: {a} != 231"
    points = [
        (0,0),
        (10,0),
        (20,0),
        (20,10),
        (10,10),
        (0,10),
    ]
    assert shoelace_formula(points) == 231
    # assert shoelace_formula(points) == trapezoid_area(points)
    
    points = [
        (0,0),
        (0,6),
        (5,6),
        (5,4),
        (7,4),
        (7,6),
        (9,6),
        (9,1),
        (7,1),
        (7,0),
        (5,0),
        (5,2),
        (2,2),
        (2,0),
    ]
    a = shoelace_formula(points)
    # assert a == 62, f"wrong area: {a} != 62"
    

if __name__ == "__main__":
    # tests()

    ans = star1("example.txt")
    print(f"example star 1: {ans}")
    assert ans == 62, f"wrong answer: {ans}"
    
    ans = star1("input.txt")
    print(f"star 1: {ans}")
    assert ans == 56678
    
    ans = star2("example.txt")
    print(f"example star 2: {ans}")
    assert ans == 952408144115
    
    ans = star2("input.txt")  
    print(f"star 2: {ans}")
    assert ans > 79088771669566
    assert ans == 79088855654037
    # 79088771669566 too low
    # 79088855654036
