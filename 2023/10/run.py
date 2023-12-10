import math
import numpy as np
import matplotlib.pyplot as plt

def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))
    return lines

# def get_neighbors(pos):
#     return [
#         (pos[0] + 1, pos[1]), ["|", "L", "J"],
#         (pos[0] - 1, pos[1]), ["|", "7", "F"],
#         (pos[0], pos[1] + 1), ["-", "J", "7"],
#         (pos[0], pos[1] - 1), ["-", "F", "L"],
#     ]

# def is_connected(this, other, lines):
#     # this_symbol = lines[this[0]][this[1]]
#     other_symbol = lines[other[0]][other[1]]
#     for neighbor, accepted_connections in get_neighbors(this):
#         if other == neighbor and other_symbol in accepted_connections:
#             return True
#     return False

def is_valid_connection(delta, other_symbol):
    if delta == (1, 0):
        return other_symbol in ["|", "L", "J"]
    elif delta == (-1, 0):
        return other_symbol in ["|", "7", "F"]
    elif delta == (0, 1):
        return other_symbol in ["-", "J", "7"],
    elif delta == (0, -1):
        return other_symbol in ["-", "F", "L"]
    
    raise Exception("Invalid delta")

def _get_distances(lines, start_deltas):
    lines = [list(line) for line in lines]
    
    # find S
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "S":
                start = (i, j)
                break
    
    pos = (start[0], start[1])
    previous_pos = None
    # neighbors = [
    #     (pos[0] + 1, pos[1]), ["|", "L", "J"],
    #     (pos[0] - 1, pos[1]), ["|", "7", "F"],
    #     (pos[0], pos[1] + 1), ["-", "J", "7"],
    #     (pos[0], pos[1] - 1), ["-", "F", "L"],
    # ]
    symbol_to_delta = {
        "S": start_deltas, # start
        "|": [(-1, 0), (1, 0)],
        "-": [(0, -1), (0, 1)],
        "L": [(-1, 0), (0, 1)],
        "J": [(0, -1), (-1, 0)],
        "7": [(0, -1), (1, 0)],
        "F": [(1, 0), (0, 1)],
    }
    # accepted_transitions = {
    #     "|": ["|", "F", "L", "7" "J"],
    #     "-": ["-", "F", "L", "7" "J"],
    #     "F": ["|", "7", "J"],
    #     "7": ["F", "J"],
    #     "7": ["|", "-"],
    #     "F": ["|", "-"],
    # }
    distances = np.zeros((len(lines), len(lines[0])))
    # sym = lines[pos[0]][pos[1]]
    while True:
        sym = lines[pos[0]][pos[1]]
        for delta in symbol_to_delta[sym]:
            new_pos = (pos[0] + delta[0], pos[1] + delta[1])
            if new_pos[0] < 0 or new_pos[0] >= len(lines) or new_pos[1] < 0 or new_pos[1] >= len(lines[0]):
                # out of bounds
                # print("out of bounds")
                continue
            if distances[new_pos] != 0:
                # skip visited
                continue
            new_sym = lines[new_pos[0]][new_pos[1]]
            if new_sym == ".":
                continue
            if is_valid_connection(delta, new_sym):
                # print(new_pos)
                previous_pos = (pos[0], pos[1])
                pos = (new_pos[0], new_pos[1])
                
                # update map
                distances[pos] = distances[previous_pos] + 1
                
                break
        else:
            # no valid connections (or whole loop visited)
            break
        
    return distances
        

def star1(filename):
    lines = get_input(filename)
    
    # start only has two valid connections (according to the text)
    # try both direction, take minimum of map to get the shortest path
    distances = []
    for start_deltas in [
        [(1, 0), (0, 1)],
        [(0, 1), (1, 0)],
    ]:
        distances.append(_get_distances(lines, start_deltas))
    
    distances = np.array(distances)
    distances = np.min(distances, axis=0)
    
    return int(np.max(distances))


def tests():
    # is_connected((0, 0), (0, 1), ["|", "L", "J"])
    pass

if __name__ == "__main__":
    tests()

    example = star1("example.txt")
    print(f'Example: {example}')
    assert(example == 8)
    
    print(f'First star: {star1("input.txt")}')
    assert(star1("input.txt") == 6838)
    
    # example = star2("example.txt")
    # print(f"Star 2 example: {example}")
    # assert(example == 2)

    # ans = star2("input.txt")
    # # assert ans == 12833235391111
    # print(f'Second star: {ans}')
