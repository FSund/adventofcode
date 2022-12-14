# Credit for this: Nicholas Swift
# as found at https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
from warnings import warn
import heapq
import numpy as np
import matplotlib.pyplot as plt

class Node:
    """
    A node class for A* Pathfinding
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
    
    def __repr__(self):
        return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

    # defining less than for purposes of heap queue
    def __lt__(self, other):
        return self.f < other.f
    
    # defining greater than for purposes of heap queue
    def __gt__(self, other):
        return self.f > other.f

def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Return reversed path


# https://gist.github.com/ryancollingwood/32446307e976a11a1185a5394d6657bc
def astar(maze, height, start, end, heuristic, viz=False, allow_diagonal_movement = False):
    """
    Returns a list of tuples as a path from the given start to the given end in the given maze
    :param maze:
    :param start:
    :param end:
    :return:
    """
    
    # visualize
    if viz:
        grid = np.zeros((len(maze), len(maze[0])))
        plt.ion()
        fig, ax = plt.subplots()
        if viz == 1:
            im = ax.imshow(grid, vmin=0, vmax=10)
        elif viz == 2:
            im = ax.imshow(grid, vmin=ord('a')-1, vmax=ord('z'))

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Heapify the open_list and Add the start node
    heapq.heapify(open_list) 
    heapq.heappush(open_list, start_node)

    # Adding a stop condition
    outer_iterations = 0
    # max_iterations = (len(maze[0]) * len(maze) // 2)
    max_iterations = 1e6

    # what squares do we search
    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)
    if allow_diagonal_movement:
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1),)

    # Loop until you find the end
    while len(open_list) > 0:
        outer_iterations += 1

        if outer_iterations > max_iterations:
            # if we hit this point return the path such as it is
            # it will not contain the destination
            warn("giving up on pathfinding too many iterations")
            return return_path(current_node)       
        
        # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            # plt.pause(10)
            return return_path(current_node)
        
        if viz:
            im.set_data(grid)
            fig.canvas.flush_events()

        # Generate children
        children = []
        
        for new_position in adjacent_squares: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            # if maze[node_position[0]][node_position[1]] != 0:
            #     continue
            
            # Ensure elevation increase is max 1
            current_height = height[current_node.position[0], current_node.position[1]]
            new_height = height[node_position[0], node_position[1]]
            if new_height - current_height > 1:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            # Child is on the closed list
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = heuristic(current_node, child)
            child.f = child.g + child.h

            # Child is already in the open list
            if len([open_node for open_node in open_list if child.position == open_node.position and child.g > open_node.g]) > 0:
                continue

            if viz:
                if viz == 1:
                    grid[child.position[0], child.position[1]] += 1
                elif viz == 2:
                    grid[child.position[0], child.position[1]] = height[child.position[0], child.position[1]]

            # Add the child to the open list
            heapq.heappush(open_list, child)

    plt.show()
    warn("Couldn't get a path to destination")
    print(f"{current_node=}")
    print(f"{end=}")
    return None


def example(print_maze = True):

    maze = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,] * 2,
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,] * 2,
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,] * 2,
            [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,] * 2,
            [0,0,0,1,1,0,0,1,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,] * 2,
            [0,0,0,1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,] * 2,
            [0,0,0,1,0,1,1,1,1,0,1,1,0,0,1,1,1,0,0,0,1,1,1,1,1,1,1,0,0,0,] * 2,
            [0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,1,1,0,1,0,0,0,0,0,0,1,1,1,0,] * 2,
            [0,0,0,1,0,1,1,0,1,1,0,1,1,1,0,0,0,0,0,1,0,0,1,1,1,1,1,0,0,0,] * 2,
            [0,0,0,1,0,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,1,0,1,0,1,1,] * 2,
            [0,0,0,1,0,1,0,1,1,0,1,1,1,1,0,0,1,1,1,1,1,1,1,0,1,0,1,0,0,0,] * 2,
            [0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,1,0,] * 2,
            [0,0,0,1,0,1,1,1,1,0,1,0,0,1,1,1,0,1,1,1,1,0,1,1,1,0,1,0,0,0,] * 2,
            [0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1,1,] * 2,
            [0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,] * 2,
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,] * 2,]
    
    start = (0, 0)
    end = (len(maze)-1, len(maze[0])-1)

    path = astar(maze, start, end)

    if print_maze:
      for step in path:
        maze[step[0]][step[1]] = 2
      
        for row in maze:
            line = []
            for col in row:
                if col == 1:
                    line.append("\u2588")
                elif col == 0:
                    line.append(" ")
                elif col == 2:
                    line.append(".")
        print("".join(line))

    print(path)


class BFSNode:
    def __init__(self, position, parent):
        self.position = position
    
    def __eq__(self, other):
        return self.position == other.position


def backtrace_bfs(parent, start, end):
    path = [end]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path


def find_a_bfs(maze, height, start, viz=False):
    visited = set() # to keep track of already visited nodes
    bfs_traversal = list()  # the BFS traversal result
    queue = list()  # queue
    parent = {}  # dict
    
    # push the root node to the queue and mark it as visited
    queue.append(start)
    visited.add(start)
    
    adjacent = ((0, -1), (0, 1), (-1, 0), (1, 0),)
    
    # visualize
    if viz:
        grid = np.zeros((len(maze), len(maze[0])))
        plt.ion()
        fig, ax = plt.subplots()
        if viz == 1:
            im = ax.imshow(grid, vmin=0, vmax=10)
        elif viz == 2:
            im = ax.imshow(grid, vmin=ord('a')-1, vmax=ord('z'))
    
    # loop until the queue is empty
    while queue:
        # pop the front node of the queue and add it to bfs_traversal
        current_node = queue.pop(0)
        bfs_traversal.append(current_node)
        
        if height[current_node[0], current_node[1]] == ord('a'):
            return backtrace_bfs(parent, start, current_node)
        
        if viz:
            if viz == 1:
                grid[current_node[0], current_node[1]] += 1
            elif viz == 2:
                grid[current_node[0], current_node[1]] = height[current_node[0], current_node[1]]
            im.set_data(grid)
            fig.canvas.flush_events()
        
        # check all the neighbour nodes of the current node
        for translation in adjacent:
            position = (current_node[0] + translation[0], current_node[1] + translation[1])
            
            # Make sure within range
            if position[0] > (len(maze) - 1) or position[0] < 0 or position[1] > (len(maze[0]) - 1) or position[1] < 0:
                continue
            
            # Ensure elevation decrease is max 1
            # (since we are searching backwards)
            current_height = height[current_node[0], current_node[1]]
            new_height = height[position[0], position[1]]
            if new_height - current_height < -1:
                continue

            # if the neighbour nodes are not already visited, 
            # push them to the queue and mark them as visited
            if position not in visited:
                visited.add(position)
                queue.append(position)
                parent[position] = current_node

    return bfs_traversal
    
if __name__ == "__main__":
    example()