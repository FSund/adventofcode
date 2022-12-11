from math import floor

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

lines = []
with open("input.txt") as file:
    for line in file:
        lines.append(line.strip("\n"))

class Monkey:
    # primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]
    def __init__(self, starting_items, operation, test, true, false):
        self.items = starting_items
        self.operation = operation.split("=")[1]
        self.divisor = int(test.strip("divisible by "))
        self.true_destination = int(true.strip("throw to monkey "))
        self.false_destination = int(false.strip("throw to monkey "))
        self.inspections = 0
    
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
            
            # print(self.items[i])
            # reduce angst
            for prime in self.primes:
                if self.items[i] < prime:
                    break

                quotient, remainder = divmod(self.items[i], prime)
                while remainder == 0 and remainder > 1:
                    self.items[i] = quotient
                    quotient, remainder = divmod(self.items[i], prime)
                
                # quotient = number // divisor
                # quotient, remainder = divmod(self.items[i], prime)
                # while remainder == 0:
                #     self.items[i] = quotient
                #     quotient, remainder = divmod(self.items[i], prime)

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
