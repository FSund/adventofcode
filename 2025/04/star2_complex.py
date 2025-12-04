from pathlib import Path
from collections import defaultdict

def get_input(filename):
    script_dir = Path(__file__).parent
    lines = []
    with open(script_dir / filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def aoc(filename):
    lines = get_input(filename)

    # dictionary with complex number as key
    maze = defaultdict(lambda: ".")
    for r, row in enumerate(lines):
        for c, char in enumerate(row):
            maze[r * 1j + c] = char

    neighbors = [1, -1, 1j, -1j, 1+1j, 1-1j, -1+1j, -1-1j]
    ans = 0
    keys = list(maze.keys())  # snapshot keys, since the dict can get new default elements during iteration
    while True:
        removed_this_iteration = 0
        for p in keys:
            if maze[p] == "@":
                # if there are fewer than four rolls of paper in the eight adjacent positions
                count = 0
                for dir in neighbors:
                    if maze[p + dir] == "@":
                        count += 1

                if count < 4:
                    removed_this_iteration += 1
                    maze[p] = "."

        ans += removed_this_iteration
        if not removed_this_iteration:
            break

    return ans


def tests():
    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 43, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
