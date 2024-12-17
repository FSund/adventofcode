import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple


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
def can_move(grid, pos, move, what, new_grid = None, moves=[]):
    # (i0, j0) is the position of the object we are trying to move
    i0, j0 = pos
    
    # (i, j) is the destination of the move
    i = i0 + MOVES[move][0]
    j = j0 + MOVES[move][1]
    
    # grid[i0, j0] should be equal to `what`
    assert grid[i0, j0] == what
    
    # trying to move object at (i0, j0) into (i, j)
    if grid[i, j] == EMPTY:
        moves.append(((i0, j0), (i, j), what))
        if new_grid is not None:
            new_grid[i, j] = what
            new_grid[i0, j0] = EMPTY
            # print(new_grid)
        return True
    elif grid[i, j] == LEFT_BOX:
        if move == '<':
            # if trying to move something left into LEFT_BOX
            # check if we can move LEFT_BOX to the left
            assert what == RIGHT_BOX
            if can_move(grid, (i, j), move, LEFT_BOX, new_grid, moves):  # moves  LEFT_BOX at (i, j) to the left (to (i, j-1))
                if new_grid is not None:
                    new_grid[i, j] = what
                    new_grid[i0, j0] = EMPTY
                    # print(new_grid)
                moves.append(((i0, j0), (i, j), what))
                moves.append(((i, j), (i, j-1), LEFT_BOX))
                return True
            else:
                return False
        elif move == '>':
            # if trying to move something right into LEFT_BOX
            # check if we can move right half of box to the right
            assert what != LEFT_BOX
            if can_move(grid, (i, j+1), move, RIGHT_BOX, new_grid, moves):  # moves RIGHT_BOX at (i, j+1) to the right (to (i, j+2))
                if new_grid is not None:
                    new_grid[i, j+1] = grid[i, j]
                    new_grid[i, j] = what
                    new_grid[i0, j0] = EMPTY
                    # print(new_grid)
                    moves.append(((i0, j0), (i, j), what))
                    moves.append(((i, j+1), (i, j+2), RIGHT_BOX))
                return True
            else:
                return False
        else:
            # up or down
            if can_move(grid, (i, j), move, LEFT_BOX, new_grid, moves) and can_move(grid, (i, j+1), move, RIGHT_BOX, new_grid, moves):
                if new_grid is not None:
                    new_grid[i, j] = what
                    new_grid[i0, j0] = EMPTY
                    moves.append(((i0, j0), (i, j), what))
                    moves.append(((i, j), (i, j-1), LEFT_BOX))
                return True
            else:
                return False
    elif grid[i, j] == RIGHT_BOX:
        if move == '<':
            # trying to move something left into RIGHT_BOX
            assert what != LEFT_BOX
            if can_move(grid, (i, j-1), move, LEFT_BOX, new_grid, moves):  # moves LEFT_BOX at (i, j-1) to the left (to (i, j-2))
                if new_grid is not None:
                    new_grid[i, j-1] = grid[i, j]
                    new_grid[i, j] = what
                    new_grid[i0, j0] = EMPTY
                    # print(new_grid)
                    moves.append(((i0, j0), (i, j), what))
                    moves.append(((i, j-1), (i, j-2), LEFT_BOX))
                return True
            else:
                return False
        elif move == '>':
            # trying to move something right into RIGHT_BOX
            assert what == LEFT_BOX
            if can_move(grid, (i, j), move, RIGHT_BOX, new_grid, moves):
                if new_grid is not None:
                    new_grid[i, j] = what
                    new_grid[i0, j0] = EMPTY
                    moves.append(((i0, j0), (i, j), what))
                    moves.append(((i, j), (i, j+1), RIGHT_BOX))
                return True
            else:
                return False
        else:
            # up or down
            if can_move(grid, (i, j-1), move, LEFT_BOX, new_grid, moves) and can_move(grid, (i, j), move, RIGHT_BOX, new_grid, moves):
                if new_grid is not None:
                    new_grid[i, j] = what
                    new_grid[i0, j0] = EMPTY
                    moves.append(((i0, j0), (i, j), what))
                    moves.append(((i, j-1), (i, j-2), LEFT_BOX))
                return True
            else:
                return False
    elif grid[i, j] == WALL:
        # trying to move into wall
        return False



