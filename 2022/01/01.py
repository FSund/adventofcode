
calories = []
with open("input.txt") as f:
    cals = 0
    for line in f:
        if line == "\n":
            calories.append(cals)
            cals = 0
        else:
            cals += int(line)
        
        print(line)
        print(cals)
    else:
        print("DONE")

print(calories)
print(max(calories))
print(calories.sort())
print(calories[-3:])
print(sum(calories[-3:]))
breakpoint()
