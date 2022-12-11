from math import floor

lines = []
with open("input.txt") as file:
    for line in file:
        lines.append(line.strip("\n"))

# class :

# class Factors:
#     def __init__(self, factors=None):
#         if factors:
#             self.factors = factors
#         else:
#             self.factors = {}
#             for f in [1, 2, 3, 5, 7, 11, 13, 17, 19]:
#                 self.factors[f] = 0
    
#     def add(self, value):
#         self.factors[1] += value
    
#     def multiply(self, value):
#         self.factors[value] += 1
#         self.factors[1] *= 
    
#     def multiply_with_factors(self, factors):
#         for key in self.factors.keys():
#             self.factors[key] += factors[key]

class Product:
    primes = [1, 2, 3, 5, 7, 11, 13, 17, 19, 23]
    max_prime = max(primes)
    def __init__(self, value):
        # 1, 2, 3, 5, 7, 11, 13, 17, 19, and 23
        self.factors = [0 for i in range(self.max_prime+1)]
        self.factors[1] = value
    
    def multiply(self, number):
        self.factors[number] += 1
    
    def _get_value(self):
        value = 1
        for prime in self.primes:
            if self.factors[prime]:
                value *= prime*self.factors[prime]
        return value
    
    def is_divisible_by(self, number):
        if self.factors[number] > 0:
            return True
        if self.factors[1] % number:
            return True
        return False

a = Product(79)
print(a._get_value())
a.multiply(2)
print(a._get_value())
a.multiply(5)
print(a._get_value())
a.multiply(2)
print(a._get_value())
a.multiply(23)
print(a._get_value())

print(15*2*5*2*23)
print(a.is_divisible_by(5))
print(a.is_divisible_by(23))
print(a.is_divisible_by(2))
# print(a.is_divisible_by(79))


class Item:        
    def __init__(self, value):
        # self.value = value
        # self.factors = {}
        # self.factors[1] = value
        self.elements = [Product(value)]
    
    # def multiply_self(self):
    #     self.factors[1] *= 2
    
    def multiply(self, number):
        for i in range(len(self.elements)):
            self.elements[i].multiply(number)
            
    def add(self, number):
        self.elements.append(Product(number))
    
    def square(self):
        # self.elements += self.elements
        pass

    def is_divisible_by(self, number):
        for element in self.elements:
            if not element.is_divisible_by(number):
                return False
        return True


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
                    self.items[i].square()
                else:
                    self.items[i].multiply(int(factor))
            else:
                value = int(self.operation.split(" + ")[1])
                self.items[i].add(value)

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

# def prime_factors(n):
#     i = 2
#     factors = []
#     while i * i <= n:
#         if n % i:
#             i += 1
#         else:
#             n //= i
#             factors.append(i)
#     if n > 1:
#         factors.append(n)
#     return factors

# mult = 1
# for monkey in monkeys:
#     mult *= monkey._test

for i in range(100):
    for monkey in monkeys:
        monkey.inspect()
        monkey.test(monkeys)

print(len(monkeys[0].items))

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
