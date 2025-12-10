from pathlib import Path
from itertools import product, combinations
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


# def rectangle_is_inside(x1, x2, y1, y2, left, right, up, down):
#     """
#     Check if rectangle with corners (x1, y1), (x2, y2) is inside polygon.
#     """
#     # check if any lines going down crosses top border
#     for d in down:

#         if 

#     return True


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
    # start_x = x1 + 1
    # end_x = x2 - 1
    # start_y = y1 + 1
    # end_y = y2 - 1

    # start_x = x1
    # end_x = x2
    # start_y = y1
    # end_y = y2

    # start_x, end_x = sorted([x1, x2])
    # start_y, end_y = sorted([y1, y2])

    for e_start_x, e_start_y, e_end_x, e_end_y in edges:
        # if ex >= start_x and ex <= end_x and ey >= start_y and ey <= end_y:
        #     return False

        e_start_x, e_end_x = sorted((e_start_x, e_end_x))
        e_start_y, e_end_y = sorted((e_start_y, e_end_y))
        if start_x < e_end_x and end_x > e_start_x and start_y < e_end_y and end_y > e_start_y:
            return True
        
    return False


def get_edges(tiles):
    n = tiles.shape[0]

    # edges = []
    # for (x1, y1), (x2, y2) in combinations(tiles, 2):
    #     edges.append((x1, y1, x2, y2))

    edges = []
    for i in range(n-1):
        x1, y1 = tiles[i]
        x2, y2 = tiles[i+1]
        edges.append((x1, y1, x2, y2))

    # close the polygon
    edges.append((tiles[-1][0], tiles[-1][1], tiles[0][0], tiles[0][1]))

    return edges


def aoc(filename):
    # lines = get_input(filename)
    tiles = np.loadtxt(filename, delimiter=",", dtype=int)
    # n = tiles.shape[0]

    # x1, y1 = np.max(tiles, axis=0)
    # grid = np.zeros((x1+5, y1+5), dtype=np.uint8)
    # print(f"shape: {x1, y1}")
    # print(f"memory: {x1*y1*8} bits, {x1*y1/1024} kB, {x1*y1/1024/1024} MB")

    edges = get_edges(tiles)

    biggest = -1
    for (x1, y1), (x2, y2) in combinations(tiles, 2):
        # x1, y1 = tiles[i,:]
        # x2, y2 = tiles[j,:]

        # x1, x2 = sorted([x1, x2])
        # y1, y2 = sorted([y1, y2])

        start_x, end_x = sorted((x1, x2))
        start_y, end_y = sorted((y1, y2))

        dx = end_x - start_x
        dy = end_y - start_y
        area = (dy + 1) * (dx + 1)

        if area > biggest:  # check area first to avoid costly check
            if not intersect(start_x, start_y, end_x, end_y, edges):
                biggest = area

            # print(f"{x1=}, {y1=}, {x2=}, {y2=}, {area=}")
            # print(biggest)
        # else:
        #     dx = x2 - x1
        #     dy = y2 - y1
        #     area = (dy + 1) * (dx + 1)
        #     print(f"discard: {x1=}, {y1=}, {x2=}, {y2=}, {area=}")


    if biggest == -1:
        raise RuntimeError("Did not find solution")

    # print(f"biggest has area of {biggest[0]}, tiles {tiles[biggest[1]]} and {tiles[biggest[2]]}, idx {biggest[1]}, {biggest[2]}")
    print(f"biggest has area of {biggest}")
    # biggest = biggest[0]

    # if grid.shape[0] > 10_000:
    #     # fig, ax = plt.subplots()
    #     # ax.imshow(grid[:15_000, :15_000].transpose())
    #     # fig.savefig(f"{filename}.png", dpi=500)
    #     pass
    # else:
    #     fig, ax = plt.subplots()
    #     ax.imshow(grid.transpose())
    #     plt.show()
    
    return biggest


def tests():
    tiles = np.loadtxt("example.txt", delimiter=",", dtype=int)
    edges = get_edges(tiles)
    assert not intersect(9, 5, 2, 3, edges), "This rectangle should not intersect!"
    assert not intersect(2, 3, 9, 5, edges), "This rectangle should not intersect!"

    # tiles = np.loadtxt("example.txt", delimiter=",", dtype=int)
    # vertical = get_vertical(tiles)
    # assert rectangle_is_inside(2, 9, 3, 5, vertical), "This rectangle should be inside!"


    # vertical = [
    #     (10, 10, 1, 10),
    # ]

    # # square
    # x1 = 1
    # y1 = 1
    # x2 = 9
    # y2 = 9
    # assert rectangle_is_inside(x1, x2, y1, y2, vertical)

    # # wide, 1 tall, outside
    # x1 = 1
    # y1 = 5
    # x2 = 12
    # y2 = 5
    # assert not rectangle_is_inside(x1, x2, y1, y2, vertical)

    # # wide, 1 tall, inside
    # x1 = 1
    # y1 = 5
    # x2 = 9
    # y2 = 5
    # assert rectangle_is_inside(x1, x2, y1, y2, vertical)

    # # on the edge
    # x1 = 1
    # y1 = 1
    # x2 = 10
    # y2 = 10
    # assert rectangle_is_inside(x1, x2, y1, y2, vertical)

    # # over the edge (to the right)
    # x1 = 1
    # y1 = 1
    # x2 = 11
    # y2 = 10
    # assert not rectangle_is_inside(x1, x2, y1, y2, vertical)

    # # over the edge (down)
    # x1 = 1
    # y1 = 1
    # x2 = 10
    # y2 = 11
    # assert not rectangle_is_inside(x1, x2, y1, y2, vertical)

    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 24, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
