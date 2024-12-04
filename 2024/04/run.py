def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines

template = [
    "ooooooo",
    "ooooooo",
    "ooooooo",
    "oooXooo",
    "ooooooo",
    "ooooooo",
    "ooooooo",
]

right = [
    "ooooooo",
    "ooooooo",
    "ooooooo",
    "oooXMAS",
    "ooooooo",
    "ooooooo",
    "ooooooo",
]
rightdown = [
    "ooooooo",
    "ooooooo",
    "ooooooo",
    "oooXooo",
    "ooooMoo",
    "oooooAo",
    "ooooooS",
]
down = [
    "ooooooo",
    "ooooooo",
    "ooooooo",
    "oooXooo",
    "oooMooo",
    "oooAooo",
    "oooSooo",
]
downleft = [
    "ooooooo",
    "ooooooo",
    "ooooooo",
    "oooXooo",
    "ooMoooo",
    "oAooooo",
    "Soooooo",
]
left = [
    "ooooooo",
    "ooooooo",
    "ooooooo",
    "SAMXooo",
    "ooooooo",
    "ooooooo",
    "ooooooo",
]
upleft = [
    "Soooooo",
    "oAooooo",
    "ooMoooo",
    "oooXooo",
    "ooooooo",
    "ooooooo",
    "ooooooo",
]
up = [
    "oooSooo",
    "oooAooo",
    "oooMooo",
    "oooXooo",
    "ooooooo",
    "ooooooo",
    "ooooooo",
]
upright = [
    "ooooooS",
    "oooooAo",
    "ooooMoo",
    "oooXooo",
    "ooooooo",
    "ooooooo",
    "ooooooo",
]

def look_for_xmas(lines, i, j):
    count = 0
    
    for arr in [right, rightdown, down, downleft, left, upleft, up, upright]:
        found = 0
        for ii in range(7):
            for jj in range(7):
                try:
                    found += lines[i+ii][j+jj] == arr[ii][jj]
                except Exception:
                    breakpoint()

        if found == 4:
            count += 1
    
    return count


def pad_with_dots(lines):
    n = len(lines)
    m = len(lines[0])
    
    ## pad with 3 dots in each direction to avoid exceptions
    # top
    lines = ["." * m] + lines
    lines = ["." * m] + lines
    lines = ["." * m] + lines

    # bottom
    lines = lines + ["." * m]
    lines = lines + ["." * m]
    lines = lines + ["." * m]

    # left and right
    for i in range(len(lines)):
        lines[i] = "..." + lines[i] + "..."
    
    if len(lines) < 10:
        for line in lines:
            print(line)

    assert len(lines) == n + 6
    for line in lines:
        assert len(line) == m + 6
    
    return lines


def count_xmas(lines):
    lines = pad_with_dots(lines)
    
    count = 0
    n = len(lines)
    m = len(lines[0])
    for i in range(n-6):  # skip edges
        for j in range(m-6):  # skip edges
            count += look_for_xmas(lines, i, j)

    return count


def star1(filename):
    lines = get_input(filename)
    
    return count_xmas(lines)


xmases = [
[
    "MoS",
    "oAo",
    "MoS",
],
[
    "SoS",
    "oAo",
    "MoM",
],
[
    "MoM",
    "oAo",
    "SoS",
],
[
    "SoM",
    "oAo",
    "SoM",
]
]

def look_for_xmas2(lines, i, j):
    count = 0
    
    for arr in xmases:
        matches = 0
        for ii in range(3):
            for jj in range(3):
                try:
                    matches += lines[i+ii][j+jj] == arr[ii][jj]
                except Exception:
                    breakpoint()

        if matches == 5:
            count += 1
    
    return count

def count_xmas2(lines):
    count = 0
    n = len(lines)
    m = len(lines[0])
    for i in range(n-2):  # skip edges
        for j in range(m-2):  # skip edges
            count += look_for_xmas2(lines, i, j)

    return count


def star2(filename):
    lines = get_input(filename)
    
    return count_xmas2(lines)


def tests():
    lines = [
        "XMAS"
    ]
    ans = count_xmas(lines)
    print(ans)
    assert ans == 1
    
    ans = star1("example.txt")
    print(f"example star 1: {ans}")
    assert ans == 18, f"wrong answer: {ans}"
    
    ans = star2("example.txt")
    print(f"example star 2: {ans}")
    assert ans == 9, f"wrong answer: {ans}"

if __name__ == "__main__":
    tests()
    
    ans = star1("input.txt")
    print(f"star 1: {ans}")
    assert ans == 2397

    ans = star2("input.txt")
    print(f"star 2: {ans}")
    assert ans == 1824
