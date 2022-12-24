import numpy as np
from itertools import cycle

def get_input(filename="input.txt"):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))
    return lines


# def print_elves(elves):
#     for i in range(len(elves)):

all_neighbors = (
    (-1, -1), (-1, 0), (-1, 1),
    ( 0, -1),          ( 0, 1),
    ( 1, -1), ( 1, 0), ( 1, 1),
)

NORTH, SOUTH, WEST, EAST = range(4)
# propose_idx = NORTH

proposes = [[] for i in range(4)]
proposes[NORTH] = [-1,-1], [-1, 0], [-1, 1]
proposes[SOUTH] = [ 1,-1], [ 1, 0], [ 1, 1]
proposes[WEST] =  [-1,-1], [ 0,-1], [ 1,-1]
proposes[EAST] =  [-1, 1], [ 0, 1], [ 1, 1]


class Elf:
    propose_idx = None
    def __init__(self, pos):
        self.pos = pos
        self.new_pos = None
    
    def propose_move(self, grid, suggestions):
        self.new_pos = None

        # check total neighbors first
        total_neighbors = 0
        for neighbor in all_neighbors:
            i = self.pos[0] + neighbor[0]
            j = self.pos[1] + neighbor[1]
            total_neighbors += grid[i,j]
        if total_neighbors == 0:
            return

        for k in range(4):  # loop over 4 suggest directions
            # rotate to global direction
            direction = (Elf.propose_idx + k) % 4
            
            # count neighbors in direction
            n_neighbors = 0
            for pos in proposes[direction]:
                i = self.pos[0] + pos[0]
                j = self.pos[1] + pos[1]
                n_neighbors += grid[i,j]
            
            if n_neighbors == 0:
                # suggest move
                i = self.pos[0] + proposes[direction][1][0]
                j = self.pos[1] + proposes[direction][1][1]
                suggestions[i, j] += 1
                self.new_pos = (i, j)
                return

    def do_move(self, grid, suggestions):
        if self.new_pos is not None:
            i = self.new_pos[0]
            j = self.new_pos[1]
            if suggestions[i,j] == 1:
                grid[self.pos[0], self.pos[1]] = 0
                self.pos = (i, j)
                grid[self.pos[0], self.pos[1]] = 1


def print_map(map):
    lines = []
    for i in range(map.shape[0]):
        line = ""
        for j in range(map.shape[1]):
            line += "#" if map[i,j] else "."
        lines.append(line)
        print(line)
    return lines


def solve(filename, n_moves=10):
    lines = get_input(filename)
    m = len(lines)
    n = len(lines[0])
    offset = (m, n)
    shape = (m + 2*offset[0], n + 2*offset[1])
    grid = np.zeros(shape, dtype=int)
    print(grid.shape)
    elves = []
    for i in range(m):
        for j in range(n):
            if lines[i][j] == "#":
                ii = i+offset[0]
                jj = j+offset[1]
                grid[ii,jj] += 1
                elves.append(Elf((ii, jj)))
    
    suggestions = np.zeros(shape, dtype=int)
    
    # print_map(map)
    # print_map(map)
    # print()
    
    # global propose_idx
    propose_idx = cycle([NORTH, SOUTH, WEST, EAST])
    for i in range(n_moves):
        suggestions.fill(0)
        Elf.propose_idx = next(propose_idx)

        for elf in elves:
            elf.propose_move(grid, suggestions)
        
        # check number of proposed moves
        assert(np.sum(np.sum(suggestions)) <= len(elves))
        
        for elf in elves:
            elf.do_move(grid, suggestions)

        # print_map(map)
        # print()
    
        i0 = 1e9
        i1 = 0
        j0 = 1e9
        j1 = 0
        for elf in elves:
            assert(grid[elf.pos[0], elf.pos[1]] == 1)
            if elf.pos[0] > i1:
                i1 = elf.pos[0]
            if elf.pos[0] < i0:
                i0 = elf.pos[0]
            
            if elf.pos[1] > j1:
                j1 = elf.pos[1]
            if elf.pos[1] < j0:
                j0 = elf.pos[1]
        
        # print(f"{i0} {i1} {j0} {j1}")
        
        assert(np.sum(np.sum(grid)) == len(elves))
    
    # print_map(map[i0-1:i1+2, j0-1:j1+2])
    print(f"{i0 = }")
    print(f"{i1 = }")
    print(f"{j0 = }")
    print(f"{j1 = }")
    
    print(f"{i0-offset[0] = }")
    print(f"{i1-offset[0] = }")
    print(f"{j0-offset[1] = }")
    print(f"{j1-offset[1] = }")
    
    # min_x = min(elves, key=lambda x: x.pos[0]).pos[0]
    # print(f"{min_x = }")
    
    height = i1 - i0 + 1
    width = j1 - j0 + 1
    print(f"{width = }")
    print(f"{height = }")
    
    return width*height - len(elves)


example_round10 = [
    ".......#......",
    "...........#..",
    "..#.#..#......",
    "......#.......",
    "...#.....#..#.",
    ".#......##....",
    ".....##.......",
    "..#........#..",
    "....#.#..#....",
    "..............",
    "....#..#..#...",
    "..............",
]


if __name__ == "__main__":
    assert(solve("23/example.txt") == 110)
    
    # print(solve("23/example.txt", n_moves=10))
    
    print(f'star 1: {solve("23/input.txt")}')
    # 4246 is too high
    # 4162