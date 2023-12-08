import math

def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))
    return lines

def star1(filename):
    lines = get_input(filename)
    
    m = {}
    for line in lines[2:]:
        key, lr = line.split(" = ")
        lr = lr.strip("(").strip(")")
        lr = [f.strip() for f in lr.split(",")]
        m[key] = lr
    
    instructions = list(lines[0])
    pos = "AAA"
    count = 0
    while True:
        for ins in instructions:
            # print(f"instruction: {ins}")
            if ins == "L":
                pos = m[pos][0]
            elif ins == "R":
                pos = m[pos][1]
            else:
                print("Unknown instruction")
                return

            count += 1

            if pos == "ZZZ":
                break
            
        if pos == "ZZZ":
            break
    
    return count


def do_move(positions, m, instructions):
    count = 0
    for ins in instructions:
        # move all positions
        for pos in positions:
            if ins == "L":
                pos = m[pos][0]
            else:
                pos = m[pos][1]

        # check if all positions end with z
        for pos in positions:
            if pos[-1] != "Z":
                break
        else:
            return count
    
    return count


def get_count(pos, m, instructions):
    count = 0
    z_pos = None
    while True:
        for ins in instructions:
            if ins == "L":
                pos = m[pos][0]
            else:
                pos = m[pos][1]

            count += 1
            if pos[-1] == "Z":
                if z_pos and pos == z_pos:
                    return count
                else:
                    # found first z
                    z_pos = pos
                    # reset count, so we count length of z-to-z loop
                    count = 0


def star2(filename):
    lines = get_input(filename)
    m = {}
    for line in lines[2:]:
        key, lr = line.split(" = ")
        lr = lr.strip("(").strip(")")
        lr = [f.strip() for f in lr.split(",")]
        m[key] = lr
    
    instructions = list(lines[0])
    positions = []
    for key in m.keys():
        if key[-1] == "A":
            positions.append(key)

    print(f"Starting positions: {positions}")
    
    counts = []
    for pos in positions:
        counts.append(get_count(pos, m, instructions))

    return math.lcm(*counts)

def tests():
   pass
    
    


if __name__ == "__main__":
    tests()

    example = star1("example.txt")
    print(f'Example: {example}')
    assert(example == 6)
    
    print(f'First star: {star1("input.txt")}')
    assert(star1("input.txt") == 21883)
    
    example = star2("example2.txt")
    print(f"Star 2 example {example}")
    assert(example == 6)

    ans = star2("input.txt")
    assert ans == 12833235391111
    print(f'Second star: {ans}')
