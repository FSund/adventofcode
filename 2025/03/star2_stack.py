from pathlib import Path

def get_input(filename):
    script_dir = Path(__file__).parent
    lines = []
    with open(script_dir / filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def argmax(line: str) -> int:
    """
    Returns index of largest number (the first one)
    """
    for d in list("987654321"):
        idx = line.find(d)
        if idx >= 0:
            return idx
        
    raise RuntimeError("Couldn't find max")


def make_largest_joltage(line: str, batteries_needed = 12) -> int:
    """
    turn on exactly batteries_needed batteries
    """

    n = len(line)
    batteries = [int(line[0])]
    for idx in range(1, n):
        joltage = int(line[idx])
        if joltage > batteries[-1]:
            while len(batteries) and joltage > batteries[-1] and (batteries_needed - len(batteries) < n - idx):
                batteries.pop()
            batteries.append(joltage)
        elif len(batteries) < batteries_needed:
            batteries.append(joltage)

    return int("".join(f"{j}" for j in batteries))


def aoc(filename):
    lines = get_input(filename)

    ans = 0
    for line in lines:
        ans += make_largest_joltage(line)

    return ans


def tests():
    # assert make_largest_joltage("98111111111", 3) == 981
    assert make_largest_joltage("8191", 3) == 891

    # make_largest_joltage("2232546378857275787561723292343835435343333776427842773354273372424413455462238746648634437374254318")
    assert make_largest_joltage("234234234234278") == 434234234278
    assert make_largest_joltage("987654321111111") == 987654321111
    assert make_largest_joltage("811111111111119") == 811111111119
    assert make_largest_joltage("818181911112111") == 888911112111

    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 3121910778619, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
