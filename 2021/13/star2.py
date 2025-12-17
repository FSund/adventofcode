from pathlib import Path
from typing import List, Dict, Any
from collections import defaultdict


def get_input(filename):
    script_dir = Path(__file__).parent
    lines = []
    with open(script_dir / filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def fold_x(dots, x_fold, shape):
    new_shape = (x_fold, shape[1])
    
    keys = list(dots.keys())  # make copy of keys since dots changes in the loop
    for dot in keys:
        (x, y) = (dot.real, dot.imag)
        if x > x_fold:
            dx = x - x_fold  # distance from fold to dot
            assert dx > 0
            new_x = x_fold - dx
            dots[complex(new_x, y)] = 1
            dots.pop(dot)

    return new_shape

def fold_y(dots, y_fold, shape):
    new_shape = (shape[0], y_fold)
    
    keys = list(dots.keys())  # make copy of keys since dots changes in the loop
    for dot in keys:
        (x, y) = (dot.real, dot.imag)
        if y > y_fold:
            dy = y - y_fold  # distance from fold to dot
            assert dy > 0
            new_y = y_fold - dy
            dots[complex(x, new_y)] = 1
            dots.pop(dot)

    return new_shape


def aoc(filename):
    lines = get_input(filename)
    
    # dots = defaultdict(lambda: None)
    dots = defaultdict(int)
    folds = []
    shape = [0, 0]
    for line in lines:
        if "fold" in line:
            folds.append(line)
        elif line != "":
            x, y = line.split(",")
            x = int(x)
            y = int(y)
            dots[complex(x, y)] = 1

            # update shape
            shape[0] = max(x, shape[0])
            shape[1] = max(y, shape[1])
            
    shape = (shape[0]+1, shape[1]+1)
    # folds = [folds[0]]
    for fold in folds:
        val = int(fold.split("=")[-1])
        if "x" in fold:
            shape = fold_x(dots, val, shape)
            assert shape[0] == val
        else:
            shape = fold_y(dots, val, shape)

        for dot in dots.keys():
            assert dot.real < shape[0]
            assert dot.imag < shape[1]

    lines = []
    for x in range(shape[1]):
        lines.append(["."] * shape[0])

    for dot in dots.keys():
        x, y = (dot.real, dot.imag)
        x = int(x)
        y = int(y)
        lines[y][x] = "#"

    for line in lines:
        print("".join(line))


if __name__ == "__main__":
    ans = aoc("input.txt")
    print(f"{ans = }")