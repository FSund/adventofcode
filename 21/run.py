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


if __name__ == "__main__":
    assert(star1("example.txt") == 152)
    
    print(star1("input.txt"))