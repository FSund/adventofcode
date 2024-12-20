import operator


def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def get_combo(operand: int, A: int, B: int, C: int):
    if 0 <= operand <= 3:
        return operand
    elif operand == 4:
        return A
    elif operand == 5:
        return B
    elif operand == 6:
        return C
    else:
        raise ValueError("operand out of range")


def run_program(program, A, B, C):
    out = []
    ip = 0
    while ip < len(program):
        opcode = program[ip]
        operand = program[ip+1]
        literal_operand = operand
        combo_operand = get_combo(operand, A, B, C)
        increase_ip = True
        if opcode == 0:
            # adv
            A = int(A / (2**combo_operand))
        elif opcode == 1:
            # bxl
            B = operator.xor(B, literal_operand)
        elif opcode == 2:
            # bst
            B = combo_operand % 8
        elif opcode == 3:
            # jnz
            if A != 0:
                ip = literal_operand
                increase_ip = False
        elif opcode == 4:
            # bxc
            B = operator.xor(B, C)
        elif opcode == 5:
            # out
            out.append(combo_operand % 8)
        elif opcode == 6:
            # bdv -- same as adv but stored in B
            B = int(A / (2**combo_operand))
        elif opcode == 7:
            # cdv -- same as adv but stored in C
            C = int(A / (2**combo_operand))
        
        if increase_ip:
            ip += 2
    
    return out


def find_bits(idx, program, A, B0, C0, options):
    for jj in range(0b111+1):
        out = run_program(program, A, B0, C0)
        if out[0] == program[idx]:
            # print(f"A = {A} = {A:b}, {out = }")
            if idx == 0:
                print(f"A = {A} = {A:b}, {out = }")
                options.append(A)
            else:
                find_bits(idx-1, program, A << 3, B0, C0, options)

        A += 1

def aoc(filename):
    lines = get_input(filename)
    
    # A0 = int(lines[0].split(": ")[1])
    B0 = int(lines[1].split(": ")[1])
    C0 = int(lines[2].split(": ")[1])
    program = [int(x) for x in lines[4].split(": ")[1].split(",")]
    program = tuple(program)
    
    A = 0b000
    options = []
    find_bits(len(program) - 1, program, A, B0, C0, options)

    return min(options)

def tests():
    lines = get_input("example2.txt")
    A0 = int(lines[0].split(": ")[1])
    B0 = int(lines[1].split(": ")[1])
    C0 = int(lines[2].split(": ")[1])
    program = [int(x) for x in lines[4].split(": ")[1].split(",")]
    out = run_program(program, 117440, B0, C0)
    print(f"{out = } == {program = }")
    assert out == program
    
    ans = aoc("example2.txt")
    print(f"example star 1: {ans}")
    assert ans == 117440, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
