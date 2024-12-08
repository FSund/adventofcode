def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def _can_be_true(current_value, values, expected_result, star2=False):
    if not len(values):
        return current_value == expected_result
    
    # list[1:] returns en empty list if only 1 value in the list
    plus = _can_be_true(current_value + values[0], values[1:], expected_result, star2)
    product = _can_be_true(current_value * values[0], values[1:], expected_result, star2)
    if star2:
        # convert to string, merge digits, and back to int
        # very slow, but works
        new_current = eval(f"{current_value}{values[0]}")
        concat = _can_be_true(new_current, values[1:], expected_result, star2)
    else:
        concat = False
    
    return plus or product or concat
    
    
def can_be_true(values, expected_result, star2=False):
    return _can_be_true(values[0], values[1:], expected_result, star2)


def get_result(line, star2=False):
    expected_result, values = line.split(": ")
    expected_result = int(expected_result)
    values = [int(v) for v in values.split(" ")]
    
    if can_be_true(values, expected_result, star2):
        return expected_result
    else:
        return 0


def do_calc(filename, star2=False):
    lines = get_input(filename)

    total = 0
    n_true = 0
    for line in lines:
        result = get_result(line, star2)
        n_true += result > 0
        total += result
    
    print(f"{n_true} of {len(lines)}")
    
    return total


# The engineers just need the total calibration result, which is the sum of the 
# test values from just the equations that could possibly be true. In the above 
# example, the sum of the test values for the three equations listed above is 3749.

# Determine which equations could possibly be true. What is their total 
# calibration result?


def tests():
    assert not can_be_true([1, 1, 10], 1)
    assert get_result("103: 3 1 1 5 98") == 0
    assert can_be_true([10, 10], 100)
    assert can_be_true([10, 10], 20)
    assert can_be_true([1, 1], 1)
    assert not can_be_true([10, 10], 1)
    assert can_be_true([1, 1, 1], 1)
    assert can_be_true([1, 1, 1, 1, 1, 1, 1, 1], 1)
    assert can_be_true([1, 1, 1, 1, 1, 1, 1, 1], 2)
    assert can_be_true([1, 1, 1, 1, 1, 1, 1, 1], 3)
    assert can_be_true([1, 1, 1, 1, 1, 1, 1, 1], 4)
    assert can_be_true([1, 1, 1, 1, 1, 1, 1, 1], 5)
    assert can_be_true([1, 1, 1, 1, 1, 1, 1, 1], 6)
    assert can_be_true([1, 1, 1, 1, 1, 1, 1, 1], 7)
    assert can_be_true([1, 1, 1, 1, 1, 1, 1, 1], 8)
    # assert can_be_true([10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 110*1e6 + 10)
    assert not can_be_true([1, 1, 10], 1)
    assert can_be_true([10, 10, 10], 110)
    assert can_be_true([10, 10, 10], 110)
    assert can_be_true([10, 10, 10, 10], 1010)
    assert can_be_true([10, 10, 10, 10], 10000)
    assert can_be_true([10, 10, 10], 200)
    
    assert get_result("3267: 81 40 27") == 3267
    assert get_result("110000010: 10 10 10 10 10 10 10 10 10 10") == 110*1e6 + 10
    
    assert get_result("453693978: 7 219 8 44 2 9 3 2 6 4 1 6") == 0
    assert not can_be_true([7, 219, 8, 44, 2, 9, 3, 2, 6, 4, 1, 6], 453693978)
    
    ans = do_calc("example.txt")
    print(f"example star 1: {ans}")
    assert ans == 3749, f"wrong answer: {ans}"
    
    ans = do_calc("example.txt", star2=True)
    print(f"example star 2: {ans}")
    assert ans == 11387, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = do_calc("input.txt")
    print(f"star 1: {ans}")
    assert ans == 5540634308362
    
    ans = do_calc("input.txt", star2=True)
    print(f"star 2: {ans}")
    # assert ans == 1984
