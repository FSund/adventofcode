from dataclasses import dataclass
from functools import cache
import numpy as np
from datetime import datetime
from pathlib import Path
from collections import OrderedDict
import heapq
from collections import deque

def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines

def star1(filename):
    lines = get_input(filename)
    left = []
    right = []
    for line in lines:
        l, r = line.split("   ")
        left.append(l)
        right.append(r)
    
    left.sort()
    right.sort()
    diff = 0
    for l, r in zip(left, right):
        diff += abs(int(l) - int(r))
    
    return diff


def star2(filename):
    lines = get_input(filename)
    left = []
    right = []
    for line in lines:
        l, r = line.split("   ")
        left.append(int(l))
        right.append(int(r))
    
    left.sort()
    right.sort()
    right = np.array(right)
    sum = 0
    for l in left:
        # find the number of times each number in the left list
        # appears in the right list
        sum += np.sum(right == l) * l
    
    return sum


def tests():
    ans = star1("example.txt")
    print(f"example star 1: {ans}")
    assert ans == 11, f"wrong answer: {ans}"
    
    ans = star2("example.txt")
    print(f"example star 2: {ans}")
    assert ans == 31, f"wrong answer: {ans}"

if __name__ == "__main__":
    tests()
    
    ans = star1("input.txt")
    print(f"star 1: {ans}")

    ans = star2("input.txt")
    print(f"star 2: {ans}")