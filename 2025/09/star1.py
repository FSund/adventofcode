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

    biggest = 0
    for idx, line1 in enumerate(lines):
        x1, y1 = [int(d) for d in line1.split(",")]
        for line2 in lines[idx:]:
            x2, y2 = [int(d) for d in line2.split(",")]
            if x1 > x2:
                dx = x1 - x2
            else:
                dx = x2 - x1
            if y1 > y2:
                dy = y1 - y2
            else:
                dy = y2 - y1

            area = (dy+1) * (dx+1)
            if area > biggest:
                biggest = area

    return biggest

        

def tests():
    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 50, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
