def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))
    return lines

def matches_arrangement(line, arrangement):
    groups = [[]]
    for i in range(len(line)):
        if line[i] == ".":
            groups.append([])
        elif line[i] == "#":
            groups[-1].append(i)
        
    counts = []
    for group in groups:
        if len(group) == 0:
            continue
        counts.append(len(group))

    return counts == arrangement

def get_arrangements(_line: list, idx=0):
    if "?" not in _line:
        # print("? not in line")
        yield _line
        return
    
    line = _line.copy()
    # recursively get all arrangements
    # for i in range(idx, len(line)):
    if line[idx] == "?":
        line[idx] = "." # try empty
        if idx == len(line) - 1:
            # print("yielding, idx == len(line) - 1")
            yield line
        else:
            yield from get_arrangements(line, idx+1)

        line[idx] = "#" # try full
        if idx == len(line) - 1:
            # print("yielding, idx == len(line) - 1")
            yield line
        else:
            yield from get_arrangements(line, idx+1)
    else:
        if idx == len(line) - 1:
            # print("yielding, idx == len(line) - 1")
            yield line
        else:
            yield from get_arrangements(line, idx+1)

def count_valid_arrangements(line):
    line, groups = line.split(" ")
    line = list(line)
    groups = [int(g) for g in groups.split(",")]
    
    count = 0
    for arr in get_arrangements(line):
        # print(arr)
        if matches_arrangement(arr, groups):
            count += 1
    return count

def star1(filename):
    lines = get_input(filename)
    
    count = 0
    for idx, line in enumerate(lines):
        print(f"{idx}/{len(lines)}")
        count += count_valid_arrangements(line)
    
    return count

def tests():
    assert count_valid_arrangements("???.??.? 3,2,1") == 1
    
    # print("???.###")
    for arr in get_arrangements(list("???.###")):
        # print(arr)
        assert arr

    assert matches_arrangement("###", [3])
    assert matches_arrangement("###.###", [3,3])
    assert matches_arrangement("#.#", [1,1])
    arr = [
        ".###.##.#...",
        ".###.##..#..",
        ".###.##...#.",
        ".###.##....#",
        ".###..##.#..",
        ".###..##..#.",
        ".###..##...#",
        ".###...##.#.",
        ".###...##..#",
        ".###....##.#",
    ]
    for arrangement in arr:
        assert matches_arrangement(arrangement, [3,2,1])

    # for arr in get_arrangements(list("###.###")):
    #     print(arr)
    
    # arr = list(get_arrangements(list("###?###")))
    # print(arr)
    for arr in get_arrangements(list("###?###")):
        # print(arr)
        assert arr in [list("###.###"), list("#######")]
    
    for arr in get_arrangements(list("??")):
        assert arr in [list("##"), list(".#"), list("#."), list("..")]
    
    for arr in get_arrangements(list("??.")):
        assert arr in [list("##."), list(".#."), list("#.."), list("...")]
    
    for arr in get_arrangements(list(".??.")):
        assert arr in [list(".##."), list("..#."), list(".#.."), list("....")]
    
    for arr in get_arrangements(list(".?.?.")):
        assert arr in [list(".#.#."), list("...#."), list(".#..."), list(".....")]
        
    for arr in get_arrangements(list("???")):
        assert arr in [list("###"), list(".##"), list("#.#"), list("##."), list("..#"), list(".#."), list("#.."), list("...")]
    
    # for arr in get_arrangements(list("???.??.?")):
    #     print(arr)


if __name__ == "__main__":
    tests()

    example = star1("example.txt")
    print(f'Example: {example}')
    assert(example == 21)
    
    ans = star1("input.txt")
    print(f'First star: {ans}')
    # assert(ans == 9693756)
    
    # example = star2("example.txt", expansion=1000000)
    # print(f"Star 2 example: {example}")
    # # assert example == 10
    
    # # assert star2("example3.txt") == 8

    # ans = star2("input.txt")
    # print(f'Second star: {ans}')
    # assert ans == 717878258016

    # # 575363132488 too low
