from pathlib import Path
from typing import List, Dict, Any
from collections import defaultdict


def get_input(filename):
    script_dir = Path(__file__).parent
    lines = []
    with open(script_dir / filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def dfs_path_exists(graph, start, target) -> bool:
    visited = set()
    stack = [start]
    
    while stack:
        node = stack.pop()
        
        if node == target:
            return True
        
        if node not in visited:
            visited.add(node)
            
            directions = [1, -1, 1j, -1j]  # 4 neighors
            for dir in directions:
                neighbor = node + dir
                if graph[neighbor] >= graph[start]:
                    continue
                if neighbor not in visited:
                    stack.append(neighbor)
    
    return False


def make_graph(lines):
    graph = defaultdict(lambda: 99)
    for i, line in enumerate(lines):
        for j, height in enumerate(line):
            graph[complex(i, j)] = int(height)

    return graph


def aoc(filename):
    lines = get_input(filename)

    graph = make_graph(lines)
    
    keys = list(graph.keys())  # snapshot keys, since the dict can get new default elements during iteration

    neighbors = [1, -1, 1j, -1j]  # 4 neighors
    low_points = []
    for point in keys:
        low_point = True
        for dir in neighbors:
            if graph[point + dir] <= graph[point]:
                low_point = False
            
        if low_point:
            low_points.append(point)

    # this is very badly optimized (should cache dfs for each basin)
    # but gets the result in 10 seconds or so
    basins = defaultdict(int)
    for point in keys:
        # "Locations of height `9` do not count as being in any basin"
        if graph[point] == 9:
            continue

        # check if this point belongs to any basins
        for low_point in low_points:
            if dfs_path_exists(graph, point, low_point):
                basins[low_point] += 1

    sizes = list(reversed(sorted(basins.values())))
    return sizes[0]*sizes[1]*sizes[2]
        

def tests():
    graph = make_graph(get_input("example.txt"))
    assert dfs_path_exists(graph, 8j, 9j)

    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 1134, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
