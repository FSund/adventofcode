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
LEFT_BOX = 3
RIGHT_BOX = 4


def parse_input(filename):
    lines = get_input(filename)
    
    # make everything twice as _wide_
    n, m = len(lines[0]), len(lines[0])
    grid = np.zeros((n, m * 2), dtype=int)
    robot = None
    for i in range(n):
        for j in range(m):
            if lines[i][j] == "#":
                grid[i, j * 2] = WALL
                grid[i, j * 2 + 1] = WALL
            elif lines[i][j] == ".":
                grid[i, j * 2] = EMPTY
                grid[i, j * 2 + 1] = EMPTY
            elif lines[i][j] == "O":
                grid[i, j * 2] = LEFT_BOX
                grid[i, j * 2 + 1] = RIGHT_BOX
            elif lines[i][j] == "@":
                grid[i, j * 2] = ROBOT
                grid[i, j * 2 + 1] = EMPTY
                robot = (i, j * 2)
    
    moves = []
    for i in range(grid.shape[0] + 1, len(lines)):
        for j in range(len(lines[i])):
            moves.append(lines[i][j])
    
    return grid, robot, moves

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

MOVES = {
    "^": UP,
    "v": DOWN,
    "<": LEFT,
    ">": RIGHT,
}

# recursive
# def can_move(grid, pos, move):
#     i0, j0 = pos
#     i = i0 + MOVES[move][0]
#     j = j0 + MOVES[move][1]

#     if grid[i, j] == LEFT_BOX:
#         return (
#             can_move(grid, (i, j), move)  # left half
#             and can_move(grid, (i, j+1), move)  # right half
#         )
#     elif grid[i, j] == RIGHT_BOX:
#         return (
#             can_move(grid, (i, j-1), move)  # left half
#             and can_move(grid, (i, j), move)  # right half
#         )
#     elif grid[i, j] == EMPTY:
#         return True
#     elif grid[i, j] == WALL:
#         return False

# recursive function
# def do_move(grid, pos, move):
#     i0, j0 = pos
#     i = i0 + MOVES[move][0]
#     j = j0 + MOVES[move][1]
    
#     if grid[i, j] == LEFT_BOX:
#         if can_move(grid, (i, j), move) and can_move(grid, (i, j+1), move):
#             # do the move
#             # grid[i0, j0] = EMPTY  # not sure if this is necessary?
#             # grid[i0, j0+1] = EMPTY
#             grid[i, j] = LEFT_BOX  # is already LEFT_BOX....
#             grid[i, j+1] = RIGHT_BOX
            
#             return True
#     elif grid[i, j] == RIGHT_BOX:
#         if can_move(grid, (i, j-1), move) and can_move(grid, (i, j), move):
#             # do the move
#             grid[i0, j0-1] = EMPTY  # not sure if this is necessary?
#             grid[i0, j0] = EMPTY
#             grid[i, j-1] = LEFT_BOX
#             grid[i, j] = RIGHT_BOX
            
#             return True
#     elif grid[i, j] == EMPTY:
#         # do the move
#         grid[i, j] = grid[i0, j0]
#         grid[i0, j0] = EMPTY
#         return True
#     elif grid[i, j] == WALL:
#         return False

# recursive function
def do_move(grid, pos, move, what):
    i0, j0 = pos
    i = i0 + MOVES[move][0]
    j = j0 + MOVES[move][1]
    
    if grid[i, j] == EMPTY:
        grid[i0, j0] = EMPTY
        grid[i, j] = what
    elif grid[i, j] == LEFT_BOX:
        do_move(grid, (i, j), move, LEFT_BOX) and do_move(grid, (i, j+1), move, RIGHT_BOX)
        grid[i0, j0] = EMPTY
        grid[i, j] = what
    elif grid[i, j] == RIGHT_BOX:
        do_move(grid, (i, j-1), move, LEFT_BOX) and do_move(grid, (i, j), move, RIGHT_BOX)
        grid[i0, j0] = EMPTY
        grid[i, j] = what
    elif grid[i, j] == WALL:
        raise RuntimeError("Moving into wall, you should have checked this already!")


