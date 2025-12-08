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

    ans = 0
    numbers = []
    for j in reversed(range(len(lines[0]))):  # right to left
        number = ""
        for i in range(len(lines) - 1):  # top to bottom
            number += lines[i][j]
        if number.split() == []:
            continue
        number = eval(number)
        numbers.append(number)

        # stop adding numbers to list when we find operator
        # add the answer to the sum
        if lines[-1][j] != " ":  # if operator
            op = lines[-1][j]  # operator
            this = 0
            if op == "*":
                this = 1
                for number in numbers:
                    this *= number
            elif op == "+":
                for number in numbers:
                    this += number

            ans += this
            numbers = []

    return ans


def tests():
    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 3263827, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
