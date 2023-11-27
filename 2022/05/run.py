import numpy as np

def get_priority(char):
    if char.islower():
        return ord(char) - 97 + 1
    else:
        return ord(char) - 65 + 27

def intersection(lst1, lst2):
    return [value for value in lst1 if value in lst2]

def is_fully_contained_in_other(r1, r2):
    if r1[0] <= r2[0] and r1[1] >= r2[1]:
        return True
    elif r2[0] <= r1[0] and r2[1] >= r1[1]:
        return True
    else:
        return False

def has_some_overlap(r1, r2):
    # r1[0]   r1[1]
    #      r2[0]     r2[1]
    if r1[0] <= r2[0] and r1[1] >= r2[0]:
        return True
    #      r1[0]     r1[1]
    # r2[0]   r2[1]
    if r2[0] <= r1[0] and r2[1] >= r1[0]:
        return True

    return False
    

def get_starting_stacks(file):
    line = "yes"
    lines = []
    while line != "\n":
        line = file.readline()
        lines.append(line.strip("\n"))
    lines = lines[:-1]
    stacks = [[]]*len(lines[-1].replace(" ", ""))
    
    for line in lines[:-1]:
        for i in range(len(stacks)):
            stacks[i].append(line[i*5 + 1])
    
    return stacks

def get_start_numpy(file):
    m = np.empty((9, 36),  dtype=str)
    for i in range(9):
        line = file.readline()
        for j, c in enumerate(line[:-2]):
            m[i, j] = c
    # print(m[0, :])
    m = np.fliplr(m.transpose())
    n = np.empty((9, 8), dtype=str)
    for i in range(9):
        n[i, :] = (m[i*4 + 1, 1:])
    print(n)
    stacks = n.tolist()
    for i in range(9):
        for j in range(8)[::-1]:
            if stacks[i][j] == " ":
                stacks[i].pop(j)
    return stacks

def do_move(amount, source, destination, stacks):
    while amount:
        stacks[destination].append(stacks[source][-1])
        stacks[source].pop(-1)
        amount -= 1

def do_move_2(amount, source, destination, stacks):
    stacks[destination] += stacks[source][-amount:]
    while amount:
        stacks[source].pop(-1)
        amount -= 1

def get_output(stacks):
    out = ""
    for s in stacks:
        if len(s):
            out += s[-1]
        else:
            out += " "

    return out


sum = 0
with open("input.txt") as file:
    # get_starting_stacks(file)
    stacks = get_start_numpy(file)
    file.readline()
    
    for line in file:
        line = line[:-1]
        # example: "move 2 from 4 to 2"
        _, amount, _, source, _, destination = line.split(" ")
        # do_move(int(amount), int(source)-1, int(destination)-1, stacks)
        do_move_2(int(amount), int(source)-1, int(destination)-1, stacks)
        # print(stacks)
        # print(get_output(stacks))

print(get_output(stacks))
