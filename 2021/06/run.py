import math

def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def star1(filename, days=80):
    lines = get_input(filename)
    
    fish = [int(f) for f in lines[0].split(",")]
    
    first_days = days - 7*math.floor(days/7)
    print(f"{first_days = }")
    for day in range(first_days):
        new_fish = []
        for i in range(len(fish)):
            if fish[i] == 0:
                fish[i] = 6
                new_fish.append(8)
            else:
                fish[i] -= 1

        fish += new_fish
        
        # if day % 10 == 0:
        #     print(len(fish))

    n = len(fish)
    print(f"{n = }")
    exponent = int((days - first_days)/7) - 2
    print(f"{exponent = }")
    n = n * (2**exponent)

    return n


def tests():
    ans = star1("example.txt")
    print(f"example star 1: {ans}")
    assert ans == 5934, f"wrong answer: {ans}"
    
    ans = star1("example.txt", days=256)
    print(f"example star 2: {ans}")
    assert ans == 26984457539, f"wrong answer: {ans}"

if __name__ == "__main__":
    tests()
    
    ans = star1("input.txt")
    print(f"star 1: {ans}")
    assert ans == 387413

    ans = star1("input.txt", days=256)
    print(f"star 2: {ans}")
    # assert ans == 23864