# recursive function
def get_move_set(grid, pos, move_str, what, empty_after: set, new_positions: set):
    # (i0, j0) is the position of the object we are trying to move
    i0, j0 = pos
    
    # (i, j) is the destination of the move
    i = i0 + MOVES[move_str][0]
    j = j0 + MOVES[move_str][1]
    
    # grid[i0, j0] should be equal to `what`
    assert grid[i0, j0] == what
    
    # trying to move object at (i0, j0) into (i, j)
    if grid[i, j] == EMPTY:
        # move `what` into (i, j)
        empty_after.add((i0, j0))
        new_positions.add(((i, j), what))
        return True
    elif grid[i, j] == LEFT_BOX:
        if move_str == '<':
            # if trying to move something left into LEFT_BOX
            # check if we can move LEFT_BOX to the left
            assert what == RIGHT_BOX
            if get_move_set(grid, (i, j), move_str, LEFT_BOX, empty_after, new_positions):  # moves LEFT_BOX at (i, j) to the left (to (i, j-1))
                # move `what` into (i, j)
                empty_after.add((i0, j0))
                new_positions.add(((i, j), what))
                return True
            else:
                return False
        elif move_str == '>':
            # if trying to move something right into LEFT_BOX
            # check if we can move right half of box to the right
            assert what != LEFT_BOX
            if (
                # get_move_set(grid, (i, j), move_str, LEFT_BOX, empty_after, new_positions)  # moves LEFT_BOX at (i, j) to the right (to (i, j+1))
                # and
                get_move_set(grid, (i, j+1), move_str, RIGHT_BOX, empty_after, new_positions)  # moves RIGHT_BOX at (i, j+1) to the right (to (i, j+2))
            ):
                # move LEFT_BOX at (i, j) to the right
                empty_after.add((i, j))
                new_positions.add(((i, j+1), LEFT_BOX))
                
                # move `what` into (i, j)
                empty_after.add((i0, j0))
                new_positions.add(((i, j), what))
                return True
            else:
                return False
        else:
            # up or down
            # check if we can move LEFT_BOX and RIGHT_BOX above or below
            if (
                get_move_set(grid, (i, j), move_str, LEFT_BOX, empty_after, new_positions)
                and
                get_move_set(grid, (i, j+1), move_str, RIGHT_BOX, empty_after, new_positions)
            ):
                # move `what` into (i, j)
                empty_after.add((i0, j0))
                new_positions.add(((i, j), what))
                return True
            else:
                return False
    elif grid[i, j] == RIGHT_BOX:
        if move_str == '<':
            # trying to move something left into RIGHT_BOX
            assert what != RIGHT_BOX
            # check if we can move LEFT_BOX at (i, j-1) to the left, to (i, j-2)
            if get_move_set(grid, (i, j-1), move_str, LEFT_BOX, empty_after, new_positions):  # moves LEFT_BOX at (i, j-1) to the left (to (i, j-2))
                # move RIGHT_BOX at (i, j) to the left
                empty_after.add((i, j))
                new_positions.add(((i, j-1), RIGHT_BOX))

                # move `what` into (i, j)
                empty_after.add((i0, j0))
                new_positions.add(((i, j), what))
                return True
            else:
                return False
        elif move_str == '>':
            # trying to move something right into RIGHT_BOX
            assert what == LEFT_BOX
            if get_move_set(grid, (i, j), move_str, RIGHT_BOX, empty_after, new_positions):
                # move `what` into (i, j)
                empty_after.add((i0, j0))
                new_positions.add(((i, j), what))
                return True
            else:
                return False
        else:
            # up or down
            # check if we can move LEFT_BOX and RIGHT_BOX above or below
            if (
                get_move_set(grid, (i, j), move_str, RIGHT_BOX, empty_after, new_positions)
                and
                get_move_set(grid, (i, j-1), move_str, LEFT_BOX, empty_after, new_positions)
            ):
                # move `what` into (i, j)
                empty_after.add((i0, j0))
                new_positions.add(((i, j), what))
                return True
            else:
                return False
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
    # n_half = int(grid.shape[0]/2)
    # m_half = int(grid.shape[1]/2)

    # for i in range(grid.shape[0]):
    #     for j in range(n_half):
    #         if grid[i, j] == LEFT_BOX:
    #             if i >= n_half:
    #                 score += 100 * (grid.shape[0] - 1 - i) + j
    #             else:
    #                 score += 100 * i + j
        
    #     for j in range(m_half, grid.shape[1]):
    #         if grid[i, j] == RIGHT_BOX:
    #             if i >= n_half:
    #                 score += 100 * (grid.shape[0] - 1 - i) + (grid.shape[1] - 1 - j)
    #             else:
    #                 score += 100 * i + (grid.shape[1] - 1 - j)

    # boxes = []
    # for i in range(grid.shape[0]):
    #     for j in range(grid.shape[1]):
    #         if grid[i, j] == LEFT_BOX:
    #             boxes.append((i, j))
    
    # for box in boxes:
    #     i0, j0 = box
    #     j1 = j0 + 1
        
    #     # if i0 >= n_half:
    #     #     score += 100 * (grid.shape[0] - 1 - i0)
    #     # else:
    #     #     score += 100 * i0
        
    #     # 100 times distance from top edge
    #     score += 100 * i0

    #     # distance from closest edge left/right
    #     if j1 >= m_half:
    #         score += (grid.shape[1] - j1 - 1)
    #     else:
    #         score += j0
    
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == LEFT_BOX:
                score += 100 * i + j
            
    return score


