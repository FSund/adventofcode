import numpy as np
import matplotlib.pyplot as plt
import numpy.typing as npt
from queue import PriorityQueue
from typing import Tuple
from star1 import bfs as bfs_star1


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
    start_pos: Tuple[int, int], # (i, j)
    end_pos: Tuple[int, int],  # (i, j)
    score_limit: int,
    viz=False
):
    # visited = set() # to keep track of already visited nodes
    # queue = list()  # queue
    queue = PriorityQueue()
    parent = {}  # dict, for backtrace
    
    # make start node
    start_node = (0,) + start_pos + (0,)  # (score, i, j, rot_idx)
    
    # push the root node to the queue and mark it as visited
    # queue.append(start)
    queue.put(start_node)
    # visited.add(start_node)
    
    # east is adjacent[0], add 1 to rotate clockwise and -1 to rotate counterclockwise
    directions = ((0, 1), (1, 0), (0, -1), (-1, 0),)
    n, m = grid.shape
    
    # visualize
    if viz:
        path_map = np.copy(grid)
        plt.ion()
        fig, ax = plt.subplots()
        im = ax.imshow(path_map, vmin=0, vmax=10)
    
    # lowest_score = np.inf
    
    paths = []
    
    # loop until the queue is empty
    while queue:
        # pop the front node of the queue and add it to bfs_traversal
        # current_node = queue.pop(0)
        if queue.empty():
            break
        current_node = queue.get()

        score = current_node[0]
        current_pos = (current_node[1], current_node[2], current_node[3])  # (i, j, rot_idx)
        i = current_pos[0]
        j = current_pos[1]
        rot_idx = current_pos[2]
        
        # print(f"{score = }")
        
        if viz:
            if path_map[i, j] != 2:
                path_map[i, j] = 2
                # im.set_data(path_map)
                im.set_array(path_map)
                fig.canvas.flush_events()
        
        if (i, j) == end_pos:
            print(f"reached end, {score = }, {score_limit = }")
            # if score == score_limit:
            #     paths.append(backtrace_bfs(parent, start_node, current_node))

            # if score < lowest_score:
            #     lowest_score = score
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
            (score +    1, i + dir[0],    j + dir[1],    rot_idx),  # forward
            (score + 1001, i + dir_1x[0], j + dir_1x[1], rot_1x ),  # turn right then move forward
            (score + 2001, i + dir_2x[0], j + dir_2x[1], rot_2x ),  # turn 180 then move forward
            (score + 1001, i + dir_3x[0], j + dir_3x[1], rot_3x ),  # turn left then move forward
        ]
        # dir = directions[rot_idx]
        # rot_r = (rot_idx + 1) % 4
        # rot_l = (rot_idx + 4 - 1) % 4
        # neighbor_nodes = [
        #     (score +    1, i + dir[0], j + dir[1], rot_idx),  # forward
        #     (score + 1000, i,          j,          rot_r  ),  # turn right (stay on same tile)
        #     (score + 1000, i,          j,          rot_l  ),  # turn left (stay on same tile)
        # ]
        for node in neighbor_nodes:
            # position = (node[0], node[1])
            position = (node[1], node[2], node[3])  # (i, j, <index of direction this tile was entered from>)
            i, j = position[0], position[1]
            
            # check if the node is already visited
            # includes both position and direction ???
            # if position in visited:
            #     continue
            
            # only skip if the score is higher than the lowest score
            new_score = node[0]
            if new_score > score_limit:
                continue
            
            # check if the node is a wall
            if grid[i, j] == 1:
                continue
            
            # make sure within range
            if i > (n - 1) or i < 0 or j > (m - 1) or j < 0:
                continue

            # if the neighbour nodes are not already visited, 
            # push them to the queue and mark them as visited
            # visited.add(position)
            # queue.append(node)
            queue.put(node)
            
            if node not in parent:
                parent[node] = [current_node]
            else:
                if current_node not in parent[node]:
                    parent[node].append(current_node)

            # parent[position] = current_pos
    
    # for rot_idx in range(4):
    #     path = backtrace_bfs(parent, start_node, (end[0], end[1], rot_idx))
    #     paths.append(path)
    
    tiles = set()
    queue = PriorityQueue()
    for node in parent.keys():
        i = node[1]
        j = node[2]
        if i == end_pos[0] and j == end_pos[1]:
            queue.put(node)

    new_grid = np.copy(grid)
    while queue:
        if queue.empty():
            break
        current_node = queue.get()
        tiles.add((current_node[1], current_node[2]))
        if current_node[1] == start_pos[0] and current_node[2] == start_pos[1]:
            continue

        parent_nodes = parent[current_node]
        
        for parent_node in parent_nodes:
            i = parent_node[1]
            j = parent_node[2]
            new_grid[i, j] = 9
            queue.put(parent_node)
        
    fig, ax = plt.subplots()
    im = ax.imshow(new_grid, vmin=0, vmax=10)
    fig.show()
    
    return tiles


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
    lowest_score = bfs_star1(grid, start + (rot_idx,), end)
    print(f"{lowest_score = }")
    tiles = bfs(grid, start, end, lowest_score, viz=False)
    print(f"{len(tiles) = }")
    
    return len(tiles)
    
    


def tests():
    ans = aoc("example3.txt")
    print(f"example: {ans = }")
    assert ans == 19, f"wrong answer: {ans}"
    
    # score 7036
    ans = aoc("example1.txt")
    print(f"example: {ans = }")
    assert ans == 45, f"wrong answer: {ans}"
    
    ans = aoc("example2.txt")
    print(f"example: {ans = }")
    assert ans == 64, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
    # assert ans == 1429911
    # 114408 too high
