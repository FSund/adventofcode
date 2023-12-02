import numpy as np

def get_input(filename="input.txt"):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))
    return lines

def test_star2():
    lines = get_input("example.txt")
    
    assert(not check_if_drop_row(np.asarray([0,0,0,0,0,0]), np.asarray([0,0,0,0,0,0]), 0))
    assert(not check_if_drop_row(np.asarray([0,0,0,0,0,0]), np.asarray([0,0,0,0,0,0]), 1))
    assert(not check_if_drop_row(np.asarray([0,0,0,0,0,0]), np.asarray([0,0,0,0,0,0]), 2))
    assert(not check_if_drop_row(np.asarray([0,0,0,0,0,0]), np.asarray([0,0,0,0,0,0]), 3))
    assert(not check_if_drop_row(np.asarray([0,0,0,0,0,0]), np.asarray([0,0,0,0,0,0]), 4))
    assert(not check_if_drop_row(np.asarray([0,0,0,0,0,0]), np.asarray([0,0,0,0,0,0]), 5))
    
    assert(check_if_drop_row(np.asarray([0,0,0,0,0,0]), np.asarray([1,1,1,1,1,1]), 0))
    assert(check_if_drop_row(np.asarray([0,0,0,0,0,0]), np.asarray([1,1,1,1,1,1]), 1))
    assert(check_if_drop_row(np.asarray([0,0,0,0,0,0]), np.asarray([1,1,1,1,1,1]), 2))
    assert(check_if_drop_row(np.asarray([0,0,0,0,0,0]), np.asarray([1,1,1,1,1,1]), 3))
    assert(check_if_drop_row(np.asarray([0,0,0,0,0,0]), np.asarray([1,1,1,1,1,1]), 4))
    assert(check_if_drop_row(np.asarray([0,0,0,0,0,0]), np.asarray([1,1,1,1,1,1]), 5))
    
    assert(not check_if_drop_row(np.asarray([1, 0, 1, 1, 1]), np.asarray([1, 0, 1, 1, 0]), 0))
    assert(not check_if_drop_row(np.asarray([1, 0, 1, 1, 1]), np.asarray([1, 0, 1, 1, 0]), 1))
    assert(not check_if_drop_row(np.asarray([1, 0, 1, 1, 1]), np.asarray([1, 0, 1, 1, 0]), 2))
    assert(not check_if_drop_row(np.asarray([1, 0, 1, 1, 1]), np.asarray([1, 0, 1, 1, 0]), 3))
    # assert(not check_if_drop_row(np.asarray([1, 0, 1, 1, 1]), np.asarray([1, 0, 1, 1, 0]), 4))
    
    # print(find_most_common(np.asarray([[0,0,0,0,0,0], [1,1,1,1,1,1]])))
    assert(np.all(find_most_common(np.asarray([[0,0,0,0,0,0], [1,1,1,1,1,1]])) == np.asarray([1,1,1,1,1,1])))
    assert(np.all(find_most_common(np.asarray([[0,0,0,0,0,0], [1,1,1,1,1,1], [1,1,1,1,1,1]])) == np.asarray([1,1,1,1,1,1])))
    assert(np.all(find_least_common(np.asarray([[0,0,0,0,0,0], [1,1,1,1,1,1]])) == np.asarray([0,0,0,0,0,0])))
    assert(np.all(find_least_common(np.asarray([[0,0], [1,1], [1,1]])) == np.asarray([0,0])))
    assert(np.all(find_least_common(np.asarray([[0,0], [1,0], [1,1]])) == np.asarray([0,1])))
    assert(np.all(find_least_common(np.asarray([[0,0,0,0,0,0], [1,1,1,1,1,1], [1,1,1,1,1,1]])) == np.asarray([0,0,0,0,0,0])))
    
    arr = np.asarray([[0,0,0], [1,0,0], [1,1,1]])
    most_common = find_most_common(arr)
    arr = do_col(arr, 0, most_common)
    # print(arr)
    most_common = find_most_common(arr)
    arr = do_col(arr, 1, most_common)
    assert(np.all(arr == np.asarray([1,1,1])))
    
    arr = np.asarray([[0,0,0], [1,0,0], [1,1,1]])
    most_common = find_least_common(arr)
    arr = do_col(arr, 0, most_common)
    # print(arr)
    assert(np.all(arr == np.asarray([0,0,0])))
    
    arr = np.asarray([[0,0,0], [0,1,0], [1,1,1], [1,1,1], [1,1,1]])
    most_common = find_least_common(arr)
    arr = do_col(arr, 0, most_common)
    # print(arr)
    most_common = find_least_common(arr)
    arr = do_col(arr, 0, most_common)
    assert(np.all(arr == np.asarray([0,0,0])))
    
    arr = np.asarray([list(line) for line in lines], dtype=int)
    least_common = find_least_common(arr)
    arr = do_col(arr, 0, least_common)
    # print(arr)
    assert(np.all(arr[:,0] == np.asarray([0,0,0,0,0])))
    least_common = find_least_common(arr)
    print(least_common)
    arr = do_col(arr, 1, least_common)
    print(arr)
    assert(np.all(arr[:,1] == np.asarray([1,1])))
    print(arr)
    
    assert(np.all(find_ox(lines) == np.asarray([[1,0,1,1,1]])))
    assert(np.all(find_co(lines) == np.asarray([[0,1,0,1,0]])))
    
    ox = find_ox(lines)
    print(f"{ox = }")
    ox = eval(f"0b{''.join([str(int(x)) for x in ox[0]])}")
    print(f"{ox = }")
    
    co = find_co(lines)
    print(f"{co = }")
    co = eval(f"0b{''.join([str(int(x)) for x in co[0]])}")
    print(f"{co = }")
    
    return ox*co

