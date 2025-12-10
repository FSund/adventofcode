from pathlib import Path
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('qtagg')


def get_input(filename):
    script_dir = Path(__file__).parent
    lines = []
    with open(script_dir / filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def rectangle_is_inside(x1, x2, y1, y2, left, right, up, down):
    """
    Check if rectangle with corners (x1, y1), (x2, y2) is inside polygon.
    """
    # check if any lines going down crosses top border
    for d in down:
        
        if 

    return True


def get_vertical(tiles):
    vertical = []
    n = tiles.shape[0]
    for i in range(n):
        x1, y1 = tiles[i-1,:]  # wrap around
        x2, y2 = tiles[i,:]

        x1, x2 = sorted((x1, x2))
        y1, y2 = sorted((y1, y2))

        if x1 == x2:  # x value (horizontal) does not change --> this is a vertical line
            vertical.append((x1, x2, y1, y2))

    return vertical


def aoc(filename):
    # lines = get_input(filename)
    tiles = np.loadtxt(filename, delimiter=",", dtype=int)
    n = tiles.shape[0]
    
    # x1, y1 = np.max(tiles, axis=0)
    # grid = np.zeros((x1+5, y1+5), dtype=np.uint8)
    # print(f"shape: {x1, y1}")
    # print(f"memory: {x1*y1*8} bits, {x1*y1/1024} kB, {x1*y1/1024/1024} MB")

    graph = defaultdict(int)
    for i in range(n):
        x1, y1 = tiles[i-1,:]  # wrap around
        x2, y2 = tiles[i,:]

        x1, x2 = sorted((x1, x2))
        y1, y2 = sorted((y1, y2))
        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                graph[(x, y)] = 1  # edge



    # check each point on the border of each possible rectangle
    

    biggest = (-1, 0, 0)
    n_rectangles = 0
    for i in range(n):
        x1, y1 = tiles[i]
        for j in range(i+1, n):
            x2, y2 = tiles[j]
            n_rectangles += 1

            x1, x2 = sorted((x1, x2))
            y1, y2 = sorted((y1, y2))

            if not rectangle_is_inside(x1, x2, y1, y2, left, right, up, down):
                continue

            dx = x2 - x1
            dy = y2 - y1
            area = (dy + 1) * (dx + 1)
            biggest = max(biggest, (area, i, j))

    if biggest[0] == -1:
        raise RuntimeError("Did not find solution")

    print(f"biggest has area of {biggest[0]}, tiles {tiles[biggest[1]]} and {tiles[biggest[2]]}")
    biggest = biggest[0]
    if grid.shape[0] > 10_000:
        # fig, ax = plt.subplots()
        # ax.imshow(grid[:15_000, :15_000].transpose())
        # fig.savefig(f"{filename}.png", dpi=500)
        pass
    else:
        fig, ax = plt.subplots()
        ax.imshow(grid.transpose())
        plt.show()
    
    return biggest


def tests():
    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 24, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
