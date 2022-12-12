import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
import time
from warnings import warn
from astar import astar


def find_next_position(height, i, j, end):
    dx = end[0] - i
    dy = end[1] - j
    l = sqrt(dx**2 + dy**2)
    dx = float(dx) / l
    dy = float(dy) / l
    
    if abs(dx) > abs(dy):
        return round(i + dx), j
    elif abs(dy) > abs(dx):
        return i, round(j + dy)
    elif abs(dx) == abs(dy):
        return round(i + dx), j
        
    raise RuntimeError

class Node:
    def __init__(self, parent, position, height):
        self.parent = parent
        self.position = position
        self.height = height
    
    def __repr__(self):
        return f"node position: {self.position}"
    
    def __eq__(self, other):
        return self.position == other.position

# Node.n = n
# Node.m = m

def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Return reversed path

def solve(height, start, end):
    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)

    # i = start[0]
    # j = start[1]
    # position = [start[0], start[1]]
    m, n = height.shape
    
    # visualize
    visit_grid = np.zeros((m, n), dtype=int)
    plt.ion()
    fig, ax = plt.subplots()
    im = ax.imshow(visit_grid, vmin=0, vmax=10)

    start_node = Node(None, start, height[start[0], start[1]])
    end_node = Node(None, end, height[end[0], end[1]])
    nodes = [start_node]
    iterations = 0
    max_iterations = (len(height[0]) * len(height) * 2)
    max_iterations = 10000
    visited = []
    while len(nodes) > 0:
        iterations += 1
        # i, j = find_next_position(height, i, j, end)
        # print([i, j])
        
        # pos_grid[i, j] += 1
        # im.set_data(pos_grid)
        # fig.canvas.flush_events()
        # time.sleep(0.01)
        
        # if i == end[0] and j == end[1]:
        #     break
        
        if iterations > max_iterations:
            warn("giving up on pathfinding too many iterations")
            break
        
        current_node = nodes.pop()
        visited.append(current_node)
        
        print(current_node)
        
        if current_node == end_node:
            print("DONE")
            return return_path(current_node)

        children = []
        for translation in adjacent_squares:
            new_position = (current_node.position[0] + translation[0], current_node.position[1] + translation[1])
            
            # ensure within bounds
            if new_position[0] < 0 or new_position[1] < 0 or new_position[0] >= (m-1) or new_position[1] >= (n-1):
                continue
            
            new_height = height[new_position[0], new_position[1]]
            
            # ensure valid height difference
            if new_height - current_node.height > 1:
                continue
            
            # Create new node
            new_node = Node(current_node, new_position, new_height)
            print(new_position)
            
            # visualize
            visit_grid[new_position[0], new_position[1]] += 1
            im.set_data(visit_grid)
            fig.canvas.flush_events()
            # print(np.max(np.max(visit_grid)))

            # Append
            children.append(new_node)

        for child in children:
            if len([closed_child for closed_child in visited if closed_child == child]) > 0:
                continue
            
            nodes.append(child)
        
        # print(len(nodes))

if __name__ == "__main__":
    lines = []
    with open("input.txt") as file:
        for line in file:
            lines.append(line.strip("\n"))

    # find start and end
    m = len(lines)
    n = len(lines[0])
    start = None
    end = None
    for i in range(m):
        if "S" in lines[i]:
            # start[0] = i
            # start[1] = lines[i].index("S")
            start = (i, lines[i].index("S"))
            # lines[i][start[1]] = "a"
        if "E" in lines[i]:
            # end[0] = i
            # end[1] = lines[i].index("E")
            end = (i, lines[i].index("E"))
            # lines[i][end[1]] = "z"

    height = np.empty((m, n), dtype=int)
    for i in range(m):
        for j in range(n):
            height[i, j] = ord(lines[i][j])

    # print(lines)

    # print(np.max(np.max(height)))
    # print(np.min(np.min(height)))

    height[height == ord('S')] = ord('a')
    height[height == ord('E')] = ord('z')

    # print(np.max(np.max(height)))
    # print(np.min(np.min(height)))

    if False:
        pos_grid = np.zeros((m, n), dtype=bool)
        pos_grid[start[0], start[1]] += 1

        plt.ion()
        fig, ax = plt.subplots()
        im = ax.imshow(pos_grid, vmin=0, vmax=1)

        # plt.imshow()
        # plt.show()

    # solve(height, start, end)
    
    # path = astar_dec12(height, start, end)
    maze = np.zeros((m, n), dtype=int)
    # def heuristic(parent, child):
    #     child_height = height[child.position[0], child.position[1]]
    #     parent_height = height[parent.position[0], parent.position[1]]
    #     if child_height - parent_height > 1:
    #         return int(1e9)
    #     else:
    #         dx = child.position[0] - parent.position[0]
    #         dy = child.position[1] - parent.position[1]
    #         return (dx ** 2) + (dy ** 2)
    
    # def heuristic(parent, child):
    #     # h(n) is a heuristic function that estimates the cost of the
    #     # cheapest path from n to the goal
    #     dx = child.position[0] - parent.position[0]
    #     dy = child.position[1] - parent.position[1]
    #     return (dx ** 2) + (dy ** 2)

    def heuristic(parent, child):
        # h(n) is a heuristic function that estimates the cost of the
        # cheapest path from n to the goal
        dx = end[0] - child.position[0]
        dy = end[1] - child.position[1]
        
        # L2 norm
        # return (dx ** 2) + (dy ** 2)
        
        # L1 norm -- use this for star 1
        # return abs(dx) + abs(dy)
        
        # use this for star 2?
        return 1

    # star 1
    if False:
        path = astar(maze, height, start, end, viz=False, heuristic=heuristic)
        print(len(path[1:]))
    
    # star 2
    start2 = (end[0], end[1])
    end2 = (start[0], start[1])
    path = astar(maze, height, start2, end2, viz=False, heuristic=heuristic)
    print(path)
    print(len(path))
