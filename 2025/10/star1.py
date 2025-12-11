from pathlib import Path
from collections import deque


def get_input(filename):
    script_dir = Path(__file__).parent
    lines = []
    with open(script_dir / filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def bfs(start_lights, buttons, target_lights) -> int:
    target_lights = tuple(target_lights)
    start = 0
    visited = set()
    start = (
        start_lights,  # light state
        tuple([0 for i in range(len(buttons))])  # number of presses of each button (first button, second button etc.)
    )
    queue = deque([start])
    # result = []
    
    visited.add(start)
    
    while queue:
        node = queue.popleft()
        # result.append(node)

        for idx, button in enumerate(buttons):
            # press button once
            new_lights = list(node[0])
            for j in button:  # idx of light to turn on
                new_lights[j] = not new_lights[j]  # invert light
            
            new_presses = list(node[1])
            new_presses[idx] += 1  # pressed button idx once
            neighbor = (tuple(new_lights), tuple(new_presses))

            if neighbor[0] == target_lights:
                return sum(neighbor[1])
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    raise RuntimeError()


def find_fewest_presses(line) -> int:
    elements = line.split(" ")
    lights = elements[0].strip("[").strip("]")
    buttons = elements[1:-1]
    # joltage = elements[-1]
    
    start_lights = tuple([False for i in lights])
    target_lights = []
    for light in lights:
        if light == ".":
            target_lights.append(False)
        else:
            target_lights.append(True)

    for i in range(len(buttons)):
        buttons[i] = [int(d) for d in buttons[i].strip("(").strip(")").split(",")]

    return bfs(start_lights, buttons, target_lights)


def aoc(filename):
    lines = get_input(filename)
    ans = 0
    biggest = 0
    for line in lines:
        presses = find_fewest_presses(line)
        if presses > biggest:
            biggest = presses
        ans += presses

    print(f"{biggest = }")
    return ans
        

def tests():
    assert find_fewest_presses("[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}") == 2
    assert find_fewest_presses("[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}") == 3
    assert find_fewest_presses("[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}") == 2

    ans = aoc("example.txt")
    print(f"example: {ans}")
    assert ans == 7, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"{ans = }")