def aoc(filename):
    grid, robot, moves = parse_input(filename)
    print(grid)
    for move in moves:
        # new_grid = np.copy(grid)
        # if can_move(grid, robot, move, ROBOT, new_grid):
        #     # print(f"move {move} is OK")
        #     # do_move(grid, robot, move, ROBOT)
            
        #     new_grid[robot[0], robot[1]] = EMPTY
        #     robot = (
        #         robot[0] + MOVES[move][0],
        #         robot[1] + MOVES[move][1],
        #     )
        #     grid = new_grid
        #     grid[robot[0], robot[1]] = ROBOT
        # print(grid)
        
        # moves = []
        # if can_move(grid, robot, move, ROBOT, None, moves):
        #     for move in moves:
        #         i0, j0 = move[0]
        #         grid[i0, j0] = EMPTY
        #     for move in moves:
        #         i, j = move[1]
        #         what = move[2]
        #         grid[i, j] = what
        
        empty_after = set()
        new_positions = set()
        if get_move_set(grid, robot, move, ROBOT, empty_after, new_positions):
            robot = (
                robot[0] + MOVES[move][0],
                robot[1] + MOVES[move][1],
            )
            # grid[robot[0], robot[1]] = ROBOT
            for e in empty_after:
                grid[e] = EMPTY
            for n in new_positions:
                i, j = n[0]
                what = n[1]
                grid[i, j] = what
        
        # print(grid)

    print(grid)
    return calc_score(grid)


