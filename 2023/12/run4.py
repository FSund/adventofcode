from functools import cache

def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))
    return lines

def unfold(line):
    line, groups = line.split(" ")
    line = "?".join([line]*5)
    groups = ",".join([groups]*5)
    return line + " " + groups

@cache
def _count_arrangements(line: str, groups: tuple[int]):
    # if len(groups) == 0:
    #     return count_arrangements2(line[1:], groups)
    
    if len(line) == 0:  # end of recursion
        if sum(groups) == 0:
            # no more hashtags left to place, success
            return 1
        else:
            # no space left for the remaining hashtags, failure
            return 0
    
    if len(line) < (sum(groups) + len(groups)):
        # not enough space left for the remaining hashtags and dots
        return 0
    
    if sum(groups) == 0:
        # no more hashtags left to place
        # check if we can place dots to the end
        for c in line:
            if c == "#":
                return 0
        return 1
    
    # n_hashtags = sum(groups)  # exact number of hashtags that we need to place
    # n_dots = len(line) - n_hashtags
    # min_n_dots = len(groups)  # need at least one dot between each group of hashtags (and one at the start)
    
    # if line[0] != ".":
    #     # first character should be a dot
    #     return 0

    # if n_dots < min_n_dots:
    #     # not enough dots left
    #     return 0
    #     # exception?
    
    
    if line[0] == "#":
        # first character should be a question mark or a dot
        return 0
    else:
        # dot
        if line[1] == ".":
            return _count_arrangements(line[1:], groups)
        else:  # hashtag or question mark
            # try dot
            dot = _count_arrangements(line[1:], groups)
            
            # try hashtags
            for i in range(1, 1 + groups[0]):
                if line[i] == ".":
                    return dot
            
            idx2 = 1 + groups[0]
            return dot + _count_arrangements(line[idx2:], groups[1:])
            
            
        
        
        
        # if line[0] == "#":
        #     # next character is a hashtag
        #     if groups[0] == 0:  # empty group, go to next
        #         if sum(groups) == 0:
        #             return 0
        #         else:
        #             new_groups = (groups[1] - 1,) + groups[2:]
        #             return count_arrangements2(line[1:], new_groups)
        #     else:    
        #         new_groups = (groups[0] - 1,) + groups[1:]
        #         return count_arrangements2(line[1:], new_groups)

        # elif line[0] == "?":
        #     if groups[0] == 0:
        #         # no more hashtags left
        #         return count_arrangements2(line[1:], groups[1:])
            
        #     groups_with_hashtag = (groups[0] - 1,) + groups[1:]
        #     return (
        #         count_arrangements2(line[1:], groups_with_hashtag)  # hashtag
        #         + count_arrangements2(line[1:], groups)  # dot
        #     )
    
    # return count_arrangements2(line[1:], groups) + count_arrangements2(line[1:], groups[1:])
    
    raise RuntimeError("This should not happen")
    
    
def assert_equal(a, b):
    assert a == b, f"{a} != {b}"
    # raise AssertionError(f"{a} != {b}")

def test_count_arrangements2():
    line = "???.### 1,1,3"
    line = unfold(line)
    assert line == "???.###????.###????.###????.###????.### 1,1,3,1,1,3,1,1,3,1,1,3,1,1,3"

    assert_equal(_count_arrangements(".??", (1,)), 2)
    
    assert_equal(_count_arrangements("", ()), 1)
    assert_equal(_count_arrangements(".#", (1,)), 1)
    assert_equal(_count_arrangements("..#", (1,)), 1)
    assert_equal(_count_arrangements("..", (1,)), 0)
    assert_equal(_count_arrangements(".?", (1,)), 1)
    assert_equal(_count_arrangements("..?", (1,)), 1)
    assert_equal(_count_arrangements(".??", (1,)), 2)
    assert_equal(_count_arrangements(".??.", (1,)), 2)
    assert_equal(_count_arrangements(".???", (2,)), 2)
    assert_equal(_count_arrangements(".###", (3,)), 1)
    assert_equal(_count_arrangements(".#.#", (1,1,)), 1)
    assert_equal(_count_arrangements(".???", (1,1,)), 1)
    assert_equal(_count_arrangements(".????", (1,1,)), 3)
    assert_equal(_count_arrangements(".??.??", (1,1,)), 4)
    
    assert_equal(_count_arrangements(".????.#...#... 4,1,1", (1,1,)), 1)
    
    
def count_arrangements(_line):
    line = unfold(_line)
    line = "." + line
    line, groups = line.split(" ")
    groups = tuple([int(x) for x in groups.split(",")])
    return _count_arrangements(line, groups)

def star2(filename):
    lines = get_input(filename)
    lines = [count_arrangements(line) for line in lines]
    return sum(lines)

if __name__ == "__main__":
    # assert_equal(_count_arrangements(".????.#...#...", (4,1,1,)), 1)
    # assert_equal(star2("????.#...#... 4,1,1"), 4)

    test_count_arrangements2()
    
    # REMEMBER TO PAD START WITH A SINGLE DOT
    

    
    # line, groups = line.split(" ")
    # groups = tuple([int(x) for x in groups.split(",")])
    ans = count_arrangements("???.### 1,1,3")
    assert ans == 1

    ans = count_arrangements(".??..??...?##. 1,1,3")
    assert ans == 16384
    
    assert count_arrangements("?#?#?#?#?#?#?#? 1,3,1,6") == 1
    assert count_arrangements("????.#...#... 4,1,1") == 16
    assert count_arrangements("????.######..#####. 1,6,5") == 2500
    assert count_arrangements("?###???????? 3,2,1") == 506250
    
    ans = star2("example.txt")
    print(f"star 2 example: {ans}")
    
    ans = star2("input.txt")
    print(f"star 2: {ans}")