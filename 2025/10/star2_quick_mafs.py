from pathlib import Path
import numpy as np
import sympy as sp
from scipy.optimize import milp, LinearConstraint, Bounds


def get_input(filename):
    script_dir = Path(__file__).parent
    lines = []
    with open(script_dir / filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def verify_result(line, presses):
    elements = line.split(" ")
    # lights = elements[0].strip("[").strip("]")
    buttons = elements[1:-1]
    joltage = elements[-1].strip("{").strip("}")
    n = len(joltage.split(","))

    start = [0 for i in range(n)]
    start = np.asarray(start)
    target = [int(j) for j in joltage.split(",")]
    target = np.asarray(target)

    for i in range(len(buttons)):
        buttons[i] = [int(d) for d in buttons[i].strip("(").strip(")").split(",")]
    
    button_effects = []
    for button in buttons:
        effect = [0 for i in range(n)]
        for idx in button:
            effect[idx] += 1

        button_effects.append(effect)

    button_effects = np.asarray(button_effects)

    for idx, count in enumerate(presses):
        start += button_effects[idx] * count

    assert np.all(start == target)



def find_fewest_presses(line, return_presses=False) -> int:
    elements = line.split(" ")
    # lights = elements[0].strip("[").strip("]")
    buttons = elements[1:-1]
    joltage = elements[-1].strip("{").strip("}")
    n = len(joltage.split(","))

    start = [0 for i in range(n)]
    start = np.asarray(start)
    target = [int(j) for j in joltage.split(",")]
    target = np.asarray(target)

    for i in range(len(buttons)):
        buttons[i] = [int(d) for d in buttons[i].strip("(").strip(")").split(",")]
    
    button_effects = []
    for button in buttons:
        effect = [0 for i in range(n)]
        for idx in button:
            effect[idx] += 1

        button_effects.append(effect)

    button_effects = np.asarray(button_effects)

    if False:
        A = button_effects.transpose()
        b = target
        x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
    
    elif False:
        A = sp.Matrix(button_effects.transpose())
        b = sp.Matrix(target)

        # Solve symbolically (gives exact rationals)
        x = A.pinv() @ b  # Moore-Penrose pseudoinverse

        print(f"Exact rational solution: {x}")

    else:
        A = button_effects.transpose()
        b = target
        c = np.ones(A.shape[1])  # coefficients for objective function

        # Constraint: Ax = b
        constraints = LinearConstraint(A, b, b)
        bounds = Bounds(lb=0, ub=np.inf)

        # All variables are integers
        # integrality = np.ones(A.shape[1])  # 1 = integer, 0 = continuous
        integrality = 3

        result = milp(c=c, constraints=constraints, bounds=bounds, integrality=integrality)

        if result.success:
            # print(f"{result.x=}")
            x = np.round(result.x).astype(int)
            # print(f"Solution: x = {x}")
            # print(f"Verification: Ax = {A @ x}")

            if result.status != 0:
                print("NON OPTIMAL")

            
            verify_result(line, x)

            if return_presses:
                return x
            else:
                return sum(x)
        else:
            # print("No integer solution found")

            raise RuntimeError()


def aoc(filename):
    lines = get_input(filename)
    ans = 0
    for line in lines:
        presses = find_fewest_presses(line)
        # print(f"{presses = }")
        ans += presses

    return ans


def tests():
    line = "[#....#...#] (0,1,3,4,6,7,8) (0,2,3,4,5,6,7) (0,1,2,3,4,5,8,9) (1,2,3,4,6,7,8,9) (0,1,2,3,6,7) (0,2,5,9) (3,7,9) (0,1,2,3,4,5,8) (2) (6,8,9) (0,2,4,5,6) (1,6,8,9) (2,3,4,6,7,8,9) {77,44,104,72,76,57,91,60,51,44}"
    presses = find_fewest_presses(line, True)
    verify_result(line, presses)


    line = "[#...#.####] (1,3,4,6,8) (0,1,4,5,6,9) (1,5,6) (3,4,5,8) (0,1,2,3,5,6,8,9) (0,2,3,9) (0,1,2,3,5,7,9) (0,2,4,5,7,8,9) (0,1,5,7,8) {58,53,44,44,10,63,26,32,38,44}"
    presses = find_fewest_presses(line, True)
    verify_result(line, presses)


    assert find_fewest_presses("[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}") == 10
    assert find_fewest_presses("[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}") == 12
    assert find_fewest_presses("[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}") == 11

    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 33, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
    # 15117 is too low
