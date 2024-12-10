def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def aoc(filename, days=80):
    lines = get_input(filename)
    
    fish = [int(f) for f in lines[0].split(",")]
    timers = [0 for i in range(9)]
    for f in fish:
        timers[f] += 1
        
    for day in range(days):
        n_spawned = timers[0]
        timers[0] = timers[1]
        timers[1] = timers[2]
        timers[2] = timers[3]
        timers[3] = timers[4]
        timers[4] = timers[5]
        timers[5] = timers[6]
        timers[6] = timers[7] + n_spawned
        timers[7] = timers[8]
        timers[8] = n_spawned
    
    return sum(timers)


def tests():
    ans = aoc("example.txt", days=80)
    print(f"example star 1: {ans}")
    assert ans == 5934, f"wrong answer: {ans}"
    
    ans = aoc("example.txt", days=256)
    print(f"example star 2: {ans}")
    assert ans == 26984457539, f"wrong answer: {ans}"

if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt", days=80)
    print(f"star 1: {ans}")
    assert ans == 387413

    ans = aoc("input.txt", days=256)
    print(f"star 2: {ans}")
    assert ans == 1738377086345
