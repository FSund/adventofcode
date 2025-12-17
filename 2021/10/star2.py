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

CLOSING_CHARS = [")", "]", "}", ">"]

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


def get_closing_chars(line):
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
                raise RuntimeError("This function does not work on corrupt lines")
            
    closing = []
    while chunks:
        c = chunks.pop()
        closing.append(CLOSING_CHARS[TYPE[c]])

    return closing


POINTS_TABLE = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def aoc(filename):
    lines = get_input(filename)

    values = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }
    scores = []
    for line in lines:
        c = get_incorrect_closing_char(line)
        if c:
            # corrupt, skip this
            continue

        closing = get_closing_chars(line)

        score = 0
        for c in closing:
            score *= 5
            score += POINTS_TABLE[c]
        scores.append(score)
    
    scores = sorted(scores)
    return scores[len(scores)//2]


def tests():
    c = get_incorrect_closing_char("{([(<{}[<>[]}>{[]{[(<()>")
    assert c == "}", f"found {c}"

    assert get_closing_chars("[({(<(())[]>[[{[]{<()<>>") == list("}}]])})]")

    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 288957, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")

