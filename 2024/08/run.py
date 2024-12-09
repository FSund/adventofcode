def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines

# Calculate the impact of the signal. How many unique locations within the
# bounds of the map contain an antinode?

def get_antennas(lines):
    n = len(lines)
    m = len(lines[0])
    
    antennas = {}
    for i in range(n):
        for j in range(m):
            p = lines[i][j]
            if p != ".":
                if p not in antennas.keys():
                    antennas[p] = []
                antennas[p].append((i,j))
    
    return antennas

def get_antinodes(lines):
    n = len(lines)
    m = len(lines[0])
    
    antennas = get_antennas(lines)
    
    antinodes = []
    for name, positions in antennas.items():
        for i, p1 in enumerate(positions):
            for p2 in positions[i+1:]:
                # calculate antinode positions
                
                # (di, dj) is a vector from from p2 to p1
                di = p1[0] - p2[0]
                dj = p1[1] - p2[1]
                i = p1[0] + di
                j = p1[1] + dj
                if i < 0 or i >= n or j < 0 or j >= m:
                    pass
                else:
                    antinodes.append((i, j))
                    
                # (di, dj) is a vector from from p1 to p2
                di = p2[0] - p1[0]
                dj = p2[1] - p1[1]
                i = p2[0] + di
                j = p2[1] + dj
                if i < 0 or i >= n or j < 0 or j >= m:
                    pass
                else:
                    antinodes.append((i, j))

    # print(f"{len(antinodes)} with duplicates, {len(set(antinodes))} without")
    return set(antinodes)

def get_antinodes_star2(lines):
    n = len(lines)
    m = len(lines[0])
    
    antennas = get_antennas(lines)
    
    antinodes = []
    for name, positions in antennas.items():
        for i, p1 in enumerate(positions):
            for p2 in positions[i+1:]:
                # all antennas are also antinodes (if there are more than 1 of them)
                # we have at least 2 if we are at this point in the loop
                antinodes.append(p1)
                antinodes.append(p2)

                # calculate antinode positions
                
                # (di, dj) is a vector from from p2 to p1
                di = p1[0] - p2[0]
                dj = p1[1] - p2[1]
                i = p1[0] + di
                j = p1[1] + dj
                while i >= 0 and i < n and j >= 0 and j < m:
                    antinodes.append((i, j))
                    i += di
                    j += dj
                    
                # (di, dj) is a vector from from p1 to p2
                di = p2[0] - p1[0]
                dj = p2[1] - p1[1]
                i = p2[0] + di
                j = p2[1] + dj
                while i >= 0 and i < n and j >= 0 and j < m:
                    antinodes.append((i, j))
                    i += di
                    j += dj
    
    return set(antinodes)

def aoc(filename, star2=False):
    lines = get_input(filename)
    if star2:
        antinodes = get_antinodes_star2(lines)
    else:
        antinodes = get_antinodes(lines)

    return len(antinodes)


def tests():
    lines = get_input("example.txt")
    antinodes = get_antinodes(lines)
    lines = get_input("ans.txt")
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] == "#":
                assert (i, j) in antinodes
    
    assert (5, 6) in antinodes  # the one that overlaps the topmost A antenna
    
    lines = get_input("example.txt")
    antinodes = get_antinodes_star2(lines)
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] != ".":
                assert (i, j) in antinodes

    ans = aoc("example.txt")
    print(f"example star 1: {ans}")
    assert ans == 14, f"wrong answer: {ans}"
    
    ans = aoc("example.txt", star2=True)
    print(f"example star 2: {ans}")
    assert ans == 34, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"star 1: {ans}")
    assert ans == 271
    
    ans = aoc("input.txt", star2=True)
    print(f"star 2: {ans}")
    assert ans == 994
