from dataclasses import dataclass
from functools import cache
import numpy as np
from datetime import datetime
from pathlib import Path
from collections import OrderedDict

def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))
    # return as_np(lines)
    return lines

@dataclass
class Beam:
    pos: list[int]
    vel: list[int]

def count_energized(energized):
    count = 0
    for i in range(len(energized)):
        for j in range(len(energized[0])):
            if energized[i, j] > 0:
                count += 1
    return count

def print_energized_map(energized):
    for i in range(energized.shape[0]):
        for j in range(energized.shape[1]):
            if energized[i, j] > 0:
                print("#", end="")
            else:
                print(".", end="")
        print()

@cache
def move_beams(beams, lines):
    n = len(beams)
    for idx in range(n)[::-1]: # reverse order to not loop through new beams
        beam = beams[idx]

        beam.pos[0] += beam.vel[0]
        beam.pos[1] += beam.vel[1]
        if beam.pos[0] < 0 or beam.pos[1] < 0 or beam.pos[0] >= len(lines) or beam.pos[1] >= len(lines[0]):
            # print(f"removing beam at {beam.pos}")
            beams.remove(beam)
            continue

        i = beam.pos[0]
        j = beam.pos[1]
        energized[i,j] += 1
        
        if lines[i][j] == ".":
            continue
        elif lines[i][j] == "\\":
            beam.vel = [beam.vel[1], beam.vel[0]]
        elif lines[i][j] == "/":
            beam.vel = [-beam.vel[1], -beam.vel[0]]
        elif lines[i][j] == "|":
            # split if going left or right
            # print(f"splitting beam at | at {beam.pos}")
            if beam.vel[0] == 0:
                # beams.append(Beam([i,j], [1,0]))
                beam.vel = [1,0] # down
                beams.append(Beam([i,j], [-1,0])) # up
            else:
                # do nothing if going left or right
                pass
        elif lines[i][j] == "-":
            # split if going up or down
            # print(f"splitting beam at - at {beam.pos}")
            if beam.vel[1] == 0:
                # beams.append(Beam([i,j], [0,1]))
                beam.vel = [0,1] # right 
                beams.append(Beam([i,j], [0,-1])) # left
            else:
                # do nothing if going up or down
                pass

def star1(filename):
    lines = get_input(filename)
    # energized = [[0]*len(lines)]*len(lines[0])
    energized = np.zeros((len(lines), len(lines[0])), dtype=int)
    #         pos,   dir
    beams = [Beam([0,0], [0,1])]
    for beam in beams:
        energized[beam.pos[0], beam.pos[1]] += 1

    iterations = 0
    while True:
        if len(beams) == 0:
            break
        iterations += 1
        if iterations % 100 == 0:
            print(f"iteration {iterations}, beams {len(beams)}")
        move_beams(beams, lines)

    # print([en for en in energized])
    print_energized_map(energized)
    return count_energized(energized)

def tests():
    pass

if __name__ == "__main__":
    tests()

    example = star1("example.txt")
    print(f"example star 1: {example}")
    # assert example == 1320
    
    # example = star1("input.txt")
    # print(f"star 1: {example}")
    
    # example = star2("example.txt")
    # print(f"example star 2: {example}")
    # assert example == 145
    
    # example = star2("input.txt")
    # print(f"star 2: {example}")
    # # assert example == 145
    
    