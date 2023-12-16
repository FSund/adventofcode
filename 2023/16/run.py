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

def count_energized(_energized):
    count = 0
    if len(_energized.shape) == 3:
        energized = np.sum(_energized, axis=2)
    else:
        energized = _energized
    for i in range(len(energized)):
        for j in range(len(energized[0])):
            if energized[i, j] > 0:
                count += 1
    return count

def print_energized_map(_energized):
    if len(_energized.shape) == 3:
        energized = np.sum(_energized, axis=2)
    else:
        energized = _energized
    for i in range(energized.shape[0]):
        for j in range(energized.shape[1]):
            if energized[i, j] > 0:
                print("#", end="")
            else:
                print(".", end="")
        print()

def move_beams(energized, beams, lines):
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
        if beam.vel[0] == 0 and beam.vel[1] == 1:  # down
            if energized[i, j, 0]:
                beams.remove(beam)
                continue
        elif beam.vel[0] == 0 and beam.vel[1] == -1:  # up
            if energized[i, j, 1]:
                beams.remove(beam)
                continue
        elif beam.vel[0] == 1 and beam.vel[1] == 0:  # right
            if energized[i, j, 2]:
                beams.remove(beam)
                continue
        elif beam.vel[0] == -1 and beam.vel[1] == 0:  # left
            if energized[i, j, 3]:
                beams.remove(beam)
                continue
        
        # one bool per direction
        if beam.vel[0] == 0 and beam.vel[1] == 1:  # down
            energized[i,j,0] = 1
        elif beam.vel[0] == 0 and beam.vel[1] == -1:  # up
            energized[i,j,1] = 1
        elif beam.vel[0] == 1 and beam.vel[1] == 0:  # right
            energized[i,j,2] = 1
        elif beam.vel[0] == -1 and beam.vel[1] == 0:  # left
            energized[i,j,3] = 1
        
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
            
    return energized

def run_calc(lines, initial_beam):
    # lines = get_input(filename)
    # energized = [[0]*len(lines)]*len(lines[0])
    # energized = np.zeros((len(lines), len(lines[0])), dtype=bool)
    
    # one bool per direction
    energized = np.zeros((len(lines), len(lines[0]), 4), dtype=int)
    
    # if not initial_beam:
    #     #               pos,   dir
    #     beams = [Beam([0,-1], [0,1])]
    # else:
    beams = [initial_beam]
    
    # initial conditions
    # for beam in beams:
    #     energized[beam.pos[0], beam.pos[1]] += 1

    iterations = 0
    while True:
        if len(beams) == 0:
            break
        iterations += 1
        if iterations % 10 == 0:
            # print(f"iteration {iterations}, beams {len(beams)}")
            # print(energized)
            pass
        energized2 = move_beams(np.copy(energized), beams, lines)
        if np.all(energized == energized2):
            # print("loop detected, stopping")
            break
        else:
            energized = energized2
        # if energized.shape[0] > 10:
        #     print_energized_map(energized[:10,:10])
        # else:
        #     print_energized_map(energized)

    # if energized.shape[0] > 10:
    #     print_energized_map(energized[:10,:10])
    # else:
    #     print_energized_map(energized)
    return count_energized(energized)

def star1(filename):
    lines = get_input(filename)
    initial_beam = Beam([0,-1], [0,1])
    return run_calc(lines, initial_beam)

def star2(filename):
    lines = get_input(filename)
    
    max_energized = 0

    # left edge
    for i in range(len(lines)):
        initial_beam = Beam([i,-1], [0,1])
        n = run_calc(lines, initial_beam)
        if n > max_energized:
            max_energized = n
    
    # right edge
    for i in range(len(lines)):
        initial_beam = Beam([i, len(lines[0])], [0,-1])
        n = run_calc(lines, initial_beam)
        if n > max_energized:
            max_energized = n
    
    # top edge
    for j in range(len(lines[0])):
        initial_beam = Beam([-1, j], [1,0])
        n = run_calc(lines, initial_beam)
        if n > max_energized:
            max_energized = n
            
    # bottom edge
    for j in range(len(lines[0])):
        initial_beam = Beam([len(lines), j], [-1,0])
        n = run_calc(lines, initial_beam)
        if n > max_energized:
            max_energized = n
    
    # # top left corner
    # initial_beam = Beam([0,0], [1,0])
    # n = run_calc(lines, initial_beam)
    # if n > max_energized:
    #     max_energized = n
    # initial_beam = Beam([0,0], [0,1])
    # n = run_calc(lines, initial_beam)
    # if n > max_energized:
    #     max_energized = n
        
    # # top right corner
    # initial_beam = Beam([0,len(lines[0])-1], [1,0])
    # n = run_calc(lines, initial_beam)
    # if n > max_energized:
    #     max_energized = n
    # initial_beam = Beam([0,len(lines[0])-1], [0,-1]) 
    # n = run_calc(lines, initial_beam)
    # if n > max_energized:
    #     max_energized = n
    
    # # bottom left corner
    # initial_beam = Beam([len(lines)-1,0], [-1,0])
    # n = run_calc(lines, initial_beam)
    # if n > max_energized:
    #     max_energized = n
    # initial_beam = Beam([len(lines)-1,0], [0,1])
    # n = run_calc(lines, initial_beam)
    # if n > max_energized:
    #     max_energized = n
    
    # # bottom right corner
    # initial_beam = Beam([len(lines)-1,len(lines[0])-1], [-1,0])
    # n = run_calc(lines, initial_beam)
    # if n > max_energized:
    #     max_energized = n
    # initial_beam = Beam([len(lines)-1,len(lines[0])-1], [0,-1])
    # n = run_calc(lines, initial_beam)
    # if n > max_energized:
    #     max_energized = n
    
    return max_energized
    
    
    

def tests():
    pass

if __name__ == "__main__":
    tests()

    ans = star1("example.txt")
    print(f"example star 1: {ans}")
    assert ans == 46, f"wrong answer: {ans}"
    
    ans = star1("input.txt")
    print(f"star 1: {ans}")
    
    ans = star2("example.txt")
    print(f"example star 2: {ans}")
    assert ans == 51
    
    ans = star2("input.txt")
    print(f"star 2: {ans}")
    # # assert example == 145
    
    # 7792 too low
    