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
    assert vx > 0
    while True:
        x += vx
        y += vy
        vx = max(0, vx - 1)
        vy -= 1

        if x1 <= x <= x2 and y1 <= y <= y2:
            return True
        if y < y1 and vy <= 0:
            return False
        if x > x2:
            return False

def probe_x(vx, x1, x2):
    x = 0
    assert vx > 0
    while True:
        x += vx
        vx = max(0, vx - 1)

        if x1 <= x <= x2:
            return True
        if x > x2:
            return False
        
        if vx == 0:
            return False


def aoc(filename):
    lines = get_input(filename)
    left, right = lines[0].split(", ")
    left = left.strip("target area: x=")
    right = right.strip("y=")
    x1, x2 = [int(x) for x in left.split("..")]
    y1, y2 = [int(y) for y in right.split("..")]

    ans = 0
    for vx in range(1, 2000):
        # skip x values that can't lead to valid solution
        if not probe_x(vx, x1, x2):
            continue
        for vy in range(-2000, 2000):
            success = send_probe(vx, vy, x1, x2, y1, y2)
            if success:
                # print(f"{vx = }, {vy = }")
                ans += 1

    return ans


def tests():
    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 112, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")