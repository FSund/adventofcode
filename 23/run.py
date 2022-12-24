import numpy as np

def get_input(filename="input.txt"):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))
    return lines


# def print_elves(elves):
#     for i in range(len(elves)):

neighbors = [
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
                map[i+offset[0],j+offset[1]] += 1
                elves.append(Elf((i+offset[0], j+offset[1])))
    
    suggestions = np.zeros((m + 2*offset[0], n + 2*offset[1]), dtype=int)
    
    # print_map(map)
    print_map(map[5:10,5:10])
    print()
    
    global propose_idx
    for i in range(2):
        for elf in elves:
            elf.propose_move(map, suggestions)
        for elf in elves:
            elf.do_move(map, suggestions)
        suggestions.fill(0)
        propose_idx += 1
        print_map(map[5:10,5:10])
        print()
        
    
    # print_map(map)



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
    solve("23/example.txt")