from math import floor

lines = []
with open("input.txt") as file:
    for line in file:
        lines.append(line.strip("\n"))

class Monkey:
    def __init__(self, starting_items, operation, test, true, false):
        self.items = starting_items
        self.operation = operation.split("=")[1]
        self._test = int(test.strip("divisible by "))
        self.true = int(true.strip("throw to monkey "))
        self.false = int(false.strip("throw to monkey "))
        self.inspections = 0
    
    def inspect(self):
        for i in range(len(self.items)):
            old = self.items[i]
            self.items[i] = eval(self.operation)
            self.items[i] = floor(self.items[i] / 3.0)
            self.inspections += 1

    def test(self, monkeys):
        for i in reversed(range(len(self.items))):
            test = self._test
            item = self.items[i]
            if item % test == 0:
                monkeys[self.true].items.append(item)
            else:
                monkeys[self.false].items.append(item)
            self.items.pop(i)

monkeys = []

# starting conditions
i = 0
while i < len(lines):
    items = lines[i+1].split()[2:]
    items = [int(item.strip(",")) for item in items]
    operation = lines[i+2].split(": ")[1]
    test = lines[i+3].split(": ")[1]
    true = lines[i+4].split(": ")[1]
    false = lines[i+5].split(": ")[1]
    monkeys.append(Monkey(items, operation, test, true, false))
    
    i += 7

# divide worry level by 3 (and round down to nearest int) after inspection (before test)

for i in range(20):
    for monkey in monkeys:
        monkey.inspect()
        monkey.test(monkeys)

inspections = [monkey.inspections for monkey in monkeys]
inspections.sort()
print(inspections[-1] * inspections[-2])  # 110888
