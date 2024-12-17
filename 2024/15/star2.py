import numpy as np


def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


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


def calc_score(grid):
    score = 0
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == LEFT_BOX:
                score += 100 * i + j
            
    return score


def aoc(filename):
    grid, robot, moves = parse_input(filename)
    for move in moves:
        empty_after = set()
        new_positions = set()
        if get_move_set(grid, robot, move, ROBOT, empty_after, new_positions):
            robot = (
                robot[0] + MOVES[move][0],
                robot[1] + MOVES[move][1],
            )
            for e in empty_after:
                grid[e] = EMPTY
            for n in new_positions:
                i, j = n[0]
                what = n[1]
                grid[i, j] = what
 
    return calc_score(grid)


def tests():
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
    
    ans = aoc("example.txt")
    print(f"example star 2: {ans}")
    assert ans == 9021, f"wrong answer: {ans}"

if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"star 2: {ans}")
    assert ans == 1453087
