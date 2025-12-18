from pathlib import Path
from typing import List, Dict, Any, Tuple
from collections import defaultdict
from functools import cache
from typing import Hashable


def get_input(filename):
    script_dir = Path(__file__).parent
    lines = []
    with open(script_dir / filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def star2(rules, template, count, steps):
    
    @cache
    def count_elements(left: str, right: str, iterations: int) -> Dict[str, int]:
        if iterations == 0:
            return {}
        
        # add new element
        middle = rules[(left, right)]

        c1 = count_elements(left, middle, iterations-1)
        c2 = count_elements(middle, right, iterations-1)

        count = defaultdict(int)
        count[middle] = 1
        for key, val in c1.items():
            count[key] += val
        for key, val in c2.items():
            count[key] += val

        return count

    for i in range(len(template)-1):
        elements = count_elements(template[i], template[i+1], steps)
        for key, val in elements.items():
            count[key] += val

    return count


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


def aoc(filename, steps=40):
    lines = get_input(filename)
    rules, template, count = parse_input(lines)

    count = star2(rules, template, count, steps)
    
    counts = []
    for key, val in count.items():
        counts.append(val)

    counts.sort()
    return counts[-1] - counts[0]


def tests():
    lines = ["NN", "NN -> C"]
    rules, template, count = parse_input(lines)
    assert template == "NN"
    star2(rules, template, count, steps=1)
    assert count["N"] == 2
    assert count["C"] == 1

    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 2188189693529, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")