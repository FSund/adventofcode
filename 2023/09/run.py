import math

def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))
    return lines


def extrapolate_star1(line):
    numbers = [int(v) for v in line.split(" ")]
    numbers.append(0)
    rows = []
    rows.append(numbers)
    for i in range(len(numbers) - 1):
        rows.append([0 for i in range(len(numbers))])
    
    for i in range(1, len(rows)):
        for j in range(len(numbers) - i - 1):
            rows[i][j] = rows[i-1][j+1] - rows[i-1][j]
    
    for i in range(len(rows) - 1)[::-1]:
        j = len(numbers) - i - 1
        for k in range(j, len(numbers)):
            rows[i][k] = rows[i][k-1]
    
    # forward loop
    for i in range(len(rows) - 1)[::-1]:
        j = len(numbers) - i - 1
        rows[i][j] = rows[i][j-1] + rows[i+1][j-1]
        
    return rows[0][-1]

def extrapolate_star2(line):
    numbers = [int(v) for v in line.split(" ")]
    numbers.append(0)
    rows = []
    rows.append(numbers)
    for i in range(len(numbers) - 1):
        rows.append([0 for i in range(len(numbers))])
    
    for i in range(1, len(rows)):
        for j in range(len(numbers) - i - 1):
            rows[i][j] = rows[i-1][j+1] - rows[i-1][j]
    
    for i in range(len(rows) - 1)[::-1]:
        j = len(numbers) - i - 1
        for k in range(j, len(numbers)):
            rows[i][k] = rows[i][k-1]
    
    # forward loop
    for i in range(len(rows) - 1)[::-1]:
        j = len(numbers) - i - 1
        rows[i][j] = rows[i][j-1] + rows[i+1][j-1]
    
    for i in range(len(rows)):
        # add element to front of list
        rows[i].insert(0, 0)
        
    i = len(rows) - 1
    while True:
        if rows[i][1] != 0:
            break
        i -= 1
    
    rows[i][0] = rows[i][1]
    
    # print(list(range(i)[::-1]))
    
    for i in range(i)[::-1]:
        rows[i][0] = rows[i][1] - rows[i+1][0]
        
    return rows[0][0]

def star1(filename):
    lines = get_input(filename)
    
    sum = 0
    for line in lines:
        next_value = extrapolate_star1(line)
        sum += next_value
    
    return sum


def star2(filename):
    lines = get_input(filename)
    
    sum = 0
    for line in lines:
        next_value = extrapolate_star2(line)
        sum += next_value
    
    return sum

def tests():
    assert extrapolate_star2("10 13 16 21 30 45") == 5

    assert extrapolate_star1("1 3 6 10 15 21") == 28
    assert extrapolate_star1("10 13 16 21 30 45") == 68

if __name__ == "__main__":
    tests()

    example = star1("example.txt")
    print(f'Example: {example}')
    assert(example == 114)
    
    print(f'First star: {star1("input.txt")}')
    assert(star1("input.txt") == 1934898178)
    
    example = star2("example.txt")
    print(f"Star 2 example: {example}")
    assert(example == 2)

    ans = star2("input.txt")
    # assert ans == 12833235391111
    print(f'Second star: {ans}')
