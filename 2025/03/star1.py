from pathlib import Path

def get_input(filename):
    script_dir = Path(__file__).parent
    lines = []
    with open(script_dir / filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def make_largest_joltage(line: str) -> int:
    """
    turn on exactly two batteries

    brute force, check for all joltages 99 through 11
    """
    
    n  = len(line)
    for first in range(9, 0, -1):
        print(first)
        first_c = f"{first}"
        for i in range(n):
            if line[i] == first_c:
                for second in range(9, 0, -1):
                    print(second)
                    second_c = f"{second}"
                    for j in range(i+1, n):
                        if line[j] == second_c:
                            return first * 10 + second

    raise RuntimeError("No joltage found")

def aoc(filename):
    lines = get_input(filename)

    ans = 0
    for line in lines:
        ans += make_largest_joltage(line)

    return ans


def tests():
    assert make_largest_joltage("987654321111111") == 98
    assert make_largest_joltage("811111111111119") == 89
    assert make_largest_joltage("234234234234278") == 78
    assert make_largest_joltage("818181911112111") == 92

    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 357, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
