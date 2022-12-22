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
    FLIP = 3  # rotate 180 degrees

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

class MapNode:
    def __init__(self, pos, type=NodeType.NONE):
        self.type = type
        self.pos = pos

        # neighbors
        self.right = None
        self.left = None
        self.up = None
        self.down = None
        
        # border rotations
        self.right_border = BorderType.NONE
        self.left_border = BorderType.NONE
        self.up_border = BorderType.NONE
        self.down_border = BorderType.NONE
    
    def __repr__(self):
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
        elif border_type == BorderType.FLIP:
            # yes
            self.rotate("R")
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


def _get_face_number_example(i, j):
    cube_row = i//4
    cube_col = j//4
    
    if cube_row == 0:
        if cube_col == 2:
            return 1
    elif cube_row == 1:
        if cube_col == 0:
            return 2
        elif cube_col == 1:
            return 3
        elif cube_col == 2:
            return 4
    elif cube_row == 2:
        if cube_col == 2:
            return 5
        elif cube_col == 3:
            return 6

    raise RuntimeError


def _get_face_number(i, j):
    cube_row = i//50
    cube_col = j//50
    
    if cube_row == 0:
        if cube_col == 1:
            return 1
        elif cube_col == 2:
            return 2
    elif cube_row == 1:
        if cube_col == 1:
            return 3
    elif cube_row == 2:
        if cube_col == 0:
            return 4
        elif cube_col == 1:
            return 5
    elif cube_row == 3:
        if cube_col == 0:
            return 6

    raise RuntimeError


def get_face_number(i, j, example=False):
    if example:
        return _get_face_number_example(i, j)
    else:
        return _get_face_number(i, j)


def get_border_rotation(from_face, to_face, example=False):
    border_map_example = [
        # from_face == row
        # to_face == col
        # 1    2    3    4    5    6 
        ["N", "F", "L", "N", "x", "F",],  # from face 1
        ["F", "N", "N", "x", "F", "R",],  # from face 2
        ["R", "N", "N", "N", "L", "x",],  # from face 3
        ["N", "x", "N", "N", "N", "R",],  # from face 4
        ["x", "F", "R", "N", "N", "N",],  # from face 5
        ["F", "L", "x", "L", "N", "N",],  # from face 6
    ]
    
    border_map_real = [
        # from_face == row
        # to_face == col
        # 1    2    3    4    5    6 
        ["N", "N", "N", "F", "x", "R",],  # from face 1
        ["N", "N", "R", "x", "F", "N",],  # from face 2
        ["N", "L", "N", "L", "N", "x",],  # from face 3
        ["F", "x", "R", "N", "N", "N",],  # from face 4
        ["x", "F", "N", "N", "N", "R",],  # from face 5
        ["L", "N", "x", "N", "L", "N",],  # from face 6
    ]
    
    if example:
        border_map = border_map_example
    else:
        border_map = border_map_real
    
    rot = border_map[from_face-1][to_face-1]
    if rot == "x": # 0 is not possible
        return BorderType.NONE
    elif rot == "N":  # no rotation
        return BorderType.NONE
    elif rot == "L":
        return BorderType.LEFT
    elif rot == "R":
        return BorderType.RIGHT
    elif rot == "F":
        return BorderType.FLIP


def set_border_rotations(map, example=False):
    #         1111
    #         1111
    #         1111
    #         1111
    # 222233334444
    # 222233334444
    # 222233334444
    # 222233334444
    #         55556666
    #         55556666
    #         55556666
    #         55556666
    m = len(map)
    n = len(map[0])
    
    for i in range(m):
        for j in range(n):
            node = map[i][j]
            # skip unreachable nodes
            if node.type != NodeType.NONE:
                from_face = get_face_number(i, j, example=example)
                
                # right
                other = node.right
                to_face = get_face_number(other.pos[0], other.pos[1], example=example)
                node.right_border = get_border_rotation(from_face, to_face, example)
                
                # down
                other = node.down
                to_face = get_face_number(other.pos[0], other.pos[1], example=example)
                node.down_border = get_border_rotation(from_face, to_face, example)
                
                # left
                other = node.left
                to_face = get_face_number(other.pos[0], other.pos[1], example=example)
                node.left_border = get_border_rotation(from_face, to_face, example)
                
                # up
                other = node.up
                to_face = get_face_number(other.pos[0], other.pos[1], example=example)
                node.up_border = get_border_rotation(from_face, to_face, example)

    return map


def fix_star2_connections(map):
    m = len(map)
    n = len(map[0])
    # TODO
    pass


def solve(filename, star2=False):
    lines = get_input(filename)
    map = make_map_nodes(lines)
    
    if star2:
        map = set_border_rotations(map, True if "example" in filename else False)

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
        print(pos)
        
    print(pos)
    print(f"node: {pos.node}")
    
    print(pos.get_password())
    print(f"row: {pos.node.pos[0]}")
    print(f"col: {pos.node.pos[1]}")
    
    return pos.get_password()


def testing():
    lines = get_input("22/example.txt")
    map = make_map_nodes(lines)
    map = set_border_rotations(map, example=True)
    
    node = map[5][11]
    pos = Pos(node, rot=RIGHT)
    print(_get_face_number_example(pos.node.pos[0], pos.node.pos[1]))
    print(pos)
    
    pos.do_operation("1")
    print(pos)
    
    print(_get_face_number_example(pos.node.pos[0], pos.node.pos[1]))


if __name__ == "__main__":
    
    testing()

    # assert(solve("22/example.txt") == 6032)
    # assert(solve("22/input.txt") == 1428)
    
    assert(_get_face_number_example(0, 8) == 1)
    assert(_get_face_number_example(4, 0) == 2)
    assert(_get_face_number_example(4, 4) == 3)
    assert(_get_face_number_example(4, 8) == 4)
    assert(_get_face_number_example(8, 8) == 5)
    assert(_get_face_number_example(8, 12) == 6)
    
    assert(_get_face_number(0, 50) == 1)
    assert(_get_face_number(0, 100) == 2)
    assert(_get_face_number(50, 50) == 3)
    assert(_get_face_number(100, 0) == 4)
    assert(_get_face_number(100, 50) == 5)
    assert(_get_face_number(150, 0) == 6)
    
    assert(get_border_rotation(from_face=1, to_face=1) == BorderType.NONE)
    assert(get_border_rotation(from_face=1, to_face=2) == BorderType.NONE)
    assert(get_border_rotation(from_face=1, to_face=3) == BorderType.NONE)
    assert(get_border_rotation(from_face=1, to_face=4) == BorderType.FLIP)
    
    # assert(solve("22/example.txt", star2=True) == 5031)
    
    # print(f'star 1: {solve("22/input.txt")}')
    # print(f'star 2: {solve("22/input.txt", star2=True)}')
