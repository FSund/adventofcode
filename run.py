from math import floor

lines = []
with open("input.txt") as file:
    for line in file:
        lines.append(line.strip("\n"))

class Item:
    def __init__(self, value):
        # self.value = value
        self.factors = {}
        self.factors[1] = value
    
    def multiply_self(self):
        self.factors[1] *= 2
    
    def add_factor(self, factor):
        if factor not in self.factors:
            self.factors[factor] = 0
        self.factors[factor] += 1

    def is_divisible_by(self, number):
        if self.factors[1] % number == 0:
            return True
        else:
            return False
            

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
            if "*" in self.operation:
                factor = self.operation.split(" * ")[1]
                if factor == "old":
                    self.items[i].multiply_self()
                else:
                    self.items[i].add_factor(int(factor))
            else:
                value = int(self.operation.split(" + ")[1])
                self.items[i].factors[1] += value

            # self.items[i] = floor(self.items[i] / 3.0)  # ignore for star 2
            
            # self.items[i].value = eval(self.operation)
            
            self.inspections += 1

    # def test_items(self, items):
    #     for item in items:
    #         if item % self._test != 0:
    #             return False
    #     return True

    # def divide_items(self, factor):
    #     for i in range(len(self.items)):
    #         self.items[i] /= factor

    def test(self, monkeys):
        for i in reversed(range(len(self.items))):
            test = self._test
            item = self.items[i]
            # value = item.value
            if item.is_divisible_by(test):
                monkeys[self.true].items.append(item)
            else:
                monkeys[self.false].items.append(item)
            self.items.pop(i)

monkeys = []

# starting conditions
i = 0
while i < len(lines):
    items = lines[i+1].split()[2:]
    items = [Item(int(item.strip(","))) for item in items]
    operation = lines[i+2].split(": ")[1]
    test = lines[i+3].split(": ")[1]
    true = lines[i+4].split(": ")[1]
    false = lines[i+5].split(": ")[1]
    monkeys.append(Monkey(items, operation, test, true, false))
    
    i += 7

# divide worry level by 3 (and round down to nearest int) after inspection (before test)

def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

# mult = 1
# for monkey in monkeys:
#     mult *= monkey._test

for i in range(20):
    for monkey in monkeys:
        monkey.inspect()
        monkey.test(monkeys)

print(monkeys[0].items[0].factors)

# items = []
# for monkey in monkeys:
#     items += monkey.items

# for item in items:
#     print(prime_factors(item))
        


# print(monkeys[0].items[0])

inspections = [monkey.inspections for monkey in monkeys]
print(inspections)
# inspections.sort()
# print(inspections[-1] * inspections[-2])  # 110888
