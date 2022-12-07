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

lines = []
with open("input.txt") as file:
    for line in file:
        lines.append(line[:-1])

for i in range(10):
    lines.append("$ cd ..")

fs = FileSystem()
path = []
for idx, line in enumerate(lines):
    if "$ cd" in line:
        dir = line.split(" ")[-1]
        if dir == "..":
            path.pop()
            if len(path) == 0:
                break
        else: # go to dir
            path += [dir]
            fs.mkdir_p(path)
    if "$ ls" in line:
        ls_out = get_lines_until_next_command(lines[idx+1:])
        f_sum = get_sum_of_file_sizes(ls_out)
        
        fs.add_files(path, f_sum)

total_file_size = fs.get_total_size()

s = 0
for size in Dir.totals:
    if size <= 100000:
        s += size
print(f"first star: {s}")
# first star: 1077191

disk_size = 70000000
required_space = 30000000

# Find the smallest directory that, if deleted, would free up enough space on the filesystem to run the update. What is the total size of that directory?
free_space = disk_size - total_file_size
required_delete = required_space - free_space

acceptable = []
for size in Dir.totals:
    if size >= required_delete:
        acceptable.append(size)

# print(acceptable)
print(f"second star: {min(acceptable)}")

# 25773269 too high
# 5649896 ok