def tests():
    
    # grid = np.array([
    #   [0,0,0,0,0,0],
    #   [0,0,0,0,0,0],
    #   [0,3,0,0,0,0],
    #   [0,0,0,0,0,0],
    # ])
    # assert calc_score(grid) == 101
    
    # grid = np.array([
    #   [0,0,0,0,0,0],
    #   [0,3,0,0,4,0],
    #   [0,3,0,0,4,0],
    #   [0,0,0,0,0,0],
    # ])
    # assert calc_score(grid) == 404
    

    # grid = np.array([
    #   [3,0,0,0],
    #   [0,0,0,0],
    #   [0,0,0,0],
    #   [0,0,0,0],
    # ])
    # assert calc_score(grid) == 0
    
    # grid = np.array([
    #   [0,3,0,0],
    #   [0,0,0,0],
    #   [0,0,0,0],
    #   [0,0,0,0],
    # ])
    # assert calc_score(grid) == 1
    
    # grid = np.array([
    #   [0,0,0,0],
    #   [3,0,0,0],
    #   [0,0,0,0],
    #   [0,0,0,0],
    # ])
    # assert calc_score(grid) == 100
    
    # grid = np.array([
    #   [0,0,0,0],
    #   [0,3,0,0],
    #   [0,0,0,0],
    #   [0,0,0,0],
    # ])
    # assert calc_score(grid) == 101
    
    # grid = np.array([
    #   [0,0,0,0],
    #   [0,0,0,0],
    #   [3,0,0,0],
    #   [0,0,0,0],
    # ])
    # assert calc_score(grid) == 100
    
    # grid = np.array([
    #   [0,0,0,0],
    #   [0,0,0,0],
    #   [0,3,0,0],
    #   [0,0,0,0],
    # ])
    # assert calc_score(grid) == 101
    
    # grid = np.array([
    #   [0,0,0,0],
    #   [0,0,0,0],
    #   [0,0,0,0],
    #   [3,0,0,0],
    # ])
    # assert calc_score(grid) == 0
    
    # grid = np.array([
    #   [0,0,0,0],
    #   [0,0,0,0],
    #   [0,0,0,0],
    #   [0,3,0,0],
    # ])
    # assert calc_score(grid) == 1
    
    # grid = np.array([
    #   [0,0,4,0],
    #   [0,0,0,0],
    #   [0,0,0,0],
    #   [0,0,0,0],
    # ])
    # assert calc_score(grid) == 1
    
    # grid = np.array([
    #   [0,0,0,4],
    #   [0,0,0,0],
    #   [0,0,0,0],
    #   [0,0,0,0],
    # ])
    # assert calc_score(grid) == 0
    
    # grid = np.array([
    #   [0,0,0,0],
    #   [0,0,4,0],
    #   [0,0,0,0],
    #   [0,0,0,0],
    # ])
    # assert calc_score(grid) == 101
    
    # grid = np.array([
    #   [0,0,0,0],
    #   [0,0,0,4],
    #   [0,0,0,0],
    #   [0,0,0,0],
    # ])
    # assert calc_score(grid) == 100

    # grid = np.array([
    #   [0,0,0,0],
    #   [0,0,0,0],
    #   [0,0,4,0],
    #   [0,0,0,0],
    # ])
    # assert calc_score(grid) == 101
    
    # grid = np.array([
    #   [0,0,0,0],
    #   [0,0,0,0],
    #   [0,0,0,4],
    #   [0,0,0,0],
    # ])
    # assert calc_score(grid) == 100
    
    # grid = np.array([
    #   [0,0,0,0],
    #   [0,0,0,0],
    #   [0,0,0,0],
    #   [0,0,4,0],
    # ])
    # assert calc_score(grid) == 1
    
    # grid = np.array([
    #   [0,0,0,0],
    #   [0,0,0,0],
    #   [0,0,0,0],
    #   [0,0,0,4],
    # ])
    # assert calc_score(grid) == 0
    
    m = {
        ".": EMPTY,
        "#": WALL,
        "@": ROBOT,
        "[": LEFT_BOX,
        "]": RIGHT_BOX,
    }
    lines = get_input("example_result.txt")
    grid = []
    for line in lines:
        grid.append([m[c] for c in line])
    grid = np.array(grid)
    score = calc_score(grid)
    assert score == 9021, f"score = {score} != {9021}"
    
    grid = np.zeros((4, 20))
    grid[1, 5] = LEFT_BOX
    grid[1, 6] = RIGHT_BOX
    score = calc_score(grid)
    assert score == 105, f"score = {score}"
    

    # # move 2 down
    # grid = np.zeros((5,5))
    # grid[0,0] = ROBOT
    # grid[1,0] = LEFT_BOX
    # grid[1,1] = RIGHT_BOX
    # grid[2,0] = LEFT_BOX
    # grid[2,1] = RIGHT_BOX
    # new_grid = np.copy(grid)
    # print(new_grid)
    # can_move(grid, (0, 0), 'v', ROBOT, new_grid)
    # print(new_grid)
    # assert new_grid[0,0] == EMPTY
    # assert new_grid[1,0] == ROBOT
    # assert new_grid[2,0] == LEFT_BOX
    # assert new_grid[2,1] == RIGHT_BOX
    # assert new_grid[3,0] == LEFT_BOX
    # assert new_grid[3,1] == RIGHT_BOX
    
    # move down
    grid = np.zeros((5,5))
    grid[0,1] = ROBOT
    grid[1,0] = LEFT_BOX
    grid[1,1] = RIGHT_BOX
    new_grid = np.copy(grid)
    can_move(grid, (0, 1), 'v', ROBOT, new_grid)
    assert new_grid[0,0] == EMPTY
    assert new_grid[1,1] == ROBOT
    assert new_grid[2,0] == LEFT_BOX
    assert new_grid[2,1] == RIGHT_BOX
    grid = new_grid
    can_move(grid, (1, 1), 'v', ROBOT, new_grid)
    assert new_grid[1,1] == EMPTY
    assert new_grid[2,1] == ROBOT
    assert new_grid[3,0] == LEFT_BOX
    assert new_grid[3,1] == RIGHT_BOX

    # move 2 boxes right
    grid = np.zeros((1,10))
    grid[0,0] = ROBOT
    grid[0,1] = LEFT_BOX
    grid[0,2] = RIGHT_BOX
    grid[0,3] = LEFT_BOX
    grid[0,4] = RIGHT_BOX
    new_grid = np.copy(grid)
    can_move(grid, (0, 0), '>', ROBOT, new_grid)
    assert new_grid[0,0] == EMPTY
    assert new_grid[0,1] == ROBOT
    assert new_grid[0,2] == LEFT_BOX
    assert new_grid[0,3] == RIGHT_BOX
    assert new_grid[0,4] == LEFT_BOX
    assert new_grid[0,5] == RIGHT_BOX
    
    # move up
    grid = np.zeros((5,5))
    grid[4,0] = ROBOT  # lower left corner
    grid[3,0] = LEFT_BOX
    grid[3,1] = RIGHT_BOX
    new_grid = np.copy(grid)
    can_move(grid, (4, 0), '^', ROBOT, new_grid)
    assert new_grid[4,0] == EMPTY
    assert new_grid[3,0] == ROBOT
    assert new_grid[2,0] == LEFT_BOX
    assert new_grid[2,1] == RIGHT_BOX
    grid = new_grid
    can_move(grid, (3, 0), '^', ROBOT, new_grid)
    assert new_grid[3,0] == EMPTY
    assert new_grid[2,0] == ROBOT
    assert new_grid[1,0] == LEFT_BOX
    assert new_grid[1,1] == RIGHT_BOX
    
    # move down
    grid = np.zeros((5,5))
    grid[0,0] = ROBOT  # upper left corner
    grid[1,0] = LEFT_BOX
    grid[1,1] = RIGHT_BOX
    new_grid = np.copy(grid)
    can_move(grid, (0, 0), 'v', ROBOT, new_grid)
    assert new_grid[0,0] == EMPTY
    assert new_grid[1,0] == ROBOT
    assert new_grid[2,0] == LEFT_BOX
    assert new_grid[2,1] == RIGHT_BOX
    grid = new_grid
    can_move(grid, (1, 0), 'v', ROBOT, new_grid)
    assert new_grid[1,0] == EMPTY
    assert new_grid[2,0] == ROBOT
    assert new_grid[3,0] == LEFT_BOX
    assert new_grid[3,1] == RIGHT_BOX
    
    # move left
    grid = np.zeros((5,5))
    grid[0,4] = ROBOT
    grid[0,3] = RIGHT_BOX
    grid[0,2] = LEFT_BOX
    new_grid = np.copy(grid)
    can_move(grid, (0, 4), '<', ROBOT, new_grid)
    assert new_grid[0,4] == EMPTY
    assert new_grid[0,3] == ROBOT
    assert new_grid[0,2] == RIGHT_BOX
    assert new_grid[0,1] == LEFT_BOX
    grid = new_grid
    can_move(grid, (0, 3), '<', ROBOT, new_grid)
    assert new_grid[0,3] == EMPTY
    assert new_grid[0,2] == ROBOT
    assert new_grid[0,1] == RIGHT_BOX
    assert new_grid[0,0] == LEFT_BOX
    
    # move right
    grid = np.zeros((5,5))
    grid[0,0] = ROBOT
    grid[0,1] = LEFT_BOX
    grid[0,2] = RIGHT_BOX
    new_grid = np.copy(grid)
    can_move(grid, (0, 0), '>', ROBOT, new_grid)
    assert new_grid[0,0] == EMPTY
    assert new_grid[0,1] == ROBOT
    assert new_grid[0,2] == LEFT_BOX
    assert new_grid[0,3] == RIGHT_BOX
    grid = new_grid
    can_move(grid, (0, 1), '>', ROBOT, new_grid)
    assert new_grid[0,1] == EMPTY
    assert new_grid[0,2] == ROBOT
    assert new_grid[0,3] == LEFT_BOX
    assert new_grid[0,4] == RIGHT_BOX
    
    grid = np.zeros((5,5))
    grid[2,2] = ROBOT
    assert can_move(grid, (2,2), '^', ROBOT)
    assert can_move(grid, (2,2), 'v', ROBOT)
    assert can_move(grid, (2,2), '<', ROBOT)
    assert can_move(grid, (2,2), '>', ROBOT)
    
    grid = np.zeros((5,5))
    grid[np.array([
        (1,1), (1,2), (1,3),
        (2,1),        (2,3),
        (3,1), (3,2), (3,3),
    ])] = WALL
    grid[2,2] = ROBOT
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
    # 1460390 too high
