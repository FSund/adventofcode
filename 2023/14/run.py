import numpy as np

def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))
    return as_np(lines)

def calculate_load(lines):
    load = 0
    for i in range(lines.shape[0]):
        for j in range(lines.shape[1]):
            line_load = 0
            if lines[i,j] == 0:
                load += lines.shape[0] - i
                line_load += lines.shape[0] - i

    return load

def as_np(_lines):
    c = {
        "O": 0,  # round rock
        ".": 1,  # free space
        "#": 2,  # cube-shaped rock
    }
    lines = [list(line) for line in _lines]
    for line in lines:
        for j in range(len(line)):
            line[j] = c[line[j]]
    
    lines = np.array([line for line in lines])
    return lines

def star1(filename):
    lines = get_input(filename)

    # print(lines)
    lines = roll_north(lines)
    return calculate_load(lines)
    
    
def roll_north(lines):
    # roll north
    for i in range(1, lines.shape[0]):
        for j in range(lines.shape[1]):
            if lines[i,j] == 0:
                for k in range(i-1, -1, -1):  # loop from row above to top
                    # if k is free space
                    if lines[k,j] == 1:
                        # make k+1 free space (move the round rock away)
                        lines[k+1,j] = 1
                        # move the round rock into free space
                        lines[k,j] = 0  # round rock
                        # print(f"Moved round rock from {k+1,j} to {k,j}")
                    else:
                        # stop moving the round rock
                        break
                # print(lines)
    
    return lines

def roll_south(lines):
    # roll south
    for i in range(lines.shape[0]-2, -1, -1):
        for j in range(lines.shape[1]):
            if lines[i,j] == 0:
                for k in range(i+1, lines.shape[0]):  # loop from row above to top
                    # if k is free space
                    if lines[k,j] == 1:
                        # make k+1 free space (move the round rock away)
                        lines[k-1,j] = 1
                        # move the round rock into free space
                        lines[k,j] = 0  # round rock
                        # print(f"Moved round rock from {k+1,j} to {k,j}")
                    else:
                        # stop moving the round rock
                        break
                # print(lines)
    
    return lines

def roll_east(lines):
    # roll east
    for j in range(lines.shape[1]-2, -1, -1):
        for i in range(lines.shape[0]):
            if lines[i,j] == 0:
                for k in range(j+1, lines.shape[1]):  # loop from row above to top
                    # if k is free space
                    if lines[i,k] == 1:
                        # make k+1 free space (move the round rock away)
                        lines[i,k-1] = 1
                        # move the round rock into free space
                        lines[i,k] = 0  # round rock
                        # print(f"Moved round rock from {k+1,j} to {k,j}")
                    else:
                        # stop moving the round rock
                        break
                # print(lines)
    
    return lines

def roll_west(lines):
    # roll west
    for j in range(1, lines.shape[1]):
        for i in range(lines.shape[0]):
            if lines[i,j] == 0:
                for k in range(j-1, -1, -1):  # loop from row above to top
                    # if k is free space
                    if lines[i,k] == 1:
                        # make k+1 free space (move the round rock away)
                        lines[i,k+1] = 1
                        # move the round rock into free space
                        lines[i,k] = 0  # round rock
                        # print(f"Moved round rock from {k+1,j} to {k,j}")
                    else:
                        # stop moving the round rock
                        break
                # print(lines)
    
    return lines

def spin_cycle(lines):
    lines = roll_north(lines)
    lines = roll_west(lines)
    lines = roll_south(lines)
    lines = roll_east(lines)
    return lines

def tests():
    tilted_lines = [
        "OOOO.#.O..",
        "OO..#....#",
        "OO..O##..O",
        "O..#.OO...",
        "........#.",
        "..#....#.#",
        "..O..#.O.O",
        "..O.......",
        "#....###..",
        "#....#....",
    ]
    tilted_lines = as_np(tilted_lines)
    lines = get_input("example.txt")
    
    lines = roll_north(lines)
    assert np.all(lines == tilted_lines)
    
    assert calculate_load(tilted_lines) == 136
    
    lines = get_input("example.txt")
    lines = spin_cycle(lines)
    
    first_cycle = [
        ".....#....", 
        "....#...O#", 
        "...OO##...", 
        ".OO#......", 
        ".....OOO#.", 
        ".O#...O#.#", 
        "....O#....", 
        "......OOOO", 
        "#...O###..", 
        "#..OO#....", 
    ]
    first_cycle = as_np(first_cycle)
    
    assert np.all(first_cycle == lines)

if __name__ == "__main__":
    tests()
    print("TESTS DONE")

    example = star1("example.txt")
    print(f'Example: {example}')
    assert(example == 136)
    
    ans = star1("input.txt")
    print(f'First star: {ans}')
    # assert(ans == 32371)
    
    # # 23871 too low
    
    # example = star2("example.txt")
    # print(f"Star 2 example: {example}")
    # assert example == 400
    
    # # # assert star2("example3.txt") == 8

    # ans = star2("input.txt")
    # print(f'Second star: {ans}')
    # assert ans == 37416

    # # # 575363132488 too low
