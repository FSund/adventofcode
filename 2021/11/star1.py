from pathlib import Path
from typing import List, Dict
from collections import defaultdict


def get_input(filename):
    script_dir = Path(__file__).parent
    lines = []
    with open(script_dir / filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


DIRECTIONS = [1, -1, 1j, -1j, 1+1j, 1-1j, -1+1j, -1-1j]


def flash(pos, octii):
    # return all octopuses that should flash the next round
    assert octii[pos]
    assert octii[pos] > 9

    # octii[pos] = 0
    to_flash = []
    for dir in DIRECTIONS:
        neigh = pos + dir
        if octii[neigh]:  # bounds check
            octii[neigh] += 1
            if octii[neigh] > 9:
                # flash(neigh, octii)
                to_flash.append(neigh)

    return to_flash

def aoc(filename):
    lines = get_input(filename)
    octii = defaultdict(lambda: None)
    for i, line in enumerate(lines):
        for j, energy_level in enumerate(line):
            octii[complex(i, j)] = int(energy_level)

    keys = list(octii.keys())  # store keys since size of octii can change
    ans = 0
    for step in range(100):
        # First, the energy level of each octopus increases by `1`
        to_flash = []
        for pos in keys:
            octii[pos] += 1
            if octii[pos] > 9:
                to_flash.append(pos)

        #
        flashed_this_step = []
        while to_flash:
            new_flash = []
            for pos in to_flash:
                if pos not in flashed_this_step:  # can only flash once per step
                    new_flash += flash(pos, octii)
                    flashed_this_step.append(pos)
            to_flash = new_flash

        ans += len(flashed_this_step)
        for pos in flashed_this_step:
            octii[pos] = 0

    return ans
        

def tests():
    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 1656, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
