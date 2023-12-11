import math
import numpy as np
import matplotlib.pyplot as plt

def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))
    return lines


def expand(m):
    for i in range(m.shape[0])[::-1]:  # reverse loop
        if np.sum(m[i,:] == 0) == m.shape[1]:
            # add row
            # print(m.shape)
            m = np.insert(m, i, 0, axis=0)
            # print(f"shape after row add: {m.shape}")
    
    for j in range(m.shape[1])[::-1]:  # reverse loop
        if np.sum(m[:,j] == 0) == m.shape[0]:
            # add column
            m = np.insert(m, j, 0, axis=1)
            # print(f"shape after col add: {m.shape}")
            
    return m

def input_to_matrix(lines):
    m = np.zeros([len(lines), len(lines[0])])
    stoi = {
        ".": 0,
        "#": 1,
    }
    
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            s = lines[i][j]
            m[i,j] = stoi[s]
    return m

def matrix_to_str(m):
    itos = {
        0: ".",
        1: "#",
    }
    s = ""
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            s += itos[m[i,j]]
        s += "\n"

    return s

class Galaxy:
    def __init__(self, idx, x, y):
        self.idx = idx
        self.x = x
        self.y = y
        # self.nearest = None
        # self.distance = math.inf
        self.sum_of_paths = 0

    def __repr__(self):
        return f"Galaxy {self.idx} at ({self.x}, {self.y}), sum of paths: {self.sum_of_paths}"
        # if self.nearest:
        #     return f"Galaxy {self.idx} at ({self.x}, {self.y}), nearest: {self.nearest.idx}, distance: {self.distance}"
        # else:
        #     return f"Galaxy {self.idx} at ({self.x}, {self.y})"

def star1(filename):
    lines = get_input(filename)
    m = input_to_matrix(lines)
    m = expand(m)
    
    # galaxies = []
    # for i in range(m.shape[0]):
    #     for j in range(m.shape[1]):
    #         if m[i,j] == 1:
    #             galaxies.append((i,j))
    
    galaxies = []
    k = 1
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            if m[i,j] == 1:
                galaxies.append(Galaxy(k, i, j))
                k += 1
    # print(galaxies)
    
    # nearest = 
    for idx, galaxy in enumerate(galaxies):
        
        # for other_galaxy in galaxies[idx+1:]:
        for other_galaxy in galaxies[idx+1:]:
            if other_galaxy == galaxy:
                continue
            # manhattan distance
            dist = abs(galaxy.x - other_galaxy.x) + abs(galaxy.y - other_galaxy.y)
            # if galaxy.distance > dist:
            #     galaxy.distance = dist
            #     galaxy.nearest = other_galaxy
            galaxy.sum_of_paths += dist

    # print(nearest)
    # print(galaxies)

    # sum = 0
    # for _, dist in nearest.values():
    #     sum += dist
    
    sum = 0
    for galaxy in galaxies:
        sum += galaxy.sum_of_paths

    return sum
    
def star2(filename):
    lines = get_input(filename)
    


def tests():
    m = input_to_matrix(get_input("example.txt"))
    m = expand(m)
    assert m.shape[0] == 12
    assert m.shape[1] == 13
    
    l = matrix_to_str(m)
    # print(l)
    assert l == (
"""\
....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#.......
""")


if __name__ == "__main__":
    tests()

    example = star1("example.txt")
    print(f'Example: {example}')
    assert(example == 374)
    
    print(f'First star: {star1("input.txt")}')
    # assert(star1("input.txt") == 6838)
    
    # example = star2("example2.txt")
    # print(f"Star 2 example: {example}")
    # assert example == 10
    
    # assert star2("example3.txt") == 8

    # ans = star2("input.txt")
    # # assert ans == 12833235391111
    # print(f'Second star: {ans}')

    # 6489 too high
    # 3534 too high
    # 712 too high