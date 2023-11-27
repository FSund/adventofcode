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

class BorderAction(Enum):
    NONE = 0
    LEFT = -1
    RIGHT = 1
    FLIP = 2  # rotate 180 degrees

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

class MapNode:
    def __init__(self, pos, aoc_pos, type=NodeType.NONE):
        self.type = type
        self.pos = pos  # position on 50x50 grid
        self.aoc_pos = aoc_pos  # position on input grid (used to get result)

        # neighbors
        self.neighbors = [None]*4
        self.neighbor_transforms = [BorderAction.NONE]*4
        
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
        if border_type == BorderAction.NONE:
            pass
        elif border_type == BorderAction.LEFT:
            self.rotate("L")
        elif border_type == BorderAction.RIGHT:
            self.rotate("R")
        elif border_type == BorderAction.FLIP:
            # yes
            self.rotate("R")
            self.rotate("R")

    def _move_left(self, distance):
        for i in range(distance):
            if self.node.left.type == NodeType.FREE:
                self.rotate_border(self.node.left_border_action)
                self.node = self.node.left
        
    def _move_right(self, distance):
        for i in range(distance):
            if self.node.right.type == NodeType.FREE:
                self.rotate_border(self.node.right_border_action)
                self.node = self.node.right
    
    def _move_up(self, distance):
        for i in range(distance):
            if self.node.up.type == NodeType.FREE:
                self.rotate_border(self.node.up_border_action)
                self.node = self.node.up
    
    def _move_down(self, distance):
        for i in range(distance):
            if self.node.down.type == NodeType.FREE:
                self.rotate_border(self.node.down_border_action)
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


# class CubeFace:
#     def __init__(self, id):
#         self.id = 1
#         self.transforms = []


def parse_input(lines, example=False):
    if example:
        n = 4
        face_coords = [
            [0, 8],
            [4, 0], [4, 4], [4, 8],
            [8, 8], [8, 12],
        ]
    else:
        n = 50
        # positions of upper left corner of each face, in the input
        face_coords = [
            [0, 50], [0, 100],
            [50, 50],
            [100, 0], [100, 50],
            [150, 0],
        ]
    
    # parse input into 6 lists, each containing the map nodes of each face
    faces = [[] for i in range(6)]
    cmap = {
        " ": NodeType.NONE,
        ".": NodeType.FREE,
        "#": NodeType.WALL,
    }
    for face in range(6):
        i0 = face_coords[face][0]
        j0 = face_coords[face][1]
        for i in range(n):
            faces[face].append([])
            line = lines[i0 + i]
            for j in range(n):
                p = line[j0 + j]
                faces[face][i].append(
                    MapNode(
                        pos=(i, j),
                        aoc_pos=(i0+i, j0+j),
                        type=cmap[p]
                    )
                )

    def transform_from_string(transform_string):
        if transform_string == "x": # 0 is not possible
            return BorderAction.NONE
        elif transform_string == "N":  # no rotation
            return BorderAction.NONE
        elif transform_string == "L":
            return BorderAction.LEFT
        elif transform_string == "R":
            return BorderAction.RIGHT
        elif transform_string == "F":
            return BorderAction.FLIP

    # set up border connections
    if example:
        # left[n-1] returns face to the left of face n
        right = [6, 3, 4, 6, 6, 1]
        down = [4, 5, 5, 5, 2, 2]
        left = [3, 6, 2, 3, 3, 5]
        up = [2, 1, 1, 1, 4, 4]
        
        # usage: face_neighbors[LEFT][n-1] returns face to the left of face n
        face_neighbors = [None]*4
        face_neighbors[RIGHT] = right
        face_neighbors[DOWN] = down
        face_neighbors[LEFT] = left
        face_neighbors[UP] = up
        
        # usage: transforms[from_face][to_face]
        transform_strings = [
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
    else:
        raise RuntimeError
        
    # 0-index
    for dir in [RIGHT, DOWN, LEFT, UP]:
        for i in range(6):
            face_neighbors[dir][i] -= 1

    # convert using enum
    transforms = []
    for from_face in range(6):
        transforms.append([])
        for to_face in range(6):
            transforms[from_face].append(transform_from_string(transform_strings[from_face][to_face]))

    def get_neighbor(pos, from_face, to_face, translation):
        # first find position `pos` on to_face
        transform = transforms[from_face][to_face]
        if transform == BorderAction.NONE:
            ii = pos[0] + n
            jj = pos[1] + n
        elif transform == BorderAction.FLIP:
            ii = pos[0]
            jj = pos[1]
        elif transform == BorderAction.LEFT:
            pass
        elif transform == BorderAction.RIGHT:
            pass

        # then translate and wrap around
        ii = (ii + translation[0]) % n
        jj = (jj + translation[1]) % n
        return faces[to_face][ii][]
        

    for idx in range(6):
        from_face = idx

        # left/right borders
        for i in range(n):
            j = 0  # left
            to_face = face_neighbors[LEFT][from_face]
            
            faces[idx][i][j].neighbors[LEFT] = face_neighbors[LEFT][idx]

            j = n-1  # right
            faces[idx][i][j].neighbors[RIGHT] = face_neighbors[RIGHT][idx]
            
        # up/down
        for j in range(n):
            i = 0  # up
            faces[idx][i][j].neighbors[UP] = face_neighbors[UP][idx]
            i = n-1  # down
            faces[idx][i][j].neighbors[DOWN] = face_neighbors[DOWN][idx]
        
            
                
        
        

    return faces

def testing():
    lines = get_input("22/example.txt")
    faces = parse_input(lines, example=True)
    print(faces[0][0][0].neighbors[LEFT])
    print(faces[0][0][0].neighbors[LEFT])
    print(faces[0][0][0].neighbors[LEFT])
    print(faces[0][0][0].neighbors[LEFT])

    return 0

if __name__ == "__main__":
    testing()

    # assert(solve("22/example.txt") == 6032)
    # assert(solve("22/input.txt") == 1428)
    
    # assert(_get_face_number_example(0, 8) == 1)
    # assert(_get_face_number_example(4, 0) == 2)
    # assert(_get_face_number_example(4, 4) == 3)
    # assert(_get_face_number_example(4, 8) == 4)
    # assert(_get_face_number_example(8, 8) == 5)
    # assert(_get_face_number_example(8, 12) == 6)
    
    # assert(_get_face_number(0, 50) == 1)
    # assert(_get_face_number(0, 100) == 2)
    # assert(_get_face_number(50, 50) == 3)
    # assert(_get_face_number(100, 0) == 4)
    # assert(_get_face_number(100, 50) == 5)
    # assert(_get_face_number(150, 0) == 6)
    
    # assert(get_border_rotation(from_face=1, to_face=1) == BorderAction.NONE)
    # assert(get_border_rotation(from_face=1, to_face=2) == BorderAction.NONE)
    # assert(get_border_rotation(from_face=1, to_face=3) == BorderAction.NONE)
    # assert(get_border_rotation(from_face=1, to_face=4) == BorderAction.FLIP)
    
    # assert(solve("22/example.txt", star2=True) == 5031)
    
    # print(f'star 1: {solve("22/input.txt")}')
    # print(f'star 2: {solve("22/input.txt", star2=True)}')
