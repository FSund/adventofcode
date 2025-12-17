from pathlib import Path
from typing import List, Dict
from collections import defaultdict


def get_input(filename):
    script_dir = Path(__file__).parent
    lines = []
    with open(script_dir / filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


# OPEN = ["(", "[", "{", "<"]
# CLOSE = [")", "]", "}", ">"]
OPEN = {}
IDX = {
    "(": 0,
    ")": 1,
    "[": 2,
    "]": 3,
    "{": 4,
    "}": 5,
    "<": 6,
    ">": 7,
}
TYPE = {
    "(": 0,
    ")": 0,
    "[": 1,
    "]": 1,
    "{": 2,
    "}": 2,
    "<": 3,
    ">": 3,
}

OPEN = {
    "(": 0,
    # ")": 0,
    "[": 1,
    # "]": 1,
    "{": 2,
    # "}": 2,
    "<": 3,
    # ">": 3,
}

CLOSE = {
    # "(": 0,
    ")": 0,
    # "[": 1,
    "]": 1,
    # "{": 2,
    "}": 2,
    # "<": 3,
    ">": 3,
}


# def get_incorrect_closing_char(line):
#     current_open_chunks = [0, 0, 0, 0]
#     index = {
#         "(": 0,
#         ")": 0,
#         "{": 1,
#         "}": 1,
#         "[": 2,
#         "]": 2,
#         "<": 3,
#         ">": 3,
#     }
#     operation = {
#         "(": 1,
#         ")": -1,
#         "{": 1,
#         "}": -1,
#         "[": 1,
#         "]": -1,
#         "<": 1,
#         ">": -1,
#     }
#     for c in line:
#         idx = index[c]
#         op = operation[c]
#         current_open_chunks[idx] += op
#         if current_open_chunks[idx] < 0:
#             return c

#     return None


def get_incorrect_closing_char(line):
    chunks = []
    for c in line:
        if c in OPEN:  # open
            chunks.append(c)
        else:  # c in CLOSE
            if TYPE[chunks[-1]] == TYPE[c]:
                # close the last chunk (pop it)
                chunks.pop()
            else:
                # corrupted
                return c


def aoc(filename):
    lines = get_input(filename)

    values = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }
    ans = 0
    for line in lines:
        c = get_incorrect_closing_char(line)
        if c:
            ans += values[c]

    return ans
        

def tests():
    c = get_incorrect_closing_char("{([(<{}[<>[]}>{[]{[(<()>")
    assert c == "}", f"found {c}"

    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 26397, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
