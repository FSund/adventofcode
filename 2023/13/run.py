import numpy as np

def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))
    return lines

def as_np(pattern):
    return np.array([list(row) for row in pattern])



def check_horizontal_line_reflection(pattern: np.ndarray, ignore=None):
    assert isinstance(pattern, np.ndarray)
    for j in range(1, pattern.shape[0]):
        top_length = j + 1
        bottom_length = pattern.shape[0] - j + 1
        
        reflection = False
        # print(f"---------------- {j}")
        for offset in range(1, min(top_length, bottom_length)):
            l = j+offset-1
            r = j-offset
            # print(f"Comparing row {l} vs {r}")
            if np.all(pattern[l,:] == pattern[r,:]):
                reflection = True
                # print(f"Row {l} == {r}")
            else:
                reflection = False
                # print(f"Row {l} != {r}")
                break
        # if reflection:
        #     print(f"found horizontal line reflection, with {j} rows above it")
        if reflection and (j != ignore):
            # print(f"found horizontal line reflection, with {j} rows above it")
            return j
    
    # print("no horizontal line reflection found")
    return 0

#     012345678
#   0 #.##..##.
#   1 ..#.##.#.
#   2 ##......#
#   3 ##......#
#   4 ..#.##.#.
#   5 ..##..##.
#   6 #.#.##.#.

def check_vertical_line_reflection(pattern: np.ndarray, ignore=None):
    assert isinstance(pattern, np.ndarray)
    for i in range(1, pattern.shape[1]):
        left_length = i + 1
        right_length = pattern.shape[1] - i + 1
        
        reflection = False
        # print(f"---------------- {i}")
        for offset in range(1, min(left_length, right_length)):
            l = i+offset-1
            r = i-offset
            # print(f"Comparing col {l} vs {r}")
            if np.all(pattern[:,l] == pattern[:,r]):
                reflection = True
                # print(f"Col {l} == {r}")
            else:
                reflection = False
                # print(f"Col {l} != {r}")
                break
        if reflection and (i != ignore):
            # print("found vertical line reflection ()")
            # print(f"found horizontal line reflection, with {i} columns left of it")
            return i
    
    # print("no vertical line reflection found")
    return 0
            
        

def star1(filename):
    lines = get_input(filename)
    # print(lines)
    
    sum = 0
    lines.append("")
    pattern = []
    for line in lines:
        if line == "":
            pattern = as_np(pattern)
            # print(f"checking pattern: \n{as_np(pattern)}")
            sum += 100 * check_horizontal_line_reflection(pattern)
            sum += check_vertical_line_reflection(pattern)
            pattern = []
        else:
            pattern.append(line)

    return sum

def check_smudges(pattern: np.ndarray):
    assert isinstance(pattern, np.ndarray), f"{type(pattern)} != np.ndarray"
    
    original_above = check_horizontal_line_reflection(pattern)
    original_left_of = check_vertical_line_reflection(pattern)
    # print(f"original: {original_above = }, {original_left_of = }")
    
    for i in range(pattern.shape[0]):
        for j in range(pattern.shape[1]):
            if pattern[i,j] == "#":
                pattern[i,j] = "."
                above = check_horizontal_line_reflection(pattern, original_above)
                left_of = check_vertical_line_reflection(pattern, original_left_of)
                # if above or left_of:
                #     print(f"Found smudge at {i}, {j}, with {above = }, {left_of = } in pattern \n{pattern}")
                pattern[i,j] = "#"  # reset
            else:
                pattern[i,j] = "#"
                above = check_horizontal_line_reflection(pattern, original_above)
                left_of = check_vertical_line_reflection(pattern, original_left_of)
                # if above or left_of:
                #     print(f"Found smudge at {i}, {j}, with {above = }, {left_of = } in pattern \n{pattern}")
                pattern[i,j] = "."  # reset
            
            if above or left_of:
                if above and above != original_above:
                    return (above, 0, i, j)
                elif left_of and left_of != original_left_of:
                    return (0, left_of, i, j)
                else:
                    # print(f"not accepted {above = }, {left_of = }")
                    pass
            else:
                # print(f"not accepted {above = }, {left_of = }")
                pass
            
            # if above or left_of:
            #     if (above and above != original_above
            #         or left_of and left_of != original_left_of):
            #         print(f"accepted: {above = }, {left_of = }")
            #         return (above, left_of, i, j)
            #     else:
            #         print(f"not accepted {above = }, {left_of = }")
                    
    
    raise Exception("No smudges found")


def star2(filename):
    lines = get_input(filename)
    # print(lines)
    
    sum = 0
    lines.append("")
    pattern = []
    pattern_idx = 0
    for line in lines:
        if line == "":
            # print(f"checking pattern {pattern_idx}")
            # print(f"checking pattern: \n{as_np(pattern)}")
            pattern = as_np(pattern)
            # hor1 = check_horizontal_line_reflection(pattern)
            # ver1 = check_vertical_line_reflection(pattern)
            # print("--------- new pattern")
            hor2, ver2, _, _ = check_smudges(pattern)
            
            sum += 100 * hor2
            sum += ver2
            pattern = []
            pattern_idx += 1
        else:
            pattern.append(line)

    return sum