# recursive function
def can_move(grid, pos, move, what):
    i0, j0 = pos
    i = i0 + MOVES[move][0]
    j = j0 + MOVES[move][1]
    
    # trying to move object at (i0, j0) into (i, j)
    if grid[i, j] == EMPTY:
        return True
    elif grid[i, j] == LEFT_BOX:
        if move == '<':
            # if trying to move something left into LEFT_BOX
            # check if we can move LEFT_BOX to the left
            return can_move(grid, (i, j), move, LEFT_BOX)
        elif move == '>':
            # if trying to move something right into LEFT_BOX
            # check if we can move right half of box to the right
            print("Check if we can move RIGHT_BOX right")
            return can_move(grid, (i, j+1), move, RIGHT_BOX)
        else:
            # up or down
            return can_move(grid, (i, j), move, LEFT_BOX) and can_move(grid, (i, j+1), move, RIGHT_BOX)
    elif grid[i, j] == RIGHT_BOX:
        if move == '<':
            return can_move(grid, (i, j-1), move, LEFT_BOX)
        elif move == '>':
            print("Check if we can move RIGHT_BOX right")
            return can_move(grid, (i, j), move, RIGHT_BOX)
        else:
            # up or down
            return can_move(grid, (i, j-1), move, LEFT_BOX) and can_move(grid, (i, j), move, RIGHT_BOX)
    elif grid[i, j] == WALL:
        # trying to move into wall
        return False


# def move_robot(grid, robot, move):
#     i, j = robot
#     i += MOVES[move][0]
#     j += MOVES[move][1]
    
#     n_boxes = 0
#     while True:
#         if i < 0 or i >= grid.shape[0] or j < 0 or j >= grid.shape[1]:
#             return robot
#         elif grid[i, j] == BOX:
#             n_boxes += 1
#         elif grid[i, j] == WALL:
#             return robot
#         elif grid[i, j] == EMPTY:
#             break

#         i += MOVES[move][0]
#         j += MOVES[move][1]
    
#     # backtrack while moving boxes
#     assert grid[i, j] == EMPTY
#     for k in range(n_boxes):
#         grid[i, j] = BOX
#         i -= MOVES[move][0]
#         j -= MOVES[move][1]
    
#     # move robot
#     i, j = robot
#     grid[i, j] = EMPTY
#     i += MOVES[move][0]
#     j += MOVES[move][1]
#     grid[i, j] = ROBOT
    
#     return (i, j)
    

# def can_move(grid, robot, move):
#     i, j = robot
#     i += MOVES[move][0]
#     j += MOVES[move][1]

#     n_boxes = 0
#     while True:
#         if i < 0 or i >= grid.shape[0] or j < 0 or j >= grid.shape[1]:
#             return False
#         elif grid[i, j] == BOX:
#             n_boxes += 1
#         elif grid[i, j] == WALL:
#             return False
#         elif grid[i, j] == EMPTY:
#             return True

#         i += MOVES[move][0]
#         j += MOVES[move][1]


def calc_score(grid):
    score = 0
    m_half = int(grid.shape[1]/2)
    for i in range(grid.shape[0]):
        for j in range(m_half):
            if grid[i, j] == LEFT_BOX:
                score += 100 * i + j
        
        for j in range(m_half, grid.shape[1]):
            if grid[i, j] == RIGHT_BOX:
                score += 100 * i + j
            
    return score


def aoc(filename):
    grid, robot, moves = parse_input(filename)
    print(grid)
    for move in moves:
        if can_move(grid, robot, move, ROBOT):
            # print(f"move {move} is OK")
            do_move(grid, robot, move, ROBOT)
            robot = (
                robot[0] + MOVES[move][0],
                robot[1] + MOVES[move][1],
            )
        print(grid)

    # print(grid)
    return calc_score(grid)


def tests():
    grid = np.zeros((5,5))
    grid[2,2] = ROBOT
    assert can_move(grid, (2,2), '^', ROBOT)
    assert can_move(grid, (2,2), 'v', ROBOT)
    assert can_move(grid, (2,2), '<', ROBOT)
    assert can_move(grid, (2,2), '>', ROBOT)
    
    grid = np.zeros((5,5))
    grid[2,2] = ROBOT
    grid[np.array([
        (1,1), (1,2), (1,3),
        (2,1),        (2,3),
        (3,1), (3,2), (3,3),
    ])] = WALL
    assert not can_move(grid, (2,2), '^', ROBOT)
    assert not can_move(grid, (2,2), 'v', ROBOT)
    assert not can_move(grid, (2,2), '<', ROBOT)
    assert not can_move(grid, (2,2), '>', ROBOT)
    
    grid = np.zeros((5,5))
    grid[0,0] = ROBOT
    grid[0,1] = LEFT_BOX
    grid[0,2] = RIGHT_BOX
    assert can_move(grid, (0,0), '>', ROBOT)  # recursion depth error
    
    grid = np.zeros((5,5))
    grid[0,4] = ROBOT
    grid[0,3] = RIGHT_BOX
    grid[0,2] = LEFT_BOX
    assert can_move(grid, (0,4), '<', ROBOT)
    
    ans = aoc("example.txt")
    print(f"example star 2: {ans}")
    assert ans == 9021, f"wrong answer: {ans}"

if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"star 2: {ans}")
    # 71922170897884 too low
    # assert ans == 1344
