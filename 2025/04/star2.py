from pathlib import Path

def get_input(filename):
    script_dir = Path(__file__).parent
    lines = []
    with open(script_dir / filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def aoc(filename):
    lines = get_input(filename)
    maze = []
    for line in lines:
        maze.append(list(line))

    neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    m = len(maze)  # m rows
    n = len(maze[0])  # n columns
    ans = 0
    removed_this_iteration = 1
    while removed_this_iteration:
        removed_this_iteration = 0
        for i in range(m):
            for j in range(n):
                if maze[i][j] == "@":  # roll of paper
                    # if there are fewer than four rolls of paper in the eight adjacent positions
                    count = 0
                    for neigh in neighbors:
                        ii = i + neigh[0]
                        jj = j + neigh[1]
                        if ii < 0 or ii >= m:
                            continue
                        if jj < 0 or jj >= n:
                            continue
                        if maze[ii][jj] == "@":
                            count += 1
                    if count < 4:
                        removed_this_iteration += 1
                        maze[i][j] = "."
        ans += removed_this_iteration

    return ans


def tests():
    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 43, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
