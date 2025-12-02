from pathlib import Path

def get_input(filename):
    script_dir = Path(__file__).parent
    lines = []
    with open(script_dir / filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


# def check_halves_recursive(s):
#     length = len(s)

#     # stop if odd length
#     if length % 2 != 0:
#         return False

#     half = length // 2
#     left = s[: half]
#     right = s[half :]

#     if left == right:
#         # stop if the two halves are identical
#         return True
#     else:
#         # else, split further
#         return check_halves_recursive(left) and check_halves_recursive(right)


def check_number(s: str):
    length = len(s) - 1
    while length >= 1:
        # check if divisible by length
        if len(s) % length != 0:
            length -= 1
            continue

        # split into parts
        parts = [s[i : i + length] for i in range(0, len(s), length)]
        all_equal = all(part == parts[0] for part in parts)
        if all_equal:
            return True
        
        length -= 1
    
    return False


def check_range(r):
    ans = 0
    start, end = map(int, r.split("-"))
    for current_number in range(start, end + 1):
        s = str(current_number)
        if check_number(s):
            ans += current_number
            print(current_number)

    return ans


def aoc(filename):
    lines = get_input(filename)
    ranges = lines[0].split(",")

    ans = 0
    for r in ranges:
        ans += check_range(r)

    return ans

    


def tests():
    assert check_range("11-22") == 11+22
    assert check_range("824824821-824824827") == 824824824
    assert check_range("2121212118-2121212124") == 2121212121
    
    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 4174379265, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
