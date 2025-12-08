from pathlib import Path
from scipy.cluster.hierarchy import DisjointSet
import time


def get_input(filename):
    script_dir = Path(__file__).parent
    lines = []
    with open(script_dir / filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def aoc(filename):
    lines = get_input(filename)

    # only parse strings once
    boxes = []
    for line in lines:
        x, y, z = [int(d) for d in line.split(",")]
        boxes.append([x, y, z])

    t0 = time.perf_counter()

    # Create all edges with distances
    n = len(lines)
    edges = []
    for i in range(n):
        box_i = boxes[i]
        for j in range(i+1, n):
            box_j = boxes[j]
            
            # inline distance calculation for speed
            d = (box_i[0] - box_j[0])**2 + (box_i[1] - box_j[1])**2 + (box_i[2] - box_j[2])**2
            edges.append((d, i, j))
    
    # sort by distance
    edges.sort()

    print(f"Build & sort: {time.perf_counter() - t0}")

    circuits = DisjointSet(list(range(n)))
    for d, i, j in edges:
        # connect i to j
        circuits.merge(i, j)
        
        # only need to check a single circuit, since if all of them are connected, all of them are connected
        if circuits.subset_size(0) == n:
            x1 = boxes[i][0]
            x2 = boxes[j][0]
            return x1*x2

    raise RuntimeError()


def tests():
    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 25272, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()

    t0= time.perf_counter()
    ans = aoc("input.txt")
    print(f"{ans = }")
    print(f"Total time: {time.perf_counter() - t0}")

