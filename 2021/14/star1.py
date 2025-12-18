from pathlib import Path
from typing import List, Dict, Any, Tuple
from collections import defaultdict
from functools import cache


def get_input(filename):
    script_dir = Path(__file__).parent
    lines = []
    with open(script_dir / filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


# should probably find a way to cache this
def count_elements(left: str, right: str, iterations: int, count, rules):
    if iterations == 0:
        return
    
    # count[left] += 1
    # count[right] += 1
    
    # add new element
    middle = rules[(left, right)]
    count[middle] += 1

    count_elements(left, middle, iterations-1, count, rules)
    count_elements(middle, right, iterations-1, count, rules)


def parse_input(lines):
    rules = {}
    template = ""
    for line in lines:
        if "\n" in line:
            raise RuntimeError("Malformed input")
        if "->" in line:
            pair, insert = line.split(" -> ")
            rules[(pair[0], pair[1])] = insert
        elif line == "":
            pass
        else:
            template = line

    # count initial elements
    count = defaultdict(int)
    for c in template:
        count[c] += 1

    return rules, template, count


def aoc(filename, steps=10):
    lines = get_input(filename)
    rules, template,count = parse_input(lines)

    for i in range(len(template)-1):
        count_elements(template[i], template[i+1], steps, count, rules)
    
    counts = []
    for key, val in count.items():
        counts.append(val)

    counts.sort()
    return counts[-1] - counts[0]


def tests():
    lines = ["NN", "NN -> C"]
    rules, template, count = parse_input(lines)
    assert template == "NN"
    count_elements("N", "N", 1, count, rules)
    assert count["N"] == 2
    assert count["C"] == 1

    count_elements("N", "N", 1, count, rules)


    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 1588, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")