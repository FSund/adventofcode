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


def star1(filename):
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


def star2(filename):
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
    
    sum = 0
    for i in range(1, len(lines) - 1):
        for j in range(1, len(lines[0]) - 1):
            val = lines[i][j]
            if val == "*":
                numbers = []
                numbers.append(find_number_in_loc(lines, i-1, j+1))
                numbers.append(find_number_in_loc(lines, i,   j+1))
                numbers.append(find_number_in_loc(lines, i+1, j+1))
                numbers.append(find_number_in_loc(lines, i+1, j))
                numbers.append(find_number_in_loc(lines, i-1, j-1))
                numbers.append(find_number_in_loc(lines, i,   j-1))
                numbers.append(find_number_in_loc(lines, i+1, j-1))
                numbers.append(find_number_in_loc(lines, i-1, j))
                numbers = [x for x in numbers if x != 0]
                if len(numbers) == 2:
                    sum += numbers[0] * numbers[1]
            else:
                continue
    
    return sum


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

    example = star1("example.txt")
    print(f'Example: {example}')
    
    print(f'First star: {star1("input.txt")}')
    assert(star1("input.txt") == 530495)
    
    assert(star2("example.txt") == 467835)
    print(f'Second star: {star2("input.txt")}')
    