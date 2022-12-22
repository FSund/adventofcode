import numpy as np
import re
from math import copysign
from enum import Enum

def get_input(filename="input.txt"):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))
    return lines


class NodeType(Enum):
    NONE = -1
    FREE = 0
    WALL = 1

class BorderType(Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2

class MapNode:
    def __init__(self, pos, type=NodeType.NONE):
        self.type = type
        self.pos = pos

        # neighbors
        self.right = None
        self.left = None
        self.up = None
        self.down = None
        self.right_border = BorderType.NONE
        self.left_border = BorderType.NONE
        self.up_border = BorderType.NONE
        self.down_border = BorderType.NONE
    
    def __repr__(self):
        rmap = {
            "0": ">",
            "1": "v",
            "2": "<",
            "3": "^",
        }
        return f"{self.type} [{self.pos[0]}, {self.pos[1]}]"
        
    def remove_none_connections(self, map):
        while self.left.type == NodeType.NONE:
            self.left = self.left.left
        
        while self.right.type == NodeType.NONE:
            self.right = self.right.right
        
        while self.up.type == NodeType.NONE:
            self.up = self.up.up
        
        while self.down.type == NodeType.NONE:
            self.down = self.down.down


class Pos:
    def __init__(self, node: MapNode, rot: int):
        self.node = node
        # 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^)
        self.rot = rot
    
    def __repr__(self):
        rmap = {
            "0": ">",
            "1": "v",
            "2": "<",
            "3": "^",
        }
        return f"[{self.node.pos[0]}, {self.node.pos[1]}] {self.rot}"
    
    def get_password(self):
        # The final password is the sum of 
        # 1000 times the row, 
        # 4 times the column, 
        # and the facing.
        return 1000*(self.node.pos[0]+1) + 4*(self.node.pos[1]+1) + self.rot

    def rotate(self, turn):
        if turn == "R":
            self.rot += 1
        elif turn == "L":
            self.rot -= 1
        else:
            raise RuntimeError

        self.rot = self.rot % 4

    def rotate_border(self, border_type):
        if border_type == BorderType.NONE:
            pass
        elif border_type == BorderType.LEFT:
            self.rotate("L")
        elif border_type == BorderType.RIGHT:
            self.rotate("R")

    def _move_left(self, distance):
        for i in range(distance):
            if self.node.left.type == NodeType.FREE:
                self.rotate_border(self.node.left_border)
                self.node = self.node.left
        
    def _move_right(self, distance):
        for i in range(distance):
            if self.node.right.type == NodeType.FREE:
                self.rotate_border(self.node.right_border)
                self.node = self.node.right
    
    def _move_up(self, distance):
        for i in range(distance):
            if self.node.up.type == NodeType.FREE:
                self.rotate_border(self.node.up_border)
                self.node = self.node.up
    
    def _move_down(self, distance):
        for i in range(distance):
            if self.node.down.type == NodeType.FREE:
                self.rotate_border(self.node.down_border)
                self.node = self.node.down
    
    def move(self, d):
        if self.rot == 0:  # right
            self._move_right(d)
        elif self.rot == 1:  # down
            self._move_down(d)
        elif self.rot == 2:  # left
            self._move_left(d)
        elif self.rot == 3:  # up
            self._move_up(d)
        else:
            raise RuntimeError

    def do_operation(self, operation):
        if operation.isdigit():
            self.move(int(operation))
        else:
            self.rotate(operation)


def make_map_nodes(lines):
    width = 0
    height = 0
    for line in lines:
        if line == "":
            break
        height += 1
        if len(line) > width:
            width = len(line)
    
    cmap = {
        " ": NodeType.NONE,
        ".": NodeType.FREE,
        "#": NodeType.WALL,
    }
    map = []
    for i in range(height):
        line = lines[i]
        map.append([])
        for j in range(width):
            if j >= len(line):
                p = " "
            else:
                p = line[j]
            map[i].append(
                MapNode(
                    pos=(i, j),
                    type=cmap[p]
                )
            )
            
    m = len(map)
    n = len(map[0])
    
    # connect nodes
    for i in range(m):
        for j in range(n):
            current = map[i][j]
            
            if i == 0:  # top row
                current.up = map[m-1][j]
                current.down = map[i+1][j]  # default
            elif i == (m-1):  # bottom row
                current.up = map[i-1][j]  # default
                current.down = map[0][j]
            else:
                current.up = map[i-1][j]
                current.down = map[i+1][j]

            if j == 0:  # leftmost column
                current.left = map[i][n-1]
                current.right = map[i][j+1]  # default
            elif j == (n-1):  # rightmost column
                current.left = map[i][j-1]  # default
                current.right = map[i][0]
            else:
                current.left = map[i][j-1]
                current.right = map[i][j+1]

    # remove NONE
    for i in range(m):
        for j in range(n):
            current = map[i][j]
            current.remove_none_connections(map)
    
    return map


def set_border_types(map):
    m = len(map)
    n = len(map[0])
    


def solve(filename, star2=False):
    lines = get_input(filename)
    map = make_map_nodes(lines)
    
    if star2:
        map = set_border_types(map)
    
    # find start
    current = None
    for j in range(len(map[0])):
        if map[0][j].type != NodeType.NONE:
            current = map[0][j]
            break

    # print(current)
    
    pos = Pos(current, 0)
    operations = re.split('([R,L])', lines[-1])
    for op in operations:
        pos.do_operation(op)
        # print(pos)
        
    # print(pos)
    # print(f"node: {pos.node}")
    
    # print(pos.get_password())
    # print(f"row: {pos.node.pos[0]}")
    # print(f"col: {pos.node.pos[1]}")
    
    return pos.get_password()


if __name__ == "__main__":
    assert(solve("22/example.txt") == 6032)
    assert(solve("22/input.txt") == 1428)
    
    print(solve("22/input.txt"))
    # assert(star1("22/input.txt") == 169525884255464)
    # print(f'star 1: {star1("22/input.txt")}')

    # assert(star2("22/example.txt") == 301)
    # assert(star2("22/input.txt") == 3247317268284)
    # print(f'star 2: {star2("22/input.txt")}')
