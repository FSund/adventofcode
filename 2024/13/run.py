import math
from math import lcm, gcd
import numpy as np
from scipy.optimize import linprog
import numpy.typing as npt


def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


class Robot:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel

    @staticmethod
    def from_string(s):
        pos, vel = s.split(" ")
        pos = [int(x) for x in pos.split("=")[1].split(",")]
        vel = tuple(int(x) for x in vel.split("=")[1].split(","))
        return Robot(pos, vel)

    def move(self, n_steps, map_size):
        self.pos[0] = (self.pos[0] + self.vel[0] * n_steps) % map_size[0]
        self.pos[1] = (self.pos[1] + self.vel[1] * n_steps) % map_size[1]

    def __repr__(self):
        return f"Robot({self.pos}, {self.vel})"


def aoc(filename, star2=False):
    lines = get_input(filename)
    robots = [Robot.from_string(line) for line in lines]
    if filename == "example.txt":
        map_size = (11, 7)
    else:
        map_size = (101, 103)
    
    for robot in robots:
        robot.move(100, map_size)
    
    quadrants = [
        [0, 0], 
        [0, 0]
    ]
    for robot in robots:
        print(robot)
        if robot.pos[0] == int((map_size[0] - 1)//2):
            continue
        elif robot.pos[1] == int((map_size[1] - 1)//2):
            continue
        else:
            i = 0 if robot.pos[0] < map_size[0]/2 else 1
            j = 0 if robot.pos[1] < map_size[1]/2 else 1
            quadrants[i][j] += 1
        
    return quadrants[0][0]*quadrants[0][1]*quadrants[1][0]*quadrants[1][1]


def tests():
    ans = aoc("example.txt")
    print(f"example star 1: {ans}")
    assert ans == 12, f"wrong answer: {ans}"
    
    # ans = aoc("example.txt", star2=True)
    # print(f"example star 2: {ans}")
    # assert ans == 1206, f"wrong answer: {ans}"

if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"star 1: {ans}")
    assert ans > 228153786
    
    # ans = aoc("input.txt", star2=True)
    # print(f"star 2: {ans}")
    # 71922170897884 too low
    # assert ans == 1344
