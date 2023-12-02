def get_input(filename="input.txt"):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))
    return lines

lines = get_input("input.txt")
# lines = get_input("example.txt")
# print(lines[0][-1])

depth = 0
pos = 0
for line in lines:
    val = int(line[-1])
    if "forward" in line:
        pos += val
    elif "down" in line:
        depth += val
    elif "up" in line:
        depth -= val
    else:
        raise RuntimeError

print(depth*pos)

depth = 0
pos = 0
aim = 0
for line in lines:
    val = int(line[-1])
    if "forward" in line:
        pos += val
        depth += aim * val
    elif "down" in line:
        aim += val
    elif "up" in line:
        aim -= val
    else:
        raise RuntimeError

print(depth*pos)