import numpy as np

def get_input(filename="input.txt"):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))
    return lines


# def print_elves(elves):
#     for i in range(len(elves)):

all_neighbors = [
    [-1, -1], [-1, 0], [-1, 1],
    [ 0, -1],          [ 0, 1],
    [ 1, -1], [ 1, 0], [1,  1],
]

NORTH, SOUTH, WEST, EAST = range(4)
propose_idx = NORTH

proposes = [[] for i in range(4)]
proposes[NORTH] = [-1,-1], [-1, 0], [-1, 1]
proposes[SOUTH] = [ 1,-1], [ 1, 0], [ 1, 1]
proposes[WEST] =  [-1,-1], [ 0,-1], [ 1,-1]
proposes[EAST] =  [-1, 1], [ 0, 1], [ 1, 1]


class Elf:
    def __init__(self, pos):
        self.pos = pos
        self.suggestion = None
    
    def propose_move(self, map, suggestions):
        self.suggestion = None

        # check total neighbors first
        total_neighbors = 0
        for neighbor in all_neighbors:
            i = self.pos[0] + neighbor[0]
            j = self.pos[1] + neighbor[1]
            total_neighbors += map[i,j]
        if total_neighbors == 0:
            return
            
        for dx in range(4):  # loop over 4 suggest directions
            idx = (propose_idx + dx) % 4
            
            # count neighbors in direction
            n_neighbors = 0
            for neigh in proposes[idx]:
                i = self.pos[0] + neigh[0]
                j = self.pos[1] + neigh[1]
                n_neighbors += map[i,j]
            
            if n_neighbors == 0:
                # suggest move
                i = self.pos[0] + proposes[idx][1][0]
                j = self.pos[1] + proposes[idx][1][1]
                suggestions[i, j] += 1
                self.suggestion = (i, j)
                return

    def do_move(self, map, suggestions):
        if self.suggestion:
            i = self.suggestion[0]
            j = self.suggestion[1]
            if suggestions[i,j] == 1:
                map[self.pos[0], self.pos[1]] -= 1
                self.pos = (i,j)
                map[self.pos[0], self.pos[1]] += 1
                return True
            else:
                return False
        else:
            return False


def print_map(map):
    lines = []
    for i in range(map.shape[0]):
        line = ""
        for j in range(map.shape[1]):
            line += "#" if map[i,j] else "."
        lines.append(line)
        print(line)
    return lines


def solve(filename):
    lines = get_input(filename)
    m = len(lines)
    n = len(lines[0])
    offset = (m, n)
    map = np.zeros((m + 2*offset[0], n + 2*offset[1]), dtype=int)
    elves = []
    for i in range(m):
        for j in range(n):
            if lines[i][j] == "#":
                ii = i+offset[0]
                jj = j+offset[1]
                map[ii,jj] += 1
                elves.append(Elf((ii, jj)))
    
    suggestions = np.zeros((m + 2*offset[0], n + 2*offset[1]), dtype=int)
    
    # print_map(map)
    # print_map(map)
    # print()
    
    global propose_idx
    for i in range(10):
        for elf in elves:
            elf.propose_move(map, suggestions)
        for elf in elves:
            elf.do_move(map, suggestions)
        suggestions.fill(0)
        propose_idx += 1
        # print_map(map)
        # print()
    
    # print_map(map)
    
    i0 = 1e9
    i1 = 0
    j0 = 1e9
    j1 = 0
    for elf in elves:
        if elf.pos[0] > i1:
            i1 = elf.pos[0]
        if elf.pos[0] < i0:
            i0 = elf.pos[0]
        
        if elf.pos[1] > j1:
            j1 = elf.pos[1]
        if elf.pos[1] < j0:
            j0 = elf.pos[1]
    
    # print_map(map[i0:i1+1, j0:j1+1])
    # print(f"{i0 = }")
    # print(f"{i1 = }")
    # print(f"{i1-i0}")
    # print(f"{j0 = }")
    # print(f"{j1 = }")
    # print(f"{j1-j0}")
    return (i1-i0+1)*(j1-j0+1) - len(elves)


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
    print(f'star 1: {solve("23/example.txt")}')