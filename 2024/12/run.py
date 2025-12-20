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


def bfs(map: np.typing.DTypeLike, start, viz=False):
    visited = set() # to keep track of already visited nodes
    bfs_traversal = list()  # the BFS traversal result
    queue = list()  # queue
    parent = {}  # dict
    
    # push the root node to the queue and mark it as visited
    queue.append(start)
    visited.add(start)
    
    adjacent = ((0, -1), (0, 1), (-1, 0), (1, 0),)
    n, m = map.shape
    
    # visualize
    if viz:
        grid = np.zeros((n, m))
        plt.ion()
        fig, ax = plt.subplots()
        im = ax.imshow(grid, vmin=0, vmax=10)
        # add grid
        ax.set_xticks(np.arange(-.5, m, 1), minor=True)
        ax.set_yticks(np.arange(-.5, n, 1), minor=True)
        ax.grid(which='minor', color='w', linestyle='-')
        
    
    area = 0
    perimeter = 0
    
    # loop until the queue is empty
    while queue:
        # pop the front node of the queue and add it to bfs_traversal
        current_node = queue.pop(0)
        bfs_traversal.append(current_node)
        
        area += 1
        
        if viz:
            grid[current_node[0], current_node[1]] = map[current_node[0], current_node[1]]
            im.set_data(grid)
            fig.canvas.flush_events()
        
        # check all the neighbour nodes of the current node
        for translation in adjacent:
            position = (current_node[0] + translation[0], current_node[1] + translation[1])
            
            # make sure within range
            if position[0] > (n - 1) or position[0] < 0 or position[1] > (m - 1) or position[1] < 0:
                perimeter += 1
                continue

            # disable this check to get _all_ paths to each 9
            # check later for unique endpoints to get score
            if position in visited:
                continue
            
            # don't visit neighbors of different type, but add to perimeter
            if map[position[0], position[1]] != map[start[0], start[1]]:
                perimeter += 1
                continue
            
            # if the neighbour nodes are not already visited, 
            # push them to the queue and mark them as visited
            visited.add(position)
            queue.append(position)
            parent[position] = current_node
    
    # the price of fence required for a region is found by multiplying that
    # region's area by its perimeter
    return area, perimeter, visited


def find_number_of_sides(_map, start, viz=False):
    # expand map to avoid boundary issues
    map = np.copy(_map)
    map = np.pad(map, ((1,1), (1,1)), mode="constant", constant_values=(0,0))
    assert map.shape == (_map.shape[0] + 2, _map.shape[1] + 2)
    
    this = complex(start[0]+1, start[1]+1)  # offset by pad
    other = None
    dir = complex(1, 0)  # direction we are moving
    other_dir = dir * 1j  # the direction of the neighbor we are comparing to
    t = map[int(this.real), int(this.imag)]
    
    # visualize
    n, m = map.shape
    if viz:
        grid = np.zeros((n, m))
        grid[map == map[int(this.real), int(this.imag)]] = 1
        grid[int(this.real), int(this.imag)] = 2
        plt.ion()
        fig, ax = plt.subplots()
        im = ax.imshow(grid, vmin=0, vmax=10)
        # add grid
        ax.set_xticks(np.arange(-.5, m, 1), minor=True)
        ax.set_yticks(np.arange(-.5, n, 1), minor=True)
        ax.grid(which='minor', color='w', linestyle='-')
        
    
    # first locate starting edge
    while True:
        other = this + other_dir
        if map[int(other.real), int(other.imag)] != t:
            # found neighbor of different type
            break
        else:
            # rotate 90 degrees
            dir *= 1j
            other_dir *= 1j
    
    sides = 1
    while True:
        # either rotate or move
        
        # check next point if we continue in same direction
        this_next = this + dir
        other_next = this_next + other_dir
        if int(this_next.real) == start[0] and int(this_next.imag) == start[1]:
            # finished traversing
            break
        elif map[int(this_next.real), int(this_next.imag)] == t and map[int(other_next.real), int(other_next.imag)] != t:
            # continue in this direction
            this = this_next
            other = other_next
        else:
            while not (map[int(this_next.real), int(this_next.imag)] == t and map[int(other_next.real), int(other_next.imag)] != t):
                dir *= 1j
                other_dir *= 1j
                this_next = this + dir
                other_next = this_next + other_dir
            sides += 1
        
        if viz:
            grid[int(this.real), int(this.imag)] = 2
            im.set_data(grid)
            fig.canvas.flush_events()
        
        if True:
            pass
        
        # action: rotate
        # - new edge, given the following conditions: TODO
        # - don't translate, only rotate
        # - always rotate same direction (clockwise or anti-clockwise, pick one and stick to it)
        # - can rotate multiple times (in case of dead end), but this should be handled in successive iterations
        
        # action: move
        # - same edge
        
    return sides


