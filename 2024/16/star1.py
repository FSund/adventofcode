import numpy as np
import matplotlib.pyplot as plt
import numpy.typing as npt
from queue import PriorityQueue
from typing import Tuple


def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def backtrace_bfs(parent, start, end):
    path = [end]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path


def bfs(
    grid: npt.DTypeLike,  # map with walls and free space
    _start: Tuple[Tuple[int, int, int]], # (i, j, rot_idx)
    end: Tuple[int, int],  # (i, j)
    viz=False
):
    visited = set() # to keep track of already visited nodes
    # queue = list()  # queue
    queue = PriorityQueue()
    
    # make start node
    start = (0,) + _start  # (score, i, j)
    
    # push the root node to the queue and mark it as visited
    # queue.append(start)
    queue.put(start)
    visited.add(start)
    
    # east is adjacent[0], add 1 to rotate clockwise and -1 to rotate counterclockwise
    directions = ((0, 1), (1, 0), (0, -1), (-1, 0),)
    n, m = grid.shape
    
    # visualize
    if viz:
        path_map = np.copy(grid)
        plt.ion()
        fig, ax = plt.subplots()
        im = ax.imshow(path_map, vmin=0, vmax=10)
    
    lowest_score = np.inf
    
    # loop until the queue is empty
    while queue:
        # pop the front node of the queue and add it to bfs_traversal
        # current_node = queue.pop(0)
        if queue.empty():
            break
        current_node = queue.get()

        score = current_node[0]
        i = current_node[1]
        j = current_node[2]
        rot_idx = current_node[3]
        
        if viz:
            path_map[i, j] = 2
            # im.set_data(path_map)
            im.set_array(path_map)
            fig.canvas.flush_events()
        
        if (i, j) == end:
            print(f"END, {score = }, {lowest_score = }")
            if score < lowest_score:
                lowest_score = score
            continue
        
        # check all the neighbour nodes of the current node
        # neighbor nodes are
        # 1) forward (+1 score)
        # 2) turn left (+1000 score)
        # 3) turn right (+1000 score)
        dir = directions[rot_idx]
        rot_1x = (rot_idx + 1) % 4
        dir_1x = directions[rot_1x]
        rot_2x = (rot_idx + 2) % 4
        dir_2x = directions[rot_2x]
        rot_3x = (rot_idx + 3) % 4
        dir_3x = directions[rot_3x]
        neighbor_nodes = [
            (score + 1, i + dir[0], j + dir[1], rot_idx),
            (score + 1001, i + dir_1x[0], j + dir_1x[1], rot_1x),
            (score + 2001, i + dir_2x[0], j + dir_2x[1], rot_2x),
            (score + 1001, i + dir_3x[0], j + dir_3x[1], rot_3x),
        ]
        for node in neighbor_nodes:
            # position = (node[0], node[1])
            position = (node[1], node[2], node[3])
            i, j = position[0], position[1]
            
            # check if the node is already visited
            # includes both position and direction ???
            if position in visited:
                continue
            
            # check if the node is a wall
            if grid[i, j] == 1:
                continue
            
            # make sure within range
            if i > (n - 1) or i < 0 or j > (m - 1) or j < 0:
                continue

            # if the neighbour nodes are not already visited, 
            # push them to the queue and mark them as visited
            visited.add(position)
            # queue.append(node)
            queue.put(node)
    
    return lowest_score


def aoc(filename):
    lines = get_input(filename)
    
    for line in lines:
        for c in line:
            if c == "S":
                start = (lines.index(line), line.index(c))
            elif c == "E":
                end = (lines.index(line), line.index(c))
    
    grid = np.zeros((len(lines), len(lines[0])))
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == "#":
                grid[i, j] = 1
            elif c == "E":
                grid[i, j] = 10
    
    rot_idx = 0
    return bfs(grid, start + (rot_idx,), end, viz=False)
    
    


def tests():
    ans = aoc("example2.txt")
    print(f"example star 1: {ans}")
    assert ans == 11048, f"wrong answer: {ans}"
    
    ans = aoc("example1.txt")
    print(f"example star 1: {ans}")
    assert ans == 7036, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"star 1: {ans}")
    # assert ans == 1429911
    # 114408 too high
