digits = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

def check_if_number(line, i, second_star=False):
    # check if character is a number
    if line[i].isdigit():
        return line[i]

    if second_star:
        # check if substring is a number
        for key in digits:
            if i+len(key) > len(line):
                continue
            if line[i:i+len(key)] == key:
                return digits[key]
    
    return None

def find_first_number(line, second_star=False):
    for i in range(len(line)):
        maybe_code = check_if_number(line, i, second_star)
        if maybe_code is not None:
            return maybe_code
    
    raise RuntimeError("No number found in line")

def find_last_number(line, second_star=False):
    # regular loop
    for i in range(len(line)):
        maybe_code = check_if_number(line, i, second_star)
        if maybe_code is not None:
            code = maybe_code
        
    return code

def find_code(line, second_star=False):
    code = ""
    code += find_first_number(line, second_star)
    code += find_last_number(line, second_star)
    assert code.isdigit()
    assert len(code) == 2
    return code

def main(filename, first_star=True):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    sum = 0
    for line in lines:
        if first_star:
            code = find_code(line)
        else:
            code = find_code(line, second_star=True)
        int_code = int(code)
        sum += int_code

    return sum

def check_if_number2(line, i):
    check_if_number(line, i, second_star=True)

def find_first_number2(line):
    find_first_number(line, second_star=True)
    
def find_last_number2(line):
    find_last_number(line, second_star=True)

def find_code2(line):
    find_code(line, second_star=True)

def run_tests():
    assert(check_if_number2("one23", 0) == "1")
    assert(check_if_number2("1two3", 0) == "1")
    assert(check_if_number2("1two3", 1) == "2")
    assert(check_if_number2("abc1def", 3) == "1")
    assert(check_if_number2("six8b32csscsdgjsevenfivedlhzhc", 0) == "6")
    
    assert(find_first_number2("notanum8b32csscsdgjsevenfivedlhzhc") == "8")
    assert(find_first_number2("six8b32csscsdgjsevenfivedlhzhc") == "6")
    assert(find_first_number2("feightwo4twofivefour") == "8")
    assert(find_first_number2("bgtwonedrmc35") == "2")
    assert(find_first_number2("twone") == "2")
    assert(find_first_number2("eightwo") == "8")
    assert(find_first_number2("adsfsdfeightwo") == "8")
    assert(find_first_number2("234eightwo") == "2")
    assert(find_first_number2("71six") == "7")
    
    assert(find_last_number2("123") == "3")
    assert(find_last_number2("12three") == "3")
    assert(find_last_number2("12three4") == "4")
    assert(find_last_number2("12threegarbage") == "3")
    assert(find_last_number2("six8b32csscsdgjsevenfivedlhzhc") == "5")
    assert(find_last_number2("bgtwonedrmc35") == "5")
    assert(find_last_number2("twone") == "1")
    assert(find_last_number2("eightwo") == "2")
    assert(find_last_number2("123eightwo") == "2")
    assert(find_last_number2("123eightwofdgdf") == "2")
    assert(find_last_number2("123eightwo123") == "3")
    assert(find_last_number2("71six") == "6")
    assert(find_last_number2("pjbgbnine1rphbcrhgnine2") == "2")
    assert(find_last_number2("pjbgbnine1rphbcrhg2nine") == "9")
    assert(find_last_number2("pjbgbnine1rphbcrhg2nineabv") == "9")
    
    assert(find_last_number2("one") == "1")
    assert(find_last_number2("two") == "2")
    assert(find_last_number2("three") == "3")
    assert(find_last_number2("four") == "4")
    assert(find_last_number2("five") == "5")
    assert(find_last_number2("six") == "6")
    assert(find_last_number2("seven") == "7")
    assert(find_last_number2("eight") == "8")
    assert(find_last_number2("nine") == "9")
    assert(find_last_number2("zero") == "0")
    
    assert(find_first_number2("one") == "1")
    assert(find_first_number2("two") == "2")
    assert(find_first_number2("three") == "3")
    assert(find_first_number2("four") == "4")
    assert(find_first_number2("five") == "5")
    assert(find_first_number2("six") == "6")
    assert(find_first_number2("seven") == "7")
    assert(find_first_number2("eight") == "8")
    assert(find_first_number2("nine") == "9")
    assert(find_first_number2("zero") == "0")
    
    assert(find_code2("one") == "11")
    assert(find_code2("twone") == "21")
    assert(find_code2("eightwo") == "82")
    assert(find_code2("123eightwo") == "12")
    assert(find_code2("123eightwo123") == "13")
    assert(find_code2("96twoseven") == "97")
    assert(find_code2("1bjgnlhtxgx") == "11")
    assert(find_code2("87ninenjhxpnrhljkvnms3") == "83")
    assert(find_code2("123eightwofdfdf") == "12")

if __name__ == "__main__":
    # run_tests()

    example = main("example.txt")
    print(f'Example: {example}')
    assert example == 142, "example.txt failed"

    print(f'First star: {main("input.txt")}')
    assert(main("input.txt", first_star=True) == 54239)
    
    print(f'Second star: {main("input.txt", first_star=False)}')
    assert(main("input.txt", first_star=False) == 55343)

    
# 50129 too low
# 423871440 too high
# 54239
