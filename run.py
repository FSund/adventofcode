from math import floor
from aoc import *

# primes_to_keep = [2, 3, 5, 7, 11, 13, 17, 19, 23]

lines = []
with open("input.txt") as file:
    for line in file:
        lines.append(line.strip("\n"))


class Monkey:
    # primes_to_keep = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    # primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]
    monkey_divisors = []
    monkey_factor = 1
    def __init__(self, starting_items, operation, test, true, false):
        self.items = starting_items
        self.operation = operation.split("=")[1]
        self.divisor = int(test.strip("divisible by "))
        Monkey.monkey_divisors.append(self.divisor)
        Monkey.monkey_divisors.sort()
        Monkey.monkey_factor *= self.divisor
        self.true_destination = int(true.strip("throw to monkey "))
        self.false_destination = int(false.strip("throw to monkey "))
        self.inspections = 0
    
    def _find_factor(self, n):
        factors = prime_factors(n)
        
        if n in factors:
            factors.pop(factors.index(n))

        for a in self.monkey_divisors:
            if factors.count(a):
                factors.pop(factors.index(a))
        
        factor = 1
        for f in factors:
            factor *= f

        return factor
    
    def inspect(self):
        for i in range(len(self.items)):
            old = self.items[i]
            self.items[i] = eval(self.operation)
            # self.items[i] = floor(self.items[i] / 3.0)
                    
            self.inspections += 1

    def test(self, monkeys):
        for i in reversed(range(len(self.items))):
            # item = self.items[i]
            if self.items[i] % self.divisor == 0:
                to = self.true_destination
            else:
                to = self.false_destination
            
            # factors = get_repeated_prime_factors(self.items[i])
            # factor = list_prod(factors)
            # if not self.items[i] % factor == 0:
            #     raise RuntimeError
            # self.items[i] = self.items[i] // factor
            
            if self.items[i] > Monkey.monkey_factor**2:
                factor = self._find_factor(self.items[i])
                self.items[i] = self.items[i] // factor
            
            if to == self.true_destination:
                assert(self.items[i] % self.divisor == 0)

            # to = int(op.strip("throw to monkey "))
            monkeys[to].items.append(self.items[i])
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

print(f"{Monkey.monkey_divisors=}")
print(f"{Monkey.monkey_factor=}")

# == After round 20 ==
# Monkey 0 inspected items 99 times.
# Monkey 1 inspected items 97 times.
# Monkey 2 inspected items 8 times.
# Monkey 3 inspected items 103 times.

n = 20
print(f"n = {n}")
for i in range(n):
    # print(monkeys[0].items)
    for monkey in monkeys:
        monkey.inspect()
        monkey.test(monkeys)

items = []
for monkey in monkeys:
    items += monkey.items

print(f"items: {items}")
print(f"max(items): {max(items)}")

inspections = [monkey.inspections for monkey in monkeys]
print(f"inspections: {inspections}")
inspections.sort()
print(inspections[-1] * inspections[-2])
