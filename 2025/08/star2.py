from pathlib import Path
from dataclasses import dataclass
from collections import defaultdict

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
            
            # Add neighbors in reverse order to match recursive traversal
            for neighbor in reversed(graph[node]):
                if neighbor not in visited:
                    stack.append(neighbor)
    
    return visited


def aoc(filename):
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
    for d in dist:
        i = d[1][0]
        j = d[1][1]
        
        # connect i to j
        graph[i].append(j)
        graph[j].append(i)

        # only need to check a single circuit, since if all of them are connected, all of them are connected
        visited = dfs_iterative(graph, 0)
        if len(visited) == len(boxes):
            return boxes[i].x*boxes[j].x


    raise RuntimeError()


def tests():
    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 25272, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
