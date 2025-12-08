from pathlib import Path
from functools import cache

def get_input(filename):
    script_dir = Path(__file__).parent
    lines = []
    with open(script_dir / filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines

graph = {}
visited = set()

@cache
def count_paths_dfs(start, goal):    
    if start[0] == goal[0]:  # only check first index
        return 1
    
    visited.add(start)
    path_count = 0
    
    for neighbor in graph[start]:
        if neighbor not in visited:
            path_count += count_paths_dfs(neighbor, goal)
    
    visited.remove(start)  # Backtrack
    return path_count


def aoc(filename):
    lines = get_input(filename)
    global graph
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == "^":
                graph[(i, j)] = [(i+1, j-1), (i+1, j+1)]
            else:
                graph[(i, j)] = [(i+1, j)]
    
    j = lines[0].find("S")
    node = (0, j)
    target = (len(lines) - 1, 0)
    ans = count_paths_dfs(node, target)

    return ans


def tests():
    ans = aoc("example2.txt")
    print(f"example: {ans}")
    assert ans == 4

    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 40, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
