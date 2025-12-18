from pathlib import Path


def get_input(filename):
    script_dir = Path(__file__).parent
    lines = []
    with open(script_dir / filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def send_probe(vx, vy, x1, x2, y1, y2):
    x = 0
    y = 0
    max_y = -9000000
    assert vx > 0
    while True:        
        x += vx
        y += vy
        vx = max(0, vx - 1)
        vy -= 1

        if y > max_y:
            max_y = y
        
        if x1 <= x <= x2 and y1 <= y <= y2:
            return max_y
        if y < y2 and vy < 0:
            return None
        if x > x2:
            return None


def aoc(filename):
    lines = get_input(filename)
    left, right = lines[0].split(", ")
    left = left.strip("target area: x=")
    right = right.strip("y=")
    x1, x2 = [int(x) for x in left.split("..")]
    y1, y2 = [int(y) for y in right.split("..")]

    max_max_y = -999999
    for vx in range(1, 100):
        for vy in range(-100, 100):
            max_y = send_probe(vx, vy, x1, x2, y1, y2)
            if max_y is not None:
                print(f"{vx = }, {vy = }, {max_y = }")
                if max_y > max_max_y:
                    max_max_y = max_y

    print(f"{max_max_y = }")
    return max_max_y


def tests():
    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 45, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")