from aoc import Dir, FileSystem

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

for i in range(10):
    lines.append("$ cd ..")

fs = FileSystem()
path = []
sizes = {}
for idx, line in enumerate(lines):
    if "$ cd" in line:
        dir = line.split(" ")[-1]
        if dir == "..":
            # update total when leaving dir
            sizes[":".join(path)]["total"] = sizes[":".join(path)]["local"] + sizes[":".join(path)]["subdirs"]
            
            # update subdirs size when entering folder one level up
            f_sum = sizes[":".join(path)]["local"]
            path.pop()
            if len(path) == 0:
                break
            sizes[":".join(path)]["subdirs"] += f_sum
        else: # go to dir
            path += [dir]
            fs.mkdir_p(path)

            # create dir
            sizes[":".join(path)] = {}
            sizes[":".join(path)]["local"] = 0
            sizes[":".join(path)]["subdirs"] = 0
            sizes[":".join(path)]["total"] = 0
        print(path)
    if "$ ls" in line:
        # size, dirs = ls_cmd(get_lines_until_next_command(lines[idx+1:]))
        # print(size, dirs)
        # pass
        ls_out = get_lines_until_next_command(lines[idx+1:])
        print(f"{ls_out = }")
        f_sum = get_sum_of_file_sizes(ls_out)
        print(f"{f_sum = }")
        sizes[":".join(path)]["local"] = f_sum
        # dirs.
        
        fs.add_files(path, f_sum)

total_file_size = fs.get_total_size()

s = 0
for size in Dir.totals:
    if size <= 100000:
        s += size
print(s)

# print(sizes)

disk_size = 70000000
required_space = 30000000

# Find the smallest directory that, if deleted, would free up enough space on the filesystem to run the update. What is the total size of that directory?
free_space = disk_size - total_file_size
required_delete = required_space - free_space

acceptable = []
for size in Dir.totals:
    if size >= required_delete:
        acceptable.append(size)

print(acceptable)
print(min(acceptable))

# 25773269 too high