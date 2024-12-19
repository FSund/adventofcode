import operator
import numpy as np
import matplotlib.pyplot as plt
import numpy.typing as npt
from queue import PriorityQueue
from typing import Tuple


def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def aoc(filename):
    lines = get_input(filename)
    
    A = int(lines[0].split(": ")[1])
    B = int(lines[1].split(": ")[1])
    C = int(lines[2].split(": ")[1])
    
    def get_combo(operand: int):
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
    
    program = [int(x) for x in lines[4].split(": ")[1].split(",")]
    
    out = []
    ip = 0
    while ip < len(program):
        opcode = program[ip]
        operand = program[ip+1]
        literal_operand = operand
        combo_operand = get_combo(operand)
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
    
    return ",".join([str(o) for o in out])
    


def tests():
    ans = aoc("example.txt")
    print(f"example star 1: {ans}")
    assert ans == "4,6,3,5,6,3,5,2,1,0", f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"star 1: {ans}")
