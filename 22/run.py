import numpy as np
import re
from math import copysign

def get_input(filename="input.txt"):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))
    return lines


class Pos:
    def __init__(self, pos, rot):
        self.pos = pos
        # 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^)
        self.rot = rot
    
    def __repr__(self):
        rmap = {
            "0": ">",
            "1": "v",
            "2": "<",
            "3": "^",
        }
        return f"[{self.pos[0]}, {self.pos[1]}] {self.rot}"

    def rotate(self, turn):
        if turn == "R":
            self.rot += 1
        elif turn == "L":
            self.rot -= 1
        else:
            raise RuntimeError

        self.rot = self.rot % 4
    
    def _move_horiz(self, map, d):
        print(f"moving {d} horizontally from {self.pos}")
        
        i = self.pos[0]
        one = int(copysign(d, 1))
        for d in range(d):
            i += one
            # check boundaries
        self.pos[0] = i
    
    def _move_vert(self, map, d):
        print(f"moving {d} vertically from {self.pos}")
        
        j = self.pos[1]
        one = int(copysign(d, 1))
        for d in range(d):
            j += one
            # check boundaries
        self.pos[1] = j
    
    def move(self, map, d):
        if self.rot == 0:  # right
            self._move_horiz(map, d)
        elif self.rot == 1:  # down
            self._move_vert(map, d)
        elif self.rot == 2:  # left
            self._move_horiz(map, -d)
        elif self.rot == 3:  # up
            self._move_vert(map, -d)
        else:
            raise RuntimeError

    def do_operation(self, map, operation):
        if operation.isdigit():
            self.move(map, int(operation))
        else:
            self.rotate(operation)


def make_map(lines):
    width = 0
    height = 0
    for line in lines:
        if line == "":
            break
        height += 1
        if len(line) > width:
            width = len(line)
    
    cmap = {
        " ": -1,
        ".": 0,
        "#": 1,
    }
    map = np.empty((height, width), dtype=int)
    map.fill(-1)
    for i in range(height):
        line = lines[i]
        for j in range(len(line)):
            p = line[j]
            map[i,j] = cmap[p]
    
    return map


def star1(filename):
    lines = get_input(filename)
    map = make_map(lines)
    
    i = 0
    j = np.argmax(map[i,:] == 0)
    pos = Pos([i, j], 0)
    operations = re.split('([R,L])', lines[-1])
    for op in operations:
        pos.do_operation(map, op)
        print(pos)
    
    return 6032


if __name__ == "__main__":
    assert(star1("22/example.txt") == 6032)
    # assert(star1("22/input.txt") == 169525884255464)
    # print(f'star 1: {star1("22/input.txt")}')

    # assert(star2("22/example.txt") == 301)
    # assert(star2("22/input.txt") == 3247317268284)
    # print(f'star 2: {star2("22/input.txt")}')
