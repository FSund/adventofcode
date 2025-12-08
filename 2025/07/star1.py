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

    beams = [0] * len(lines[0])
    beams[lines[0].find("S")] = 1

    n = len(lines[0])
    new_beams = [0] * len(lines[0])
    ans = 0
    for line in lines[1:]:
        for j in range(n):
            if line[j] == "^":
                if beams[j]:
                    if j >= 1:
                        new_beams[j-1] += 1
                    if j < n-1:
                        new_beams[j+1] += 1
                    ans += 1

            # pass on non-split beams
            elif beams[j]:
                new_beams[j] += 1

        beams = new_beams
        # print(beams)
        new_beams = [0] * len(lines[0])
    
    return ans

                    



def tests():
    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 21, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
