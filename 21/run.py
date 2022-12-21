from sympy import symbols, linsolve, pprint, nsimplify, nonlinsolve
import sys

def get_input(filename="input.txt"):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))
    return lines


class Monkey:
    def __init__(self, value=None, operation=None, parts=None):
        self.value = value
        self.operation = operation
        self.parts = parts


def star1(filename):
    lines = get_input(filename)
    
    monkeys = {}
    
    for line in lines:
        left, right = line.split(": ")
        if right.isdigit():
            monkeys[left] = Monkey(value=int(right))
        else:
            right = right.split(" ")
            operation = right[1]
            parts = [right[0], right[2]]
            monkeys[left] = Monkey(operation=operation, parts=parts)
    
    while monkeys["root"].value is None:
        for name in monkeys.keys():
            if monkeys[name].value is not None:
                continue

            p1 = monkeys[name].parts[0]
            p2 = monkeys[name].parts[1]
            if monkeys[p1].value is not None and monkeys[p2].value is not None:
                left = monkeys[p1].value
                right = monkeys[p2].value
                op = monkeys[name].operation
                monkeys[name].value = int(eval(f"{left}{op}{right}"))

    return monkeys["root"].value


def star2(filename):
    lines = get_input(filename)
    
    # build up equation, solve using SymPy
    syms = []
    eqs = []
    
    for line in lines:
        left, right = line.split(": ")
        if left == "root" or left == "humn":
            continue
            
        x = symbols(f'{left}')
        syms.append(x)

        if right.isdigit():
            eqs.append(eval(f"x - {right}"))
        else:
            right = right.split(" ")
            operation = right[1]
            
            y = symbols(f'{right[0]}')
            z = symbols(f'{right[2]}')
            eqs.append(eval(f"y {operation} z - x"))

    # add "root" equation
    x = symbols('pppw')
    y = symbols('sjmn')
    eqs.append(x - y)
    
    # add "humn" to the end
    humn = symbols('humn')
    syms.append(humn)

    eqs = [nsimplify(i, rational=1) for i in eqs]
    # print(eqs)
    
    # for eq in eqs:
    #     print(eq)
    # print(syms)
    # pprint(linsolve([eqs[1]], symbols("dbpl")))
    
    # print(linsolve(eqs, syms))
    sols = nonlinsolve(eqs, syms)
    # breakpoint()
    # print(sols.args[0][-1])
    
    return sols.args[0][-1]
    
    # monkeys = {}
    
    # for line in lines:
    #     left, right = line.split(": ")
    #     if right.isdigit():
    #         monkeys[left] = Monkey(value=int(right))
    #     else:
    #         right = right.split(" ")
    #         operation = right[1]
    #         parts = [right[0], right[2]]
    #         monkeys[left] = Monkey(operation=operation, parts=parts)
    
    
    # while monkeys["root"].value is None:
    #     for name in monkeys.keys():
    #         if monkeys[name].value is not None:
    #             continue

    #         p1 = monkeys[name].parts[0]
    #         p2 = monkeys[name].parts[1]
    #         if monkeys[p1].value is not None and monkeys[p2].value is not None:
    #             left = monkeys[p1].value
    #             right = monkeys[p2].value
    #             op = monkeys[name].operation
    #             monkeys[name].value = int(eval(f"{left}{op}{right}"))

    # return monkeys["root"].value
    


if __name__ == "__main__":
    assert(star1("example.txt") == 152)
    
    print(star1("input.txt"))
    
    assert(star2("example.txt") == 301)
    
    sys.setrecursionlimit(3000)
    print(star2("input.txt"))
