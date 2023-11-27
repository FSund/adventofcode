lines = []
with open("input.txt") as file:
    for line in file:
        lines.append(line[:-1])

# hack to force update of root dir size
for i in range(10):
    lines.append("$ cd ..")

def get_cwd_str(cwd):
    return "/".join(cwd)

cwd = []  # current working dir
fs = {}  # "filesystem"
for line in lines:
    if "$ cd" in line:
        dir = line.split(" ")[-1]
        if dir == "..":
            s = fs[get_cwd_str(cwd)]
            cwd.pop()
            if len(cwd) == 0:
                break
            
            # update totals for this dir
            fs[get_cwd_str(cwd)] += s
        else: # go to dir
            cwd += [dir]
            fs[get_cwd_str(cwd)] = 0
    elif "$ ls" in line:
        pass
    else:
        if "dir" in line:
            pass
        else:
            fs[get_cwd_str(cwd)] += int(line.split(" ")[0])

star_1_sum = 0
for key, size in fs.items():
    if size <= 100000:
        star_1_sum += size
print(f"{star_1_sum = }")

disk_size = 70000000
required_space = 30000000

free_space = disk_size - fs["/"]
required_delete = required_space - free_space

candidates = []
for key, size in fs.items():
    if size >= required_delete:
        candidates.append(size)

print(f"second star: {min(candidates)}")
