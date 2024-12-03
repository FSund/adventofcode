def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def starts_with_mul(substring):
    if len(substring) >= 4:
        if substring[:4] == "mul(":
            return True

    return False


def get_numbers_until_next_rparen(substring):
    maybe_number_pair,_, right = substring.partition(")")
    if len(maybe_number_pair) <= 7 and len(maybe_number_pair) >= 3:  # max 3 digits per number, plus comma
        if "," in maybe_number_pair:
            left, right = maybe_number_pair.split(",")
            if left.isdigit() and right.isdigit():
                return int(left), int(right)

    return None


def get_product(substring):
    result = get_numbers_until_next_rparen(substring)
    if result:
        return result[0]*result[1]
    else:
        return 0


def get_product_if_mul(substring):
    if starts_with_mul(substring):
        return get_product(substring[4:])
    else:
        return 0


def star1(filename):
    lines = get_input(filename)
    total = 0
    for line in lines:
        for i in range(len(line)):
            total += get_product_if_mul(line[i:])

    return total


def is_dont(substring):
    dont = "don't()"
    if len(substring) >= len(dont):
        if substring[:len(dont)] == dont:
            return True
    
    return False


def is_do(substring):
    do = "do()"
    if len(substring) >= len(do):
        if substring[:len(do)] == do:
            return True
    
    return False


def star2(filename):
    lines = get_input(filename)
    total = 0
    enabled = True
    for line in lines:
        for i in range(len(line)):
            if is_dont(line[i:]):
                enabled = False
                continue
            if is_do(line[i:]):
                enabled = True
                continue

            product = get_product_if_mul(line[i:])
            if enabled:
                total += product

    return total


def tests():
    assert starts_with_mul("mul(")
    assert not starts_with_mul("mul")
    
    assert get_numbers_until_next_rparen("") is None
    assert get_numbers_until_next_rparen(")") is None
    assert get_numbers_until_next_rparen(",)") is None
    assert get_numbers_until_next_rparen("1,1)") == (1,1)
    assert get_numbers_until_next_rparen("123,123)") == (123,123)
    
    assert is_dont("don't()")
    assert not is_dont("dont()")
    assert not is_dont("#don't()")
    assert not is_dont("##don't()")
    assert not is_dont("#don't()#")
    
    assert is_do("do()")
    assert not is_do("do'()")
    assert not is_do("#do()")
    assert not is_do("#do'()#")
    assert not is_do("do(")
    assert not is_do("do)")
    
    ans = star1("example.txt")
    print(f"example star 1: {ans}")
    assert ans == 161, f"wrong answer: {ans}"
    
    ans = star2("example2.txt")
    print(f"example star 2: {ans}")
    assert ans == 48, f"wrong answer: {ans}"

if __name__ == "__main__":
    tests()
    
    ans = star1("input.txt")
    print(f"star 1: {ans}")
    assert ans == 173731097

    ans = star2("input.txt")
    print(f"star 2: {ans}")
    assert ans == 93729253