class Robot:
    adjacent = ((0, 1), (-1, 0), (0, -1), (1, 0),)

    def __init__(self):
        self.pos = None
        self.dir_idx = 0
        self.dir = self.adjacent[self.dir_idx]
    
    def _turn(self):
        self.dir_idx = (self.dir_idx + 1) % len(self.adjacent)
        self.dir = self.adjacent[self.dir_idx]
    
    def count_walls(self, map, start, viz=False):
        self.pos = (start[0], start[1])

        walls = 0
        size = map.shape[0]
        t = map[self.pos[0], self.pos[1]]
        
        visited = []  # position and direction
        
        # visualize
        if viz:
            grid = np.zeros((size, size), dtype=int)
            grid[map == map[start[0], start[1]]] = 1
            grid[start[0], start[1]] = 2
            plt.ion()
            fig, ax = plt.subplots()
            im = ax.imshow(grid, vmin=0, vmax=10)
            # add grid
            ax.set_xticks(np.arange(-.5, size, 1), minor=True)
            ax.set_yticks(np.arange(-.5, size, 1), minor=True)
            ax.grid(which='minor', color='w', linestyle='-')
        
        loop_start = None
        while True:
            i = self.pos[0] + self.dir[0]
            j = self.pos[1] + self.dir[1]
            if i < 0 or j < 0 or i >= size or j >= size:
                # next pos is outside map
                self._turn()
                walls += 1
                continue
            
            if map[i, j] != t:
                # next pos is different type
                self._turn()
                walls += 1
                continue
            
            # if i == start[0] and j == start[1] and self.dir == self.adjacent[0]:
            #     # back at the beginning, finished
            #     return walls
            
            pos = (i, j)
            if loop_start is None:
                if (pos, self.dir) in visited:
                    # found loop start position
                    loop_start = (pos, self.dir)
                    walls = 0
            else:
                if (pos, self.dir) == loop_start:
                    # loop completed
                    return walls

            self.pos = pos
            visited.append((self.pos, self.dir))
            
            if viz:
                grid[pos[0], pos[1]] = 2
                im.set_data(grid)
                fig.canvas.flush_events()


def find_num_walls(_map: np.typing.DTypeLike, start, visited):
    # visited = list(visited)
    # row_sorted = sorted(visited, key=lambda x: x[0])  # sort by first index
    # col_sorted = sorted(visited, key=lambda x: x[1])  # sort by second index
    
    t = _map[start[0], start[1]]
    
    # checked = set()
    
    # pad to include boundary walls
    map = np.copy(_map)
    map = np.pad(map, ((1,1), (1,1)), mode="constant", constant_values=(0,0))
    n, m = map.shape
    
    n_walls = 0
    
    # check rows
    for i in range(0, n-1):
        # check if top is t and bottom is not t
        on_wall = False
        for j in range(m):
            if (i-1, j-1) in visited and map[i+1, j] != t:
                if on_wall:
                    pass
                else:
                    on_wall = True
                    n_walls += 1
            else:
                on_wall = False

    for i in range(0, n-1):
        # check if top is not t and bottom is t
        on_wall = False
        for j in range(m):
            if (i+1-1, j-1) in visited and map[i, j] != t:
                if on_wall:
                    pass
                else:
                    on_wall = True
                    n_walls += 1
            else:
                on_wall = False
    
    # check cols
    for j in range(0, m-1):
        # check if left is t and right is not t
        on_wall = False
        for i in range(n):
            if (i-1, j-1) in visited and map[i, j+1] != t:
                if on_wall:
                    pass
                else:
                    on_wall = True
                    n_walls += 1
            else:
                on_wall = False

        # check if top is not t and bottom is t
        on_wall = False
        for i in range(n):
            if (i-1, j+1-1) in visited and map[i, j] != t:
                if on_wall:
                    pass
                else:
                    on_wall = True
                    n_walls += 1
            else:
                on_wall = False
    
    return n_walls


