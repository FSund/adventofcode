from pathlib import Path
from itertools import combinations
import numpy as np


def get_input(filename):
    script_dir = Path(__file__).parent
    lines = []
    with open(script_dir / filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


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


def intersect(start_x, start_y, end_x, end_y, edges):
    for ex1, ey1, ex2, ey2 in edges:
        e_start_x, e_end_x = sorted((ex1, ex2))
        e_start_y, e_end_y = sorted((ey1, ey2))
        if start_x < e_end_x and end_x > e_start_x and start_y < e_end_y and end_y > e_start_y:
            return True
        
    return False


def get_edges(tiles):
    n = tiles.shape[0]

    edges = []
    for i in range(n-1):
        x1, y1 = tiles[i]
        x2, y2 = tiles[i+1]
        edges.append((x1, y1, x2, y2))

    # close the polygon
    edges.append((tiles[-1][0], tiles[-1][1], tiles[0][0], tiles[0][1]))

    return edges


def aoc(filename):
    tiles = np.loadtxt(filename, delimiter=",", dtype=int)
    edges = get_edges(tiles)

    biggest = -1
    for (x1, y1), (x2, y2) in combinations(tiles, 2):
        start_x, end_x = sorted((x1, x2))
        start_y, end_y = sorted((y1, y2))

        dx = end_x - start_x
        dy = end_y - start_y
        area = (dy + 1) * (dx + 1)

        if area > biggest:  # check area first to avoid costly check
            if not intersect(start_x, start_y, end_x, end_y, edges):
                biggest = area

    if biggest == -1:
        raise RuntimeError("Did not find solution")

    print(f"biggest has area of {biggest}")

    return biggest


def tests():
    tiles = np.loadtxt("example.txt", delimiter=",", dtype=int)
    edges = get_edges(tiles)
    assert not intersect(9, 5, 2, 3, edges), "This rectangle should not intersect!"
    assert not intersect(2, 3, 9, 5, edges), "This rectangle should not intersect!"

    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 24, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
