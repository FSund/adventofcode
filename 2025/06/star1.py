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

    operators = lines[-1].split()
    inputs = []
    inputs.append(lines[0].split())
    inputs.append(lines[1].split())
    inputs.append(lines[2].split())
    inputs.append(lines[3].split())

    ans = 0
    for idx, op in enumerate(operators):
        s = f"{inputs[0][idx]} {op} {inputs[1][idx]} {op} {inputs[2][idx]} {op} {inputs[3][idx]}"
        ans += eval(s)
    
    return ans



# def tests():
#     ans = aoc("example.txt")
#     print(f"example: {ans}")
#     assert ans == 4277556, f"wrong answer: {ans}"


if __name__ == "__main__":
    # tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
