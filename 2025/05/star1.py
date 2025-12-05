from pathlib import Path

def get_input(filename):
    script_dir = Path(__file__).parent
    lines = []
    with open(script_dir / filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def aoc(filename):
    lines = get_input(filename)

    ranges = []
    ingredients = []
    for line in lines:
        if "-" in line:
            ranges.append([int(d) for d in line.split("-")])
        elif len(line):
            ingredients.append(int(line))
    
    fresh = 0
    for ing in ingredients:
        for lower, upper in ranges:
            if ing >= lower and ing <= upper:
                fresh += 1
                break

    return fresh


def tests():
    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 3, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
