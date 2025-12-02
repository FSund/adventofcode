def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def count_zeros(old: int, new: int) -> int:
    assert old >= 0 and old < 100
    if 0 < new < 100:
        return 0
    
    assert new != old, "old and new cannot be the same"
    
    n = old  # current position
    at_zero = 0
    while n != new:
        if new > old:
            n += 1
            if n % 100 == 0:
                at_zero += 1
        if new < old:
            n -= 1
            if n % 100 == 0:
                at_zero += 1

    return at_zero


def aoc(filename):
    lines = get_input(filename)
    old = 50
    code = 0
    for line in lines:
        line = line.replace("L", "-").replace("R", "+")
        new = old + eval(line)
        
        at_zero = count_zeros(old, new)
        code += at_zero
        
        old = new % 100
        print(f"{old = }, {at_zero = }")

    return code


def tests():
    assert 50 // 100 == 0
    assert 150 // 100 == 1
    assert 250 // 100 == 2
    assert abs(-50 // 100) == 1
    assert abs(-150 // 100) == 2
    assert abs(-250 // 100) == 3

    assert 100 // 100 == 1
    assert 200 // 100 == 2
    assert 0 // 100 == 0

    assert count_zeros(99, 100) == 1
    assert count_zeros(99, 101) == 1
    assert count_zeros(0, 100) == 1
    assert count_zeros(1, 0) == 1
    assert count_zeros(0, 1) == 0
    assert count_zeros(0, -5) == 0
    assert count_zeros(50, 150) == 1
    assert count_zeros(50, 250) == 2
    assert count_zeros(50, -50) == 1
    assert count_zeros(50, -150) == 2
    assert count_zeros(50, -250) == 3

    ans = aoc("example.txt")
    print(f"example star 1: {ans}")
    assert ans == 6, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"star 2: {ans}")
