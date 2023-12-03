import numpy as np    

def find_number_in_loc(map, i, j):
    if not map[i][j].isdigit():
        return 0

    j = find_start_of_number(map, i, j)
    number = ""
    for k in range(j, len(map[0])):
        val = map[i][k]
        if val.isdigit():
            number += val
            # replace with dot to avoid duplicate counting
            map[i][k] = "."
        else:
            break

    if number == "":
        return 0
    else:
        return int(number)

def find_start_of_number(map, i, j):
    while map[i][j].isdigit():
        j -= 1
    
    return j+1


def main(filename, second=False):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))
    
    # pad with dots all around the edges
    lines = ["." + line + "." for line in lines]
    lines.append("." * len(lines[0]))
    lines.insert(0, "." * len(lines[0]))
    
    # make into nested lists to allow modification
    lines = [list(line) for line in lines]

    if False:    
        map = np.empty((0, len(lines[0])), dtype=int)
        for line in lines:
            map = np.vstack((map, np.asarray([list(line)])))
        
        # replace characters with -1
        for i in range(map.shape[0]):
            for j in range(map.shape[1]):
                if map[i, j] == ".":
                    map[i, j] = 0
                elif not map[i, j].isdigit():
                    map[i,j] = -1

        map = map.astype(int)
        print(map)
    
    
    sum = 0
    for i in range(1, len(lines) - 1):
        for j in range(1, len(lines[0]) - 1):
            val = lines[i][j]
            if val == ".":
                continue
            elif val.isdigit():
                continue
            else:
                sum += find_number_in_loc(lines, i-1, j+1)
                sum += find_number_in_loc(lines, i,   j+1)
                sum += find_number_in_loc(lines, i+1, j+1)
                
                sum += find_number_in_loc(lines, i+1, j)
                
                sum += find_number_in_loc(lines, i-1, j-1)
                sum += find_number_in_loc(lines, i,   j-1)
                sum += find_number_in_loc(lines, i+1, j-1)
                
                sum += find_number_in_loc(lines, i-1, j)
    
    return sum
                
            
            
            
    
    # for i in range(map.shape[0]):
    #     for j in range(map.shape[1]):
    #         if map[i, j] == -1:
    #             continue
    #         else:
    #             # create mask
    #             mask = np.zeros(map.shape, dtype=int)
    #             mask[i, j] = 1
    
    
    
    print(map)

    return None


def tests():
    lines = []
    with open("example.txt") as file:
        for line in file:
            lines.append(line.strip("\n"))
    
    # make into nested lists to allow modification
    lines = [list(line) for line in lines]
    
    assert find_number_in_loc(lines, 7, 8) == 755
    assert find_number_in_loc(lines, 2, 3) == 35
    assert lines[2][2] == "."
    assert lines[2][3] == "."
    # assert find_number_in_loc(lines, 2, 2) == 35
    assert find_number_in_loc(lines, 0, 0) == 467
    assert lines[0][0] == "."
    assert lines[0][1] == "."
    assert lines[0][2] == "."
    assert find_number_in_loc(lines, 0, 5) == 114
    assert lines[0][5] == "."
    assert lines[0][6] == "."
    assert lines[0][7] == "."
    
    
    
    


if __name__ == "__main__":
    tests()

    example = main("example.txt")
    # assert(example == 8)
    print(f'Example: {example}')
    
    print(f'First star: {main("input.txt")}')
    # assert(main("input.txt") == 2879)
    
    # example = main("example.txt", first=False)
    # assert(example == 2286)
    # print(f'Example: {example}')
    
    # print(f'Second star: {main("input.txt", first=False)}')
    # assert(main("input.txt", first=False) == 65122)
