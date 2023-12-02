import numpy as np

def get_input(filename="input.txt"):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))
    return lines

def star2():
    # lines = get_input("input.txt")
    lines = get_input("example.txt")

    arr = np.asarray([list(line) for line in lines], dtype=int)
    most_common = np.round(np.mean(arr, axis=0))
    print(most_common)

    crit = bin(eval(f"0b{''.join([str(int(x)) for x in most_common])}"))
    print(type(crit))
    print(crit)

    binary_rows = [bin(eval(f"0b{''.join([str(int(x)) for x in row])}")) for row in arr]

    for row in binary_rows:
        # print(row && crit)
        pass


def star1():
    lines = get_input("input.txt")
    # lines = get_input("example.txt")

    m = len(lines[0])
    sum = [0 for i in range(m)]

    for line in lines:
        for j in range(m):
            sum[j] += int(line[j])

    n = len(lines)

    gamma = ""
    epsilon = ""
    for i in range(m):
        sum[i] /= len(lines)
        sum[i] = int(sum[i] > 0.5)
        gamma += f"{int(sum[i] >= 0.5)}"
        epsilon += f"{int(sum[i] < 0.5)}"

    r = ""
    for d in sum:
        r += f"{d}"

    gamma = int(eval(f"0b{gamma}"))
    epsilon = int(eval(f"0b{epsilon}"))
    print(f"star 1: {gamma*epsilon}")
    
    assert(gamma*epsilon == 3277364)

    # print(r)
    # bbb = eval(f"0b{r}")
    # print(int(bbb))

    # ccc = ~bbb
    # print(int(bbb))

    # print(bbb*ccc)

if __name__ == "__main__":
    star1()
    star2()