def tests():
    pattern = [
        "#...##..#",
        "#....#..#",
        "..##..###",
        "#####.##.",
        "#####.##.",
        "..##..###",
        "#....#..#",
    ]
    np_pattern = as_np(pattern)
    # print(np_pattern.shape)
    assert np.all(np_pattern[4,:] == np_pattern[3,:])
    
    # print(check_horizontal_line_reflection(pattern))
    
    assert check_horizontal_line_reflection(np_pattern) == 4
    
    pattern = [
        "#.##..##.",
        "..#.##.#.",
        "##......#",
        "##......#",
        "..#.##.#.",
        "..##..##.",
        "#.#.##.#.",
    ]
    np_pattern = as_np(pattern)
    assert np.all(np_pattern[:,5] == np_pattern[:,4])
    
    assert check_vertical_line_reflection(np_pattern) == 5
    
    # MODIFIED PATTERH
    pattern = [
        "..##..##.",
        "..#.##.#.",
        "##......#",
        "##......#",
        "..#.##.#.",
        "..##..##.",
        "#.#.##.#.",
    ]
    np_pattern = as_np(pattern)
    assert check_horizontal_line_reflection(np_pattern) == 3
    
    # MODIFIED PATTERH
    pattern = [
        "#...##..#",
        "#...##..#",
        "..##..###",
        "#####.##.",
        "#####.##.",
        "..##..###",
        "#....#..#",
    ]
    np_pattern = as_np(pattern)
    assert check_horizontal_line_reflection(np_pattern) == 1
    
    # first example
    pattern = [
        "#.##..##.",
        "..#.##.#.",
        "##......#",
        "##......#",
        "..#.##.#.",
        "..##..##.",
        "#.#.##.#.",
    ]
    np_pattern = as_np(pattern)
    (above, left_of, i, j) = check_smudges(np_pattern)
    print(f"Smudges: above: {above}, left_of: {left_of}, at {i}, {j}")
    assert above == 3
    
    # second example
    pattern = [
        "#...##..#",
        "#....#..#",
        "..##..###",
        "#####.##.",
        "#####.##.",
        "..##..###",
        "#....#..#",
    ]
    np_pattern = as_np(pattern)
    (above, left_of, i, j) = check_smudges(np_pattern)
    print(f"Smudges: above: {above}, left_of: {left_of}, at {i}, {j}")
    assert above == 1
    
    # pattern 7
    pattern = [
        "#...##..####.", # 1
        "#.##.#..#.#.#", # 2
        "#.##.#..#.#.#", # 3
        "#...##..####.", # 4
        ".....###...##", # 5
        ".####..#..#.#", # 6
        "..####..#.###", # 7
        ".#..###...#.#", # 8
        "#.#....#.#..#", # 9
        "...##.#..#.#.", # 10
        "...#.#..##..#", # 11
        "..#.#.#....##", # 12
        "##...#...#...", # 13
        "###..#...#...", # 14
        "..#.#.#....##", # 15
    ]
    np_pattern = as_np(pattern)
    above = check_horizontal_line_reflection(np_pattern)
    assert above == 2, f"{above = }"
    left_of = check_vertical_line_reflection(np_pattern)
    
    # MODIFIED pattern 7
    pattern = [
        "#...##..####.", 
        "#.##.#..#.#.#", 
        "#.##.#..#.#.#", 
        "#...##..####.", 
        ".....###...##", 
        ".####..#..#.#", 
        "..####..#.###", 
        ".#..###...#.#", 
        "#.#....#.#..#", 
        "...##.#..#.#.", 
        "...#.#..##..#", 
        "..#.#.#....##", 
        "###..#...#...", 
        "###..#...#...", 
        "..#.#.#....##", 
    ]
    np_pattern = as_np(pattern)
    above = check_horizontal_line_reflection(np_pattern, ignore=2)
    assert above == 13, f"{above = }"
    
    left_of = check_vertical_line_reflection(np_pattern)
    print(f"wat Smudges: above: {above}, left_of: {left_of}")
    (above, left_of, i, j) = check_smudges(np_pattern)


if __name__ == "__main__":
    tests()
    print("TESTS DONE")

    example = star1("example.txt")
    print(f'Example: {example}')
    assert(example == 405)
    
    ans = star1("input.txt")
    print(f'First star: {ans}')
    assert(ans == 32371)
    
    # 23871 too low
    
    example = star2("example.txt")
    print(f"Star 2 example: {example}")
    assert example == 400
    
    # # assert star2("example3.txt") == 8

    ans = star2("input.txt")
    print(f'Second star: {ans}')
    assert ans == 37416

    # # 575363132488 too low
