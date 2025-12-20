import math
from math import lcm, gcd
import numpy as np
from scipy.optimize import linprog
import numpy.typing as npt


def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def parse_input(lines):
    machines = []
    button_a = {"x": 0, "y": 0}
    button_b = {"x": 0, "y": 0}
    prize = {"x": 0, "y": 0}
    for line in lines:
        if "Button A" in line:
            left, right = line.split(", ")
            left =  left.split(": ")[1]
            button_a["x"] = int(left.strip("X"))
            button_a["y"] = int(right.strip("Y"))
        elif "Button B" in line:
            left, right = line.split(", ")
            left =  left.split(": ")[1]
            button_b["x"] = int(left.strip("X"))
            button_b["y"] = int(right.strip("Y"))
        elif "Prize" in line:
            left, right = line.split(", ")
            left =  left.split(": ")[1]
            prize["x"] = int(left.strip("X="))
            prize["y"] = int(right.strip("Y="))
        else:
            assert line == "\n" or line == ""
            machines.append(
                {"button_a": button_a, "button_b": button_b, "prize": prize}
            )
            button_a = {"x": 0, "y": 0}
            button_b = {"x": 0, "y": 0}
            prize = {"x": 0, "y": 0}
    
    # don't forget the last machine
    machines.append(
        {"button_a": button_a, "button_b": button_b, "prize": prize}
    )
    return machines
        

def prime_factors(n):
    # brute force prime factorization
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


def minimize(a_x, b_x, a_y, b_y, x, y, star2=False):
    # Set up the matrices
    A = np.array([
        [a_x, b_x],  # x coefficients for buttons A and B
        [a_y, b_y],  # y coefficients for buttons A and B
    ])
    
    b = np.array([x, y])      # target x,y coordinates
    
    # Cost coefficients (3 tokens for A, 1 token for B)
    c = np.array([3, 1])
    
    # Use linear programming to minimize cost
    result = linprog(
        c,       # minimize these coefficients
        A_eq=A,   # equality constraints matrix
        b_eq=b,   # equality constraints vector
        bounds=(0, None),  # bounds for x and y
        method="highs",  # force method "highs" which uses the integrality option
        integrality=1,    # force integer solutions
        options={
            "autoscale": True,
        }
    )
    
    if star2 and result.status != 0:
        print(result)
        raise ValueError(f"Linear programming failed with status {result.status} ({result.message})")
    elif result.success:
        # Round up to nearest integers since we need whole button presses
        # print(result)
        n_a = int(round(result.x[0], 0))
        n_b = int(round(result.x[1], 0))
        cost = 3*n_a + 1*n_b
        print(f"{n_a = }, {n_b = }, {cost = }")
        return cost
    else:
        return 0  # No solution found


def compute_tokens_consumed(
    a_x: int, b_x: int, a_y: int, b_y: int, x: int, y: int
) -> int:
    eq_a = np.array([
        [a_x, b_x],
        [a_y, b_y]
    ])
    eq_prize = np.array([x, y])
    
    sol = np.linalg.solve(eq_a, eq_prize)
    n_a, n_b = sol
    n_a, n_b = round(n_a), round(n_b)

    px_approx = n_a * a_x + n_b * b_x
    py_approx = n_a * a_y + n_b * b_y

    if px_approx == x and py_approx == y:
        return n_a * 3 + n_b

    return 0


def get_minimum_cost(machine, star2=False):
    # these machines have two buttons labeled A and B.
    # it costs 3 tokens to push the A button and 1 token to push the B button
    
    # each button would need to be pressed no more than 100 times
    
    # do prime factorization to find the minimum number of tokens required
    # to push both buttons
    
    a_x = machine["button_a"]["x"]
    a_y = machine["button_a"]["y"]
    b_x = machine["button_b"]["x"]
    b_y = machine["button_b"]["y"]

    x = machine["prize"]["x"]
    y = machine["prize"]["y"]
    
    return compute_tokens_consumed(a_x, b_x, a_y, b_y, x, y)

    # return minimize(a_x, b_x, a_y, b_y, x, y, star2)
    
    cost_a_press = 3
    cost_b_press = 1
    
    # cost per x movement
    cost_x_a = 3/a_x
    cost_x_b = 1/b_x
    
    # cost per y movement
    cost_y_a = 3/a_y
    cost_y_b = 1/b_y
    
    # print(f"{cost_x_a = }")
    # print(f"{cost_x_b = }")
    # print(f"{cost_y_a = }")
    # print(f"{cost_y_b = }")
    
    # print(f"{lcm(a_x, b_x, x)}, {lcm(a_y, b_y, y)}")
    gcd_x = gcd(a_x, b_x, x)
    gcd_y = gcd(a_y, b_y, y)
    print(f"{gcd_x = }, {gcd_y = }")
    print(f"{gcd(a_x, x)}")
    print(f"{gcd(b_x, x)}")
    
    common_divisor = gcd_x * gcd_y
    print(f"{x/common_divisor}, {y/common_divisor}")
    n_x = int(x/common_divisor)
    n_y = int(y/common_divisor)
    
    x_primes = prime_factors(x)
    y_primes = prime_factors(y)
    print(f"{x_primes = }")
    print(f"{y_primes = }")
    print(f"a_x: {prime_factors(a_x)}")
    print(f"b_x: {prime_factors(b_x)}")
    print(f"a_y: {prime_factors(a_y)}")
    print(f"b_y: {prime_factors(b_y)}")
    
    # if n_x > x or n_y > y:
    #     return 0
    
    # x_primes = prime_factors(x)
    # y_primes = prime_factors(y)
    
    # for x_prime in x_primes:
    #     print(f"lcm x: {lcm(a_x, b_x, x_prime)}")
    #     if lcm(a_x, b_x, x_prime) > x:
    #         return 0

    # for y_prime in y_primes:
    #     print(f"lcm y: {lcm(a_y, b_y, y_prime)}")
    #     if lcm(a_y, b_y, y_prime) > y:
    #         return 0
    
    # print(f"")

    return minimize(a_x, b_x, a_y, b_y, x, y)


def aoc(filename, star2=False):
    lines = get_input(filename)
    machines = parse_input(lines)
    
    cost = 0
    for machine in machines:
        if star2:
            machine["prize"]["x"] += 10000000000000
            machine["prize"]["y"] += 10000000000000
        cost += get_minimum_cost(machine, star2)
        
    return cost


def tests():
    lines = get_input("example.txt")
    machines = parse_input(lines)
    
    assert get_minimum_cost(machines[2]) == 200
    assert get_minimum_cost(machines[0]) == 280
    
    # machine 1 from example should have no valid combination of A and B presses
    assert get_minimum_cost(machines[1]) == 0
    assert get_minimum_cost(machines[3]) == 0
    
    ans = aoc("example.txt")
    print(f"example star 1: {ans}")
    assert ans == 480, f"wrong answer: {ans}"
    
    # ans = aoc("example.txt", star2=True)
    # print(f"example star 2: {ans}")
    # assert ans == 1206, f"wrong answer: {ans}"
    
    for machine in machines:
        machine["prize"]["x"] += 10000000000000
        machine["prize"]["y"] += 10000000000000
    
    assert get_minimum_cost(machines[0]) == 0
    assert get_minimum_cost(machines[1]) > 0
    assert get_minimum_cost(machines[2]) == 0
    assert get_minimum_cost(machines[3]) > 0


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"star 1: {ans}")
    assert ans == 26810
    
    ans = aoc("input.txt", star2=True)
    print(f"star 2: {ans}")
    # 71922170897884 too low
    # assert ans == 1344
