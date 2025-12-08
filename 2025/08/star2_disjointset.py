from pathlib import Path
from scipy.cluster.hierarchy import DisjointSet


def get_input(filename):
    script_dir = Path(__file__).parent
    lines = []
    with open(script_dir / filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def calc_dist(this, other):
    x1, y1, z1 = [int(d) for d in this.split(",")]
    x2, y2, z2 = [int(d) for d in other.split(",")]
    return (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2


def aoc(filename):
    lines = get_input(filename)

    # calculate distances
    distance = []
    n = len(lines)
    for i in range(n):
        for j in range(i+1, n):
            d = calc_dist(lines[i], lines[j])
            distance.append((d, (i,j)))
    
    distance = sorted(distance)
    circuits = DisjointSet(list(range(n)))
    for d in distance:
        i = d[1][0]
        j = d[1][1]
        
        # connect i to j
        circuits.merge(i, j)
        
        # only need to check a single circuit, since if all of them are connected, all of them are connected
        if circuits.subset_size(0) == n:
            x1 = int(lines[i].split(",")[0])
            x2 = int(lines[j].split(",")[0])
            return x1*x2

    raise RuntimeError()


def tests():
    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 25272, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")

