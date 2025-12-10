from pathlib import Path
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


def rectangle_is_inside(x1, y1, x2, y2, horizontal, vertical):
    """
    Check if rectangle with corners (x1, y1), (x2, y2) is inside polygon.

    If no horizontal or vertical lines cross the borders of the rectangle, it should be fully inside
    """
    for v in vertical:
        # check if horizontal position of the line is whithin box bounds
        # v[0] == v[1] == x
        if x1 <= v[0] <= x2:
            # # check if either end of vertical line is within box bounds
            # if y1 < v[2] < y2 or y1 < v[3] < y2:
            #     return False

            # if both ends inside, ignore it
            if y1 <= v[2] <= y2 and y1 <= v[3] <= y2:
                continue
            
            # if both outside, ignore it
            if v[2] > y2 and v[3] > y2:  # larger than
                continue
            if v[2] < y1 and v[3] < y1:  # smaller than
                continue
            
            # otherwise it should cross the edge
            return False
        
    for h in horizontal:
        # check if vertical position of the line is within box bounds
        # h[2] == h[3]
        if y1 <= h[2] <= y2:
            # # check if either ends of the horizontal line is within box bounds
            # if x1 < h[0] < x2 or x1 < h[1] < x2:
            #     return False

            # if both ends inside, ignore it
            if x1 <= h[0] <= x2 and x1 <= h[1] <= x2:
                continue

            # if both outside, ignore it
            if h[0] > x2 and h[1] > x2:  # larger than
                continue
            if h[0] < x1 and h[1] < x1:  # smaller than
                continue

            # otherwise it should cross the edge of the rectangle
            return False

    return True


def get_edges(tiles):
    vertical = []
    horizontal = []
    n = tiles.shape[0]
    for i in range(n):
        x1, y1 = tiles[i-1,:]  # wrap around
        x2, y2 = tiles[i,:]

        x1, x2 = sorted((x1, x2))
        y1, y2 = sorted((y1, y2))

        # grid[x1:x2+1, y1:y2+1] = 1

        if x1 == x2:  # x value (horizontal) does not change --> this is a vertical line
            vertical.append((x1, x2, y1, y2))
        else:
            assert y1 == y2
            horizontal.append((x1, x2, y1, y2))

    return vertical, horizontal


def aoc(filename):
    # lines = get_input(filename)
    tiles = np.loadtxt(filename, delimiter=",", dtype=int)
    x1, y1 = np.max(tiles, axis=0)
    grid = np.zeros((x1+5, y1+5), dtype=np.uint8)
    print(f"shape: {x1, y1}")
    print(f"memory: {x1*y1*8} bits, {x1*y1/1024} kB, {x1*y1/1024/1024} MB")

    vertical = []
    horizontal = []
    n = tiles.shape[0]
    for i in range(n):
        x1, y1 = tiles[i-1,:]  # wrap around
        x2, y2 = tiles[i,:]

        x1, x2 = sorted((x1, x2))
        y1, y2 = sorted((y1, y2))

        grid[x1:x2+1, y1:y2+1] = 1

        if x1 == x2:  # x value (horizontal) does not change --> this is a vertical line
            vertical.append((x1, x2, y1, y2))
        else:
            assert y1 == y2
            horizontal.append((x1, x2, y1, y2))

    print(f"vertical: {len(vertical)}")
    print(f"horizontal: {len(horizontal)}")
    print(f"non-zero: {np.sum(grid > 0)}")

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

            if not rectangle_is_inside(x1, y1, x2, y2, horizontal, vertical):
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
    tiles = np.loadtxt("example.txt", delimiter=",", dtype=int)
    vertical, horizontal = get_edges(tiles)
    assert rectangle_is_inside(2, 3, 9, 5, horizontal, vertical), "This rectangle should be inside!"


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
