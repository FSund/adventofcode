import numba
from numba import njit, int64
import concurrent.futures
import functools

def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))
    return lines


def get_ways_to_win(time, record_distance):
    count = 0
    for hold_time in range(0, time):
        speed = hold_time
        distance_travelled = speed * (time - hold_time)
        
        if distance_travelled > record_distance:
            count += 1

    return count


def star1(filename):
    # lines = get_input(filename)
    if filename == "example.txt":
        times = [7, 15, 30]
        distances = [9, 40, 200]
    else:
        times = [40, 92, 97, 90]
        distances = [215, 1064, 1505, 1100]
    
    product = 1
    for time, distance in zip(times, distances):
        count = get_ways_to_win(time, distance)

        # print(count)
        product *= count
    
    return product
    

def star2(filename):
    if filename == "example.txt":
        time = 71530
        distance = 940200
    else:
        time = 40929790
        distance = 215106415051100
    
    count = get_ways_to_win(time, distance)
    
    return count


def tests():
    assert get_ways_to_win(7, 9) == 4
    assert get_ways_to_win(15, 40) == 8
    assert get_ways_to_win(30, 200) == 9
    


if __name__ == "__main__":
    tests()

    example = star1("example.txt")
    assert(example == 288)
    print(f'Example: {example}')
    
    print(f'First star: {star1("input.txt")}')
    assert(star1("input.txt") == 6209190)
    
    print(f'Second star: {star2("input.txt")}')
    assert(star2("input.txt") == 28545089)