def star2(filename):
    lines = get_input(filename)
    
    ox = find_ox(lines)
    # print(f"{ox = }")
    ox = eval(f"0b{''.join([str(int(x)) for x in ox[0]])}")
    # print(f"{ox = }")
    
    co = find_co(lines)
    # print(f"{co = }")
    co = eval(f"0b{''.join([str(int(x)) for x in co[0]])}")
    # print(f"{co = }")
    
    return ox*co


def check_if_drop_row(row, criteria, col_idx):
    test = (row == criteria)
    return not test[col_idx]
    # print(f"{test = }")
    # count = np.sum(test[:col_idx+1])
    # if count < col_idx + 1:
    #     # drop the row
    #     # print(f"drop row {i}: {arr[i,:]}")
    #     return True
    # else:
    #     return False

def find_most_common(arr):
    m = np.round(np.mean(arr, axis=0) + 1e-10)
    # convert to int
    m = m.astype(int)
    return m

def find_least_common(arr):
    m = np.round(np.mean(arr, axis=0) + 1e-10)
    # print(m)
    m = np.logical_not(m)
    # print(m)
    # convert to int
    m = m.astype(int)
    return m

def do_col(arr, j, criteria):
    n = arr.shape[0]
    for i in range(n)[::-1]:  # reverse loop
        if check_if_drop_row(arr[i,:], criteria, j):
            arr = np.delete(arr, i, axis=0)
    return arr

def find_ox(lines):
    arr = np.asarray([list(line) for line in lines], dtype=int)
    # print(f"mean: {np.mean(arr, axis=0)}")
    # most_common = np.round(np.mean(arr, axis=0))
    # print(f"{most_common = }")
    # least_common = np.logical_not(most_common)
    # print(f"{least_common = }")
    
    # most_common = find_most_common(arr)

    # crit = bin(eval(f"0b{''.join([str(int(x)) for x in most_common])}"))
    # print(type(crit))
    # print(crit)

    # binary_rows = [bin(eval(f"0b{''.join([str(int(x)) for x in row])}")) for row in arr]

    # for row in binary_rows:
    #     breakpoint()
    
    for j in range(0, arr.shape[1]):
        # print(f"colum {j}")
        most_common = find_most_common(arr)
        # print(f"{most_common = }")
        arr = do_col(arr, j, most_common)
        if arr.shape[0] == 1:
            return arr

    raise RuntimeError("No OX found")
                
def find_co(lines):
    arr = np.asarray([list(line) for line in lines], dtype=int)
    # most_common = np.round(np.mean(arr, axis=0))
    # # print(f"{most_common = }")
    # least_common = np.logical_not(most_common)
    # # print(f"{least_common = }")

    for j in range(0, arr.shape[1]):
        # print(f"colum {j}")
        least_common = find_least_common(arr)
        n = arr.shape[0]
        for i in range(n)[::-1]:  # reverse loop
            # print(f"row {i}")
            # test = arr[i,:] == least_common
            # print(f"{test = }")
            # if np.sum(test[:j]) <= j:
            #     # drop the row
            #     # print(f"drop row {i}: {arr[i,:]}")
            #     arr = np.delete(arr, i, axis=0)
            if check_if_drop_row(arr[i,:], least_common, j):
                arr = np.delete(arr, i, axis=0)
            if arr.shape[0] == 1:
                # print(f"{arr = }")
                return arr
            


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
    assert star2("example.txt")==230
    print(star2("input.txt"))
