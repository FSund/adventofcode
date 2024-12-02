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


def is_safe(levels):
    decreasing = 0
    increasing = 0
    for i in range(len(levels) - 1):
        diff = abs(levels[i] - levels[i+1])
        if levels[i] == levels[i+1]:
            pass
        elif diff <= 3:
            if levels[i] > levels[i+1]:
                decreasing += 1
            elif levels[i] < levels[i+1]:
                increasing += 1
    if increasing == 0 and decreasing == len(levels) - 1:
        return True
    elif decreasing == 0 and increasing == len(levels) - 1:
        return True
    
    return False


def star1(filename):
    lines = get_input(filename)
    count = 0
    for line in lines:
        levels = [int(level) for level in line.split(" ")]
        count += is_safe(levels)
        
    return count


def star2(filename):
    lines = get_input(filename)
    count = 0
    for line in lines:
        levels = [int(level) for level in line.split(" ")]
        can_be_safe = 0
        n = len(levels)
        for i in range(n):
            levels = [int(level) for level in line.split(" ")]
            levels.pop(i)
            can_be_safe += is_safe(levels)
        
        if can_be_safe:
            count += 1
        
    return count


def tests():
    ans = star1("example.txt")
    print(f"example star 1: {ans}")
    assert ans == 2, f"wrong answer: {ans}"
    
    ans = star2("example.txt")
    print(f"example star 2: {ans}")
    assert ans == 4, f"wrong answer: {ans}"

if __name__ == "__main__":
    tests()
    
    ans = star1("input.txt")
    print(f"star 1: {ans}")

    ans = star2("input.txt")
    print(f"star 2: {ans}")