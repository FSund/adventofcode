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


def dfs_all_paths(graph: Dict[str, List[str]], start: str, target: str) -> List[List[str]]:
    def dfs_helper(node: Any, target: Any, path: List[Any]) -> List[List[Any]]:
        if node == target:
            return [path]
        
        all_paths = []
        for neighbor in graph.get(node, []):
            # check if small cave is visited more than once
            if neighbor.islower() and neighbor in path:
                continue
            else:
                # visited.add(neighbor)
                all_paths.extend(dfs_helper(neighbor, target, path + [neighbor]))
                # visited.remove(neighbor)
        
        return all_paths
    
    return dfs_helper(start, target, [start])


def aoc(filename):
    lines = get_input(filename)
    graph = defaultdict(list)
    for line in lines:
        start, end = line.split("-")
        graph[start].append(end)
        
        # add backwards connection
        if start != "start" and end != "end":
            graph[end].append(start)
    
    paths = dfs_all_paths(graph, "start", "end")
    return len(paths)
        

def tests():
    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 10, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
