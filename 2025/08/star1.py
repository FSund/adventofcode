from pathlib import Path
from dataclasses import dataclass
from collections import defaultdict
from functools import cache

def get_input(filename):
    script_dir = Path(__file__).parent
    lines = []
    with open(script_dir / filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines

@dataclass
class Box:
    x: int
    y: int
    z: int

    def __init__(self, coords):
        self.x = coords[0]
        self.y = coords[1]
        self.z = coords[2]

    def distance_to(self, box):
        return (self.x - box.x)**2 + (self.y - box.y)**2 + (self.z - box.z)**2


def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    
    while stack:
        node = stack.pop()
        
        if node not in visited:
            visited.add(node)
            # print(node, end=' ')
            
            # Add neighbors in reverse order to match recursive traversal
            for neighbor in reversed(graph[node]):
                if neighbor not in visited:
                    stack.append(neighbor)
    
    return visited


def aoc(filename, n_connections=1000):
    lines = get_input(filename)

    boxes = []
    for line in lines:
        boxes.append(Box([int(d) for d in line.split(",")]))

    # calculate distances
    dist = []
    n = len(boxes)
    for i in range(n):
        for j in range(i+1, n):
            d = boxes[i].distance_to(boxes[j])
            dist.append((d, (i,j)))
    
    dist = sorted(dist)

    graph = defaultdict(list)
    for d in dist[:n_connections]:
        i = d[1][0]
        j = d[1][1]
        
        # connect i to j
        graph[i].append(j)
        graph[j].append(i)

    keys = list(graph.keys())
    v_sets = set()
    for key in keys:
        visited = dfs_iterative(graph, key)
        v_sets.add(tuple(sorted(visited)))
        # sizes.append(len(visited))

    sizes = []
    for v in v_sets:
        sizes.append(len(v))

    sizes = list(reversed(sorted(sizes)))
    print(sizes)
    ans = 1
    for s in sizes[:3]:
        ans *= s

    return ans

            








def tests():
    ans = aoc("example.txt", 10)
    print(f"example: {ans}")
    assert ans == 40, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
