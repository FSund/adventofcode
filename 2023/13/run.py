import numpy as np

def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))
    return lines

def as_np(pattern):
    return np.array([list(row) for row in pattern])



def check_horizontal_line_reflection(_pattern):
    pattern = as_np(_pattern)
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
        if reflection:
            print("found horizontal line reflection")
            return 100 * j
    
    print("no horizontal line reflection found")
    return 0

#     012345678
#   0 #.##..##.
#   1 ..#.##.#.
#   2 ##......#
#   3 ##......#
#   4 ..#.##.#.
#   5 ..##..##.
#   6 #.#.##.#.

def check_vertical_line_reflection(_pattern):
    pattern = as_np(_pattern)
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
        if reflection:
            print("found vertical line reflection ()")
            return i
    
    print("no vertical line reflection found")
    return 0
            
        

def star1(filename):
    lines = get_input(filename)
    print(lines)
    
    sum = 0
    lines.append("")
    pattern = []
    for line in lines:
        if line == "":
            # print(f"checking pattern: \n{as_np(pattern)}")
            sum += check_horizontal_line_reflection(pattern)
            sum += check_vertical_line_reflection(pattern)
            pattern = []
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
    
    assert check_horizontal_line_reflection(pattern) == 400
    
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
    
    assert check_vertical_line_reflection(pattern) == 5
    

if __name__ == "__main__":
    tests()
    print("TESTS DONE")

    example = star1("example.txt")
    print(f'Example: {example}')
    assert(example == 405)
    
    ans = star1("input.txt")
    print(f'First star: {ans}')
    # assert(ans == 9693756)
    
    # 23871 too low
    
    # example = star2("example.txt")
    # print(f"Star 2 example: {example}")
    # # assert example == 10
    
    # # assert star2("example3.txt") == 8

    # ans = star2("input.txt")
    # print(f'Second star: {ans}')
    # assert ans == 717878258016

    # # 575363132488 too low
