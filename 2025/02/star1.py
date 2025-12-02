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
    ranges = lines[0].split(",")

    ans = 0
    for r in ranges:
        start, end = map(int, r.split("-"))
        
        for n in range(start, end + 1):
            # check if number of digits is even
            s = str(n)
            length = len(s)
            if length % 2 != 0:
                continue

            half = length // 2
            l = s[: half]
            r = s[half :]

            if l == r:
                ans += n
                print(n)

    return ans

    


def tests():
    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 1227775554, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
