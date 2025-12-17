from pathlib import Path
from typing import List, Dict


def get_input(filename):
    script_dir = Path(__file__).parent
    lines = []
    with open(script_dir / filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def star1(line):

    # In the output values, how many times do digits `1`, `4`, `7`, or `8` appear?

    pattern, out = line.split("|")
    pattern = pattern.split()
    out = out.split()

    ans = 0
    for s in out:
        n = len(s)
        if n == 2:
            # one
            ans += 1
        elif n == 4:
            # four
            ans += 1
        elif n == 3:
            # seven
            ans += 1
        elif n == 7:
            # eight
            ans += 1
            
    return ans


def aoc(filename):
    lines = get_input(filename)

    ans = 0
    for line in lines:
        ans += star1(line)

    return ans
        

def tests():
    ans = star1("acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf")
    print(f"example: {ans}")
    assert ans == 37, f"wrong answer: {ans}"


if __name__ == "__main__":
    # tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
