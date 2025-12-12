from pathlib import Path
from typing import List, Dict
import numpy as np


def get_input(filename):
    script_dir = Path(__file__).parent
    lines = []
    with open(script_dir / filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def dfs_path_exists(graph: Dict[int, List[int]], start: int, target: int) -> bool:
    """
    Check if a path exists between two nodes using DFS.
    
    Args:
        graph: Adjacency list representation of the graph
        start: Starting node
        target: Target node
    
    Returns:
        True if path exists, False otherwise
    """
    visited = set()
    stack = [start]
    
    while stack:
        node = stack.pop()
        
        if node == target:
            return True
        
        if node not in visited:
            visited.add(node)
            
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    stack.append(neighbor)
    
    return False


def aoc(filename):
    lines = get_input(filename)

    presents = []
    regions = []
    for line in lines:
        if "x" in line:
            regions.append(line)
        elif ":" in line:
            presents.append([])
        elif "#" in line or "." in line:
            presents[-1].append(line)
        else:
            # should be an empty line
            assert line == ""

    ans = 0
    for region in regions:
        size, quantities = region.split(":")
        size = [int(d) for d in size.strip().split("x")]
        quantities = [int(q) for q in quantities.split()]

        present_area = 0
        for idx, quantity in enumerate(quantities):
            present_area += quantity * 9  # at most 9 squares per present

        if present_area <= size[0] * size[1]:
            # print("WILL FIT")
            ans += 1
        else:
            # print("WON'T FIT")
            pass

    return ans

def tests():
    ans = aoc("example.txt")
    print(f"example: {ans}")
    # assert ans == 2, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
