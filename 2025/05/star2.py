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
    
    ranges = sorted(ranges)  # sorts by first element    
    print(ranges)
    n = len(ranges)
    modified = True
    while modified:
        modified = False
        for i in range(n):
            lower = ranges[i][0]
            upper = ranges[i][1]
            for j in range(i+1, n):  # sorted list, so will be all ranges larger than start of ranges[i]
                # if start of second range inside first range
                # and end of second range outside first range
                # extend first range
                if lower <= ranges[j][0] <= upper and ranges[j][1] > upper:
                    # extend first range to end of second range
                    ranges[i][1] = ranges[j][1]
                    modified = True

                    # then delete second range (is contained in first range now)
                    ranges[j][0] = 0
                    ranges[j][1] = 0
                    # print(f"Deleted range {j}")

                # if fully contained within, just delete it
                elif lower <= ranges[j][0] <= upper and lower <= ranges[j][1] <= upper:
                    ranges[j][0] = 0
                    ranges[j][1] = 0

    ans = 0
    for lower, upper in ranges:
        if lower == 0 and upper == 0:
            continue
        print(f"{lower = }, {upper = }")
        ans += upper - lower + 1

    return ans


def tests():
    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 14, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
