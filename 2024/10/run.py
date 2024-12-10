import numpy as np
import matplotlib.pyplot as plt


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


def bfs(height, start, viz=False):
    visited = set() # to keep track of already visited nodes
    bfs_traversal = list()  # the BFS traversal result
    queue = list()  # queue
    parent = {}  # dict
    
    # push the root node to the queue and mark it as visited
    queue.append(start)
    visited.add(start)
    
    adjacent = ((0, -1), (0, 1), (-1, 0), (1, 0),)
    n, m = height.shape
    
    # visualize
    if viz:
        grid = np.zeros((n, m))
        plt.ion()
        fig, ax = plt.subplots()
        im = ax.imshow(grid, vmin=0, vmax=10)
    
    paths = []
    
    # loop until the queue is empty
    while queue:
        # pop the front node of the queue and add it to bfs_traversal
        current_node = queue.pop(0)
        bfs_traversal.append(current_node)
        
        if height[current_node[0], current_node[1]] == 9:
            paths.append(backtrace_bfs(parent, start, current_node))
        
        if viz:
            grid[current_node[0], current_node[1]] = height[current_node[0], current_node[1]]
            im.set_data(grid)
            fig.canvas.flush_events()
        
        # check all the neighbour nodes of the current node
        for translation in adjacent:
            position = (current_node[0] + translation[0], current_node[1] + translation[1])
            
            # Make sure within range
            if position[0] > (n - 1) or position[0] < 0 or position[1] > (m - 1) or position[1] < 0:
                continue
            
            # Ensure elevation increase is exactly 1
            current_height = height[current_node[0], current_node[1]]
            new_height = height[position[0], position[1]]
            if new_height - current_height != 1:
                continue

            # disable this check to get _all_ paths to each 9
            # check later for unique endpoints to get score
            # if position in visited:
            #     continue
            
            # if the neighbour nodes are not already visited, 
            # push them to the queue and mark them as visited
            visited.add(position)
            queue.append(position)
            parent[position] = current_node

    # a trailhead's score is the number of 9-height positions
    # reachable from that trailhead via a hiking trail
    niners = []
    for path in paths:
        niners.append((path[-1][0], path[-1][1]))
    niners = set(niners)
    score = len(niners)

    # calculate rating
    # A trailhead's rating is the number of distinct hiking trails
    # which begin at that trailhead.
    rating = len(paths)
    
    return score, rating


def aoc(filename, star2=False):
    lines = get_input(filename)
    
    n = len(lines)
    m = len(lines[0])
    height = np.zeros((len(lines), len(lines[0])))
    for i in range(n):
        for j in range(m):
            height[i, j] = int(lines[i][j])
    
    
    total_scores = 0
    total_ratings = 0
    for i in range(n):
        for j in range(m):
            if height[i, j] == 0:
                score, rating = bfs(height, (i, j))
                total_scores += score
                total_ratings += rating
    
    if star2:
        return total_ratings
    else:
        return total_scores


def tests():
    ans = aoc("example.txt")
    print(f"example star 1: {ans}")
    assert ans == 36, f"wrong answer: {ans}"
    
    ans = aoc("example.txt", star2=True)
    print(f"example star 2: {ans}")
    assert ans == 81, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"star 1: {ans}")
    assert ans == 667
    
    ans = aoc("input.txt", star2=True)
    print(f"star 2: {ans}")
    assert ans == 1344
