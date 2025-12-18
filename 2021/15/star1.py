from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from typing import TypeVar, Hashable
from collections import defaultdict, deque
from functools import cache
import heapq


def get_input(filename):
    script_dir = Path(__file__).parent
    lines = []
    with open(script_dir / filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines

T = TypeVar('T', bound=Hashable)

def dijkstra(graph: Dict[T, List[Tuple[T, float]]], 
             start: T, 
             end: T) -> Tuple[Optional[float], Optional[List[T]]]:
    """
    Find shortest path in weighted graph using Dijkstra's algorithm.
    
    Args:
        graph: Adjacency list where graph[node] = [(neighbor, weight), ...]
        start: Starting node
        end: Target node
        
    Returns:
        Tuple of (total_cost, path) or (None, None) if no path exists
    """
    # Priority queue: (cost, node)
    pq = [(0.0, start)]
    
    # Track minimum cost to reach each node
    costs = {start: 0.0}
    
    # Track the path
    previous = {}
    
    while pq:
        current_cost, current_node = heapq.heappop(pq)
        
        # Found the target
        if current_node == end:
            path = []
            node = end
            while node in previous:
                path.append(node)
                node = previous[node]
            path.append(start)
            return current_cost, path[::-1]
        
        # Skip if we've already found a better path to this node
        if current_cost > costs.get(current_node, float('inf')):
            continue
            
        # Explore neighbors
        for neighbor, weight in graph.get(current_node, []):
            new_cost = current_cost + weight
            
            if new_cost < costs.get(neighbor, float('inf')):
                costs[neighbor] = new_cost
                previous[neighbor] = current_node
                heapq.heappush(pq, (new_cost, neighbor))
    
    return None, None  # No path found


def aoc(filename):
    lines = get_input(filename)

    risk = {}
    for i, line in enumerate(lines):
        for j, risk_level in enumerate(line):
            risk[(i, j)] = int(risk_level)

    graph = defaultdict(list)
    neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for pos, _weight in risk.items():
        for dir in neighbors:
            neigh = (pos[0] + dir[0], pos[1] + dir[1])
            if neigh in risk:
                weight = risk[neigh]
                graph[pos].append((neigh, weight))

    n = len(lines)
    start = (0, 0)
    end = (n-1, n-1)
    path = dijkstra(graph, start, end)

    return int(path[0])


def tests():
    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 40, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")