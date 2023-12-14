import numpy as np
from datetime import datetime

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
    
def roll_north_optimized(lines):
    # roll north
    for i in range(1, lines.shape[0]):
        for j in range(lines.shape[1]):
            if lines[i,j] == 0 and lines[i-1,j] == 1:
                # find index of last empty space above
                k = i
                while k > 0 and lines[k-1,j] == 1:
                    k -= 1
                
                # move the round rock into free space
                lines[k,j] = 0
                # make i free space (move the round rock away)
                lines[i,j] = 1
                # print(f"Moved round rock from {i,j} to {k,j}")
    
    return lines

def roll_south_optimized(lines):
    # roll south
    for i in range(lines.shape[0]-2, -1, -1):  # reverse loop from row n-1 to 0
        for j in range(lines.shape[1]):
            if lines[i,j] == 0 and lines[i+1,j] == 1:  # if current is round rock and below is free space
                # find index of last empty space below
                k = i
                while k < lines.shape[0]-1 and lines[k+1,j] == 1:
                    k += 1
                # print(f"lines[k+1,j] = {lines[k+1,j]}")
                
                # move the round rock into free space
                lines[k,j] = 0
                # make i free space (move the round rock away)
                lines[i,j] = 1
                
                # print(f"Moved round rock from {i,j} to {k,j}")
                # print(lines)
    
    return lines

def roll_east_optimized(lines):
    # roll east
    for j in range(lines.shape[1]-2, -1, -1):
        for i in range(lines.shape[0]):
            if lines[i,j] == 0 and lines[i,j+1] == 1:
                # find index of last empty space east
                k = j
                while k < lines.shape[1]-1 and lines[i,k+1] == 1:
                    k += 1
                
                # move the round rock into free space
                lines[i,k] = 0
                # make i free space (move the round rock away)
                lines[i,j] = 1
                # print(f"Moved round rock from {i,j} to {k,j}")
    
    return lines


def roll_west_optimized(lines):
    # roll west
    for j in range(1, lines.shape[1]):
        for i in range(lines.shape[0]):
            if lines[i,j] == 0 and lines[i,j-1] == 1:
                # find index of last empty space west
                k = j
                while k > 0 and lines[i,k-1] == 1:
                    k -= 1
                
                # move the round rock into free space
                lines[i,k] = 0
                # make i free space (move the round rock away)
                lines[i,j] = 1
                # print(f"Moved round rock from {i,j} to {k,j}")
    
    return lines


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
    lines = roll_north_optimized(lines)
    lines = roll_west_optimized(lines)
    lines = roll_south_optimized(lines)
    lines = roll_east_optimized(lines)
    return lines

def star2(filename, iterations):
    lines = get_input(filename)
    t0 = datetime.now()
    for i in range(iterations):
        lines = spin_cycle(lines)
        if i % 10000 == 0 and i > 0:
            print(f"Finished iteration {i}")
            t = datetime.now()
            # print(f"Time elapsed: {t-t0}")
            # print(f"Time per 1000 iterations: {(t-t0)/i*1000}")
            print("Estimated time remaining: ", (t-t0)/i*iterations - (t-t0))
    print(f"Elapsed time: {datetime.now() - t0}")
    return calculate_load(lines)

def star2_memo(filename, iterations):
    lines = get_input(filename)
    t0 = datetime.now()
    memo = {}

    for i in range(iterations):
        lines_hash = hash(lines.tobytes())
        if lines_hash in memo:
            lines = memo[lines_hash]
            print(f"Found loop at iteration {i}")
            # find index of lines_hash in memo keys
            idx = list(memo.keys()).index(lines_hash)
            # idx -= 1
            # pop all keys before idx
            keys_to_delete = list(memo.keys())[:idx]
            for key in keys_to_delete:
                del memo[key]
            break
    
        prev_lines_hash = hash(lines.tobytes())
        lines = spin_cycle(lines)
        memo[prev_lines_hash] = lines
        
        # if i % 1000 == 0 and i > 0:
        print(f"Finished iteration {i}")

    remaining_iterations = iterations - i
    print(f"Remaining iterations: {remaining_iterations}")
    print(f"{len(memo) = }")
    remaining_iterations -= len(memo) * (remaining_iterations // len(memo))
    print(f"Remaining iterations: {remaining_iterations}")
    for i in range(remaining_iterations):
        lines = spin_cycle(lines)
    

    print(f"Elapsed time: {datetime.now() - t0}")
    return calculate_load(lines)

def tests():
    # north
    lines = get_input("example.txt")
    lines = roll_north(lines)
    lines2 = get_input("example.txt")
    lines2 = roll_north_optimized(lines2)
    assert np.all(lines == lines2), "Optimized is wrong"
    
    # south
    lines = get_input("example.txt")
    lines = roll_south(lines)
    lines2 = get_input("example.txt")
    lines2 = roll_south_optimized(lines2)
    assert np.all(lines == lines2), "Optimized is wrong"
    
    # east
    lines = get_input("example.txt")
    lines = roll_east(lines)
    lines2 = get_input("example.txt")
    lines2 = roll_east_optimized(lines2)
    assert np.all(lines == lines2), "Optimized is wrong"
    
    # west
    lines = get_input("example.txt")
    lines = roll_west(lines)
    lines2 = get_input("example.txt")
    lines2 = roll_west_optimized(lines2)
    assert np.all(lines == lines2), "Optimized is wrong"
    
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
    
    lines = get_input("example.txt")
    memo = {}
    h = hash(lines.tobytes())
    memo[h] = lines
    assert hash(lines.tobytes()) in memo, "lines not in memo"
    lines2 = memo[hash(lines.tobytes())]
    assert np.all(lines == lines2), "lines not equal to lines2"

if __name__ == "__main__":
    tests()
    print("TESTS DONE")

    example = star1("example.txt")
    print(f'Example: {example}')
    assert(example == 136)
    
    ans = star1("input.txt")
    print(f'First star: {ans}')
    assert(ans == 108813)
    
    example = star2_memo("example.txt", 1000000000)
    print(f"Star 2 example: {example}")
    assert example == 64
    
    # example = star2("example.txt", 1_000_000_000)
    # example = star2("example.txt", 100_000)
    # print(f"Star 2 example: {example}")
    # assert example == 64
    
    # # # assert star2("example3.txt") == 8

    ans = star2_memo("input.txt", 1_000_000_000)
    print(f'Second star: {ans}')
    # assert ans == 37416

    # # # 575363132488 too low
