def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def aoc(filename):
    lines = get_input(filename)
    n = 50
    code = 0
    for line in lines:
        line = line.replace("L", "-").replace("R", "+")
        n = n + eval(line)
        n = n % 100

        if n == 0:
            code += 1

    return code

    


def tests():
    ans = aoc("example.txt")
    print(f"example star 1: {ans}")
    assert ans == 3, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"star 1: {ans}")
