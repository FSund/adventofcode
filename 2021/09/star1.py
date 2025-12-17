from pathlib import Path
from typing import List, Dict
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

    ans = 0
    graph = defaultdict(lambda: 99)
    for j, line in enumerate(lines):
        for i, height in enumerate(line):
            graph[complex(i, j)] = int(height)

    ans = 0
    neighbors = [1, -1, 1j, -1j]  # 4 neighors
    keys = list(graph.keys())  # snapshot keys, since the dict can get new default elements during iteration
    for p in keys:
        low_point = True
        for dir in neighbors:
            if graph[p + dir] <= graph[p]:
                low_point = False
            
        if low_point:
            ans += 1 + graph[p]

    return ans
        

def tests():
    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 15, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
