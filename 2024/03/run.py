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


def starts_with_mul(substring):
    if len(substring) >= 4:
        if substring[:4] == "mul(":
            return True

    return False


def get_numbers_until_next_rparen(substring):
    maybe_number_pair,_, right = substring.partition(")")
    if len(maybe_number_pair) <= 7 and len(maybe_number_pair) >= 3:  # max 3 digits per number, plus comma
        if "," in maybe_number_pair:
            left, right = maybe_number_pair.split(",")
            if left.isdigit() and right.isdigit():
                return int(left), int(right)

    return None


def get_product(substring):
    result = get_numbers_until_next_rparen(substring)
    if result:
        return result[0]*result[1]
    else:
        return 0


def star1(filename):
    lines = get_input(filename)
    total = 0
    for line in lines:
        for i in range(len(line)):
            if starts_with_mul(line[i:]):
                total += get_product(line[i+4:])

    return total


def tests():
    assert starts_with_mul("mul(")
    assert not starts_with_mul("mul")
    
    assert get_numbers_until_next_rparen("") is None
    assert get_numbers_until_next_rparen(")") is None
    assert get_numbers_until_next_rparen(",)") is None
    assert get_numbers_until_next_rparen("1,1)") == (1,1)
    assert get_numbers_until_next_rparen("123,123)") == (123,123)
    
    ans = star1("example.txt")
    print(f"example star 1: {ans}")
    assert ans == 161, f"wrong answer: {ans}"
    
    # ans = star2("example.txt")
    # print(f"example star 2: {ans}")
    # assert ans == 4, f"wrong answer: {ans}"

if __name__ == "__main__":
    tests()
    
    ans = star1("input.txt")
    print(f"star 1: {ans}")

    # ans = star2("input.txt")
    # print(f"star 2: {ans}")