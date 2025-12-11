from pathlib import Path
from typing import List, Dict


def get_input(filename):
    script_dir = Path(__file__).parent
    lines = []
    with open(script_dir / filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def all_paths_iterative(graph: Dict[str, List[str]], start: str, target: str) -> List[List[str]]:
    """
    Iterative version using explicit stack.
    Avoids recursion depth limits.
    
    Args:
        graph: Adjacency list
        start: Starting node
        target: Target node
    
    Returns:
        List of all unique paths
    """
    all_paths = []
    # Stack stores: (current_node, path_so_far, visited_set)
    stack = [(start, [start], {start})]
    
    while stack:
        node, path, visited = stack.pop()
        
        if node == target:
            all_paths.append(path)
            continue
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                # Create new path and visited set for this branch
                new_path = path + [neighbor]
                new_visited = visited | {neighbor}
                stack.append((neighbor, new_path, new_visited))
    
    return all_paths


def aoc(filename):
    lines = get_input(filename)

    # find every path from "you" to "out"

    graph = {}
    for line in lines:
        node, neighbors = [e.strip() for e in line.split(":")]
        neighbors = [e.strip() for e in neighbors.split(" ")]

        graph[node] = neighbors

    result = all_paths_iterative(graph, "you", "out")
    return len(result)
        

def tests():
    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 5, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
