import math

def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))
    return lines

def extrapolate(line):
    numbers = [int(v) for v in line.split(" ")]
    v0 = numbers[-1]
    iterations = 0
    end = len(numbers) - 1
    while True:
        for i in range(end):
            numbers[i] = numbers[i+1] - numbers[i]
        # e0 = numbers[end]
        numbers[end] = 0
        iterations += 1
        
        # if difference between the last two numbers is 0, we're done
        if numbers[end-1] - numbers[end-2] == 0:
            break
        end -= 1
    
    # fordward loop to find next value
    n = numbers[end-1]
    for i in range(iterations-1):
        n += numbers[end]
        end += 1
        
    
    return numbers[-1]

def extrapolate2(line):
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

def star1(filename):
    lines = get_input(filename)
    
    sum = 0
    for line in lines:
        next_value = extrapolate2(line)
        sum += next_value
    
    return sum


def star2(filename):
    lines = get_input(filename)
    return None

def tests():
   assert extrapolate2("1 3 6 10 15 21") == 28
   assert extrapolate2("10 13 16 21 30 45") == 68

if __name__ == "__main__":
    tests()

    example = star1("example.txt")
    print(f'Example: {example}')
    assert(example == 114)
    
    print(f'First star: {star1("input.txt")}')
    # assert(star1("input.txt") == 21883)
    
    # example = star2("example2.txt")
    # print(f"Star 2 example {example}")
    # assert(example == 6)

    # ans = star2("input.txt")
    # assert ans == 12833235391111
    # print(f'Second star: {ans}')
