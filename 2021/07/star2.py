from pathlib import Path
from math import factorial


def get_input(filename):
    script_dir = Path(__file__).parent
    lines = []
    with open(script_dir / filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def aoc(filename):
    lines = get_input(filename)

    crabs = [int(d) for d in lines[0].split(",")]
    m = max(crabs)

    ans = 9999999999999999
    for target in range(m):
        cost = 0
        for crab in crabs:
            diff = abs(crab - target)
            cost += sum([i for i in range(1, diff + 1)])
        if cost < ans:
            ans = cost
    
    return ans


def tests():
    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 168, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
