from sympy import symbols, linsolve, parse_expr


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

    monkeys = {}
    for l in lines:
        lhs, rhs = l.split(':')
        monkeys[lhs] = rhs.strip()

    x = symbols('x')

    def find_val(monkey):
        val = monkeys[monkey]
        try:
            # string to int
            int(val)
            return val
        except ValueError:
            if val == 'x':
                return 'x'

            c1, _, c2 = val.split()
            v1 = find_val(c1)
            v2 = find_val(c2)
            res = val.replace(c1, v1).replace(c2, v2)

            return f'({res})'

    monkeys['root'] = monkeys['root'].replace('+', '==')
    monkeys['humn'] = 'x'
    
    e1 = find_val(monkeys['root'].split()[0])
    e2 = find_val(monkeys['root'].split()[2])

    expr = parse_expr(f"Eq({e1}, {e2})")
    sols = linsolve([expr], [x])
    
    return sols.args[0][0]


if __name__ == "__main__":
    assert(star1("21/example.txt") == 152)
    assert(star1("21/input.txt") == 169525884255464)
    print(f'star 1: {star1("21/input.txt")}')

    assert(star2("21/example.txt") == 301)
    assert(star2("21/input.txt") == 3247317268284)
    print(f'star 2: {star2("21/input.txt")}')
