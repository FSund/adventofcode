def get_input(filename="input.txt"):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))
    return lines

lines = get_input("input.txt")
# lines = get_input("example.txt")

n = 0
for i in range(len(lines) - 1):
    if int(lines[i+1]) > int(lines[i]):
        n += 1
    
        
print(f"first star: {n}")

values = []
for line in lines:
    values.append(int(line))

n = 0
for i in range(len(values) - 3):
    left = values[i] + values[i+1] + values[i+2]
    right = values[i+1] + values[i+2] + values[i+3]
    if right > left:
        n += 1
        
print(f"second star: {n}")
