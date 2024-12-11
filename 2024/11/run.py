import math
from collections import defaultdict


def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines

def count_digits(number: int):
    return int(math.log10(number)) + 1

def split_digits(number: int, n_digits: int):
    assert n_digits % 2 == 0

    # very bad and slow way to split I think
    number_str = f"{number}"
    n2 = int(n_digits/2)
    left = int(number_str[0:n2])
    right = int(number_str[n2:])
    
    return left, right

def aoc(filename, star2=False):
    lines = get_input(filename)
    
    n = 25
    if star2:
        n = 75
    
    stones = [int(s) for s in lines[0].split(" ")]
    stone_values = defaultdict(int)
    for stone in stones:
        stone_values[stone] += 1

    for i in range(n):
        new_values = defaultdict(int)
        keys = list(stone_values.keys())
        for key in keys:
            count = stone_values[key]
            
            # skip count = 0 to optimize a bit
            if count == 0:
                continue
            
            if key == 0:
                new_values[1] += count
            else:
                n_digits = count_digits(key)
                if n_digits % 2 == 0:
                    left, right = split_digits(key, n_digits)
                    new_values[left] += count
                    new_values[right] += count
                else:
                    new_key = key * 2024
                    new_values[new_key] += count

        stone_values = defaultdict()
        for key, val in new_values.items():
            stone_values[key] = val

    total_count = 0
    for key, count in stone_values.items():
        total_count += count
    return total_count


def digits_of_product(a: int, b: int):
    
    return math.floor(math.log10(a) + math.log10(b)) + 1
    


def tests():
    assert count_digits(1234) == 4
    assert count_digits(1234567890) == 10
    assert count_digits(12345678901234567890) == 20
    assert count_digits(1234567890123456789012345678901234567890) == 40
    assert split_digits(1234, 4) == (12, 34)
    assert split_digits(1234567890, 10) == (12345, 67890)
    assert split_digits(1000, 4) == (10, 0)
    
    ans = aoc("example.txt")
    print(f"example star 1: {ans}")
    assert ans == 55312, f"wrong answer: {ans}"
    
    # ans = aoc("example.txt", star2=True)
    # print(f"example star 2: {ans}")
    # assert ans == 81, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"star 1: {ans}")
    assert ans == 185205
    
    ans = aoc("input.txt", star2=True)
    print(f"star 2: {ans}")
    assert ans == 221280540398419