def make_map(lines):
    n = len(lines)
    m = len(lines[0])
    map = np.zeros((n, m), dtype=int)
    for i in range(n):
        for j in range(m):
            map[i, j] = ord(lines[i][j])
    
    return map


def aoc(filename, star2=False):
    lines = get_input(filename)
    
    n = len(lines)
    m = len(lines[0])
    map = make_map(lines)
    
    cost = 0
    cost2 = 0
    robot = Robot()
    for i in range(n):
        for j in range(m):
            if map[i, j] != 0:
                area, perimeter, visited = bfs(map, (i, j))
                cost += area * perimeter
                
                # sides = find_number_of_sides(map, (i, j), True)  # do this before editing map
                # cost2 += area * sides
                
                # walls = robot.count_walls(map, (i, j), viz=True)
                if star2:
                    walls = find_num_walls(map, (i, j), visited)
                    cost2 += area * walls
                
                # set all visited to 0 so we don't try this area again
                for v in visited:
                    map[v[0], v[1]] = 0
    
    if star2:
        return cost2
    else:
        return cost


def tests():
    lines = [
        "AAA",
        "ABA",
        "AAA",
    ]
    map = make_map(lines)
    visited = set()
    visited.add((0,0))
    visited.add((0,1))
    visited.add((0,2))
    visited.add((1,0))
    visited.add((1,2))
    visited.add((2,0))
    visited.add((2,1))
    visited.add((2,2))
    assert find_num_walls(map, (0, 0), visited) == 8

    visited = set()
    visited.add((1,1))
    assert find_num_walls(map, (1, 1), visited) == 4
    
    lines = [
        "RRRRIICCFF",
        "RRRRIICCCF",
        "VVRRRCCFFF",
        "VVRCCCJFFF",
        "VVVVCJJCFE",
        "VVIVCCJJEE",
        "VVIIICJJEE",
        "MIIIIIJJEE",
        "MIIISIJEEE",
        "MMMISSJEEE",
    ]
    map = make_map(lines)
    # find_num_walls(map, (0, 0)) == 10  # R
    # find_num_walls(map, (0, 4)) == 4   # I
    # find_num_walls(map, (0, 6)) == 14  # C
    # find_num_walls(map, (0, 9)) == 10  # F
    
    # find_num_walls(map, (2, 0)) == 13  # V
    # find_num_walls(map, (3, 6)) == 11  # J
    visited = set()
    visited.add((4,7))
    assert find_num_walls(map, (4, 7), visited) == 4   # the lone C
    
    lines = [
        "AAAAAA",
        "AAABBA",
        "AAABBA",
        "ABBAAA",
        "ABBAAA",
        "AAAAAA",
    ]
    
    map = make_map(lines)
    robot = Robot()
    walls = robot.count_walls(map, (1,3))  # upper right B's
    assert walls == 4
    
    ans = aoc("example.txt")
    print(f"example star 1: {ans}")
    assert ans == 1930, f"wrong answer: {ans}"
    
    ans = aoc("example.txt", star2=True)
    print(f"example star 2: {ans}")
    assert ans == 1206, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"star 1: {ans}")
    assert ans == 1452678
    
    ans = aoc("input.txt", star2=True)
    print(f"star 2: {ans}")
    # assert ans == 1344
