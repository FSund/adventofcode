import numpy as np
import matplotlib.pyplot as plt


def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


# from enum import IntEnum

# # class syntax
# class Obj(IntEnum):
#     EMPTY = 0
#     WALL = 1
#     ROBOT = 2
#     BOX = 3


EMPTY = 0
WALL = 1
ROBOT = 2
BOX = 3


def parse_input(filename):
    lines = get_input(filename)
    
    grid = np.zeros((len(lines[0]), len(lines[0])), dtype=int)
    robot = None
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if lines[i][j] == "#":
                grid[i, j] = WALL
            elif lines[i][j] == ".":
                grid[i, j] = EMPTY
            elif lines[i][j] == "O":
                grid[i, j] = BOX
            elif lines[i][j] == "@":
                grid[i, j] = ROBOT
                robot = (i, j)
    
    moves = []
    for i in range(grid.shape[0] + 1, len(lines)):
        for j in range(len(lines[i])):
            moves.append(lines[i][j])
    
    return grid, robot, moves

MOVES = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1),
}

def move_robot(grid, robot, move):
    i, j = robot
    i += MOVES[move][0]
    j += MOVES[move][1]
    
    n_boxes = 0
    while True:
        if i < 0 or i >= grid.shape[0] or j < 0 or j >= grid.shape[1]:
            return robot
        elif grid[i, j] == BOX:
            n_boxes += 1
        elif grid[i, j] == WALL:
            return robot
        elif grid[i, j] == EMPTY:
            break

        i += MOVES[move][0]
        j += MOVES[move][1]
    
    # backtrack while moving boxes
    assert grid[i, j] == EMPTY
    for k in range(n_boxes):
        grid[i, j] = BOX
        i -= MOVES[move][0]
        j -= MOVES[move][1]
    
    # move robot
    i, j = robot
    grid[i, j] = EMPTY
    i += MOVES[move][0]
    j += MOVES[move][1]
    grid[i, j] = ROBOT
    
    return (i, j)
    

def calc_score(grid):
    score = 0
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == BOX:
                score += 100 * i + j
            
    return score


def aoc(filename, star2=False):
    grid, robot, moves = parse_input(filename)
    
    for move in moves:
        robot = move_robot(grid, robot, move)

    print(grid)
    return calc_score(grid)


def tests():
    ans = aoc("example.txt")
    print(f"example star 1: {ans}")
    assert ans == 10092, f"wrong answer: {ans}"
    
    # ans = aoc("example.txt", star2=True)
    # print(f"example star 2: {ans}")
    # assert ans == 1206, f"wrong answer: {ans}"

if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"star 1: {ans}")
    assert ans == 1429911
    
    ans = aoc("input.txt", star2=True)
    print(f"star 2: {ans}")
    # 71922170897884 too low
    # assert ans == 1344
