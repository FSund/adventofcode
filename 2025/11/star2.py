from pathlib import Path
from functools import cache


def get_input(filename):
    script_dir = Path(__file__).parent
    lines = []
    with open(script_dir / filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def aoc(filename):
    lines = get_input(filename)

    # make graph
    graph = {}
    for line in lines:
        node, neighbors = [e.strip() for e in line.split(":")]
        neighbors = [e.strip() for e in neighbors.split(" ")]

        graph[node] = neighbors

    @cache
    def count_paths_graph(start, end):
        """Count all unique paths from start to end in a directed graph."""        
        if start == end:
            return 1
    
        paths = 0
        for neighbor in graph.get(start, []):
            paths += count_paths_graph(neighbor, end)

        return paths

    # svr -> dac -> fft -> out
    p1 = count_paths_graph("svr", "dac")
    p2 = count_paths_graph("dac", "fft")
    p3 = count_paths_graph("fft", "out")
    ans = p1*p2*p3

    # svr -> fft -> dac -> out
    p1 = count_paths_graph("svr", "fft")
    p2 = count_paths_graph("fft", "dac")
    p3 = count_paths_graph("dac", "out")
    ans += p1*p2*p3
    
    return ans
        

def tests():
    ans = aoc("example2.txt")
    print(f"example: {ans}")
    assert ans == 2, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
