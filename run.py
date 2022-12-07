from aoc import Dir

def get_lines_until_next_command(lines):
    out = []
    for line in lines:
        if "$" in line:
            break
        else:
            out.append(line)

    return out


def get_sum_of_file_sizes(lines):
    sum_of_file_sizes = 0
    for line in lines:
        if "dir" in line:
            pass
        else: # file
            sum_of_file_sizes += int(line.split(" ")[0])
    
    return sum_of_file_sizes

def cd_cmd(lines):
    pass

def ls_cmd(lines):
    # print(lines)
    sum_of_file_sizes = 0
    dirs = []
    for line in lines:
        if "dir" in line:
            name = line.split(" ")[1]
            dirs.append(Dir(name))
        else: # file
            sum_of_file_sizes += int(line.split(" ")[0])
    
    return sum_of_file_sizes, dirs

lines = []
with open("input.txt") as file:
    for line in file:
        lines.append(line[:-1])

dirs = Dir("/")
path = []
sizes = {}
for idx, line in enumerate(lines):
    if "$ cd" in line:
        p = line.split(" ")[-1]
        if p == "..":
            path.pop()
        else:
            path += [p]
            dirs
        print(path)
    if "$ ls" in line:
        # size, dirs = ls_cmd(get_lines_until_next_command(lines[idx+1:]))
        # print(size, dirs)
        # pass
        ls_out = get_lines_until_next_command(lines[idx+1:])
        print(f"{ls_out = }")
        f_sum = get_sum_of_file_sizes(ls_out)
        sizes[":".join(path)] = f_sum

print(sizes)
