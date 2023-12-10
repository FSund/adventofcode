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
        return other_symbol in ["-", "J", "7"]
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
    
    if sym == "S":
        return None
    return distances
        

def star1(filename):
    lines = get_input(filename)
    
    # start only has two valid connections (according to the text)
    # try both direction, take minimum of map to get the shortest path
    distances = []
    for start_deltas in [
        # [(1, 0), (0, 1)],
        # [(0, 1), (1, 0)],
        [(-1, 0),],
        [(1, 0),],
        [(0, -1),],
        [(0, 1),],
    ]:
        d = _get_distances(lines, start_deltas)
        if d is not None:
            # image = plt.imshow(d)
            # plt.show()
            distances.append(d)
    
    assert len(distances) == 2
    
    distances = np.array(distances)
    distances = np.min(distances, axis=0)
    
    # fig, ax = plt.subplots()
    # ax.imshow(distances>0)
    # ax.set_title("Star 1")
    # plt.show()
    
    return int(np.max(distances))

def is_even(x):
    return x % 2 == 0

def is_inside(pos, im):
    if im[pos[0], pos[1]] != 0:
        return False
    # if lines[pos[0]][pos[1]] != ".":
    #     return False
    else:
        count_right = 0
        for j in range(pos[1] + 1, im.shape[1]):
            if im[pos[0], j] != im[pos[0], j - 1]:
                count_right += 1
            
        count_left = 0
        for j in range(pos[1] - 1, -1, -1):
            if im[pos[0], j] != im[pos[0], j + 1]:
                count_left += 1
                
        # If the point is on the inside of the polygon then it will intersect 
        # the edge an odd number of times
        # count == 0: outside
        # count == 1: on pipe
        # count == 2: inside
        # count == 3: on pipe
        # if count_right == 0 and count_left == 0:
        #     return False
        # else:
        return is_even(count_right) and is_even(count_left)


def star2(filename):
    lines = get_input(filename)
    
    # start only has two valid connections (according to the text)
    # try both direction, take minimum of map to get the shortest path
    distances = []
    for start_deltas in [
        [(-1, 0),],
        [(1, 0),],
        [(0, -1),],
        [(0, 1),],
    ]:
        d = _get_distances(lines, start_deltas)
        if d is not None:
            print(f"Valid start: {start_deltas}")
            # plt.imshow(d)
            # plt.show()
            distances.append(d)
    
    assert len(distances) == 2, f"len(distances) = {len(distances)} != 2"
    distances = np.array(distances)
    distances = np.min(distances, axis=0)
    
    # fig, ax = plot_image(distances>0)
    # fig, ax = plt.subplots()
    # ax.imshow(distances)
    # ax.set_title(f"Star 2 {filename}")
    
    # area = find_area_inside(distances)
    # print(f"Area: {area}")
    # return area
    
    area = find_area_inside2(distances, lines)
    print(f"Area: {area}")
    return area
    
    fig, ax = plt.subplots()
    ax.imshow(distances)
    ax.set_title(f"Star 2 {filename}")
    plt.show()
    
    im = distances>0
    # pad top
    im = np.vstack((np.zeros((1, im.shape[1]), dtype=bool), im))
    lines = ["." * len(lines[0])] + lines
    # pad bottom
    im = np.vstack((im, np.zeros((1, im.shape[1]), dtype=bool)))
    lines = lines + ["." * len(lines[0])]
    # pad left
    im = np.hstack((np.zeros((im.shape[0], 1), dtype=bool), im))
    lines = ["." + line for line in lines]
    # pad right
    im = np.hstack((im, np.zeros((im.shape[0], 1), dtype=bool)))
    lines = [line + "." for line in lines]
    
    fig, ax = plt.subplots()
    # extent = (0, im.shape[1], im.shape[0], 0)
    # ax.imshow(im, extent=extent)
    # ax.grid(color='w', linewidth=2)
    if im.shape[0] > 50:
        ax.pcolormesh(im)
    else:
        ax.pcolormesh(im, edgecolors='w', linewidth=1)
    ax.invert_yaxis()
    ax.set_aspect('equal')
    # plt.show()

    im_inside = np.zeros(im.shape)
    area = 0
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            inside = is_inside((i, j), im)
            area += inside
            im_inside[i,j] = inside
    
    im = im_inside
    fig, ax = plt.subplots()
    if im.shape[0] > 50:
        ax.pcolormesh(im)
    else:
        ax.pcolormesh(im, edgecolors='w', linewidth=1)
    ax.invert_yaxis()
    ax.set_aspect('equal')
    
    plt.show()
    
    return area

def plot_image(im):
    fig, ax = plt.subplots()
    if im.shape[0] > 50:
        ax.pcolormesh(im)
    else:
        ax.pcolormesh(im, edgecolors='w', linewidth=1)
    ax.invert_yaxis()
    ax.set_aspect('equal')
    
    return fig, ax

def find_area_inside2(distances, lines):
    sym_to_arr = {
        "|": np.array([
            [0, 1, 0],
            [0, 1, 0],
            [0, 1, 0],
        ]),
        "-": np.array([
            [0, 0, 0],
            [1, 1, 1],
            [0, 0, 0],
        ]),
        "F": np.array([
            [0, 0, 0],
            [0, 1, 1],
            [0, 1, 0],
        ]),
        "J": np.array([
            [0, 1, 0],
            [1, 1, 0],
            [0, 0, 0],
        ]),
        "7": np.array([
            [0, 0, 0],
            [1, 1, 0],
            [0, 1, 0],
        ]),
        "L": np.array([
            [0, 1, 0],
            [0, 1, 1],
            [0, 0, 0],
        ]),
    }
    
    # fix S
    def find_s_pos(lines):
        for i in range(len(lines)):
            for j in range(len(lines[0])):
                if lines[i][j] == "S":
                    return (i, j)
    s_pos = find_s_pos(lines)
    print(f"S pos: {s_pos}")
    
    distances[s_pos[0]][s_pos[1]] = -1

    right = (s_pos[0], s_pos[1] + 1)
    right = distances[right[0]][right[1]] == 1
    left = (s_pos[0], s_pos[1] - 1)
    left = distances[left[0]][left[1]] == 1
    up = (s_pos[0] - 1, s_pos[1])
    up = distances[up[0]][up[1]] == 1
    down = (s_pos[0] + 1, s_pos[1])
    down = distances[down[0]][down[1]] == 1
    
    if left and right:
        sym = "-"
    elif up and down:
        sym = "|"
    elif left and down:
        sym = "7"
    elif left and up:
        sym = "J"
    elif right and up:
        sym = "L"
    elif right and down:
        sym = "F"
    else:
        raise Exception("Invalid S")
    print(f"S: {sym}")
    lines = [list(line) for line in lines]
    lines[s_pos[0]][s_pos[1]] = sym
    
    im = np.zeros([len(distances)*3, len(distances[0])*3])
    for i in range(len(distances)):
        for j in range(len(distances[0])):
            if distances[i,j] != 0:
                sym = lines[i][j]
                arr = sym_to_arr[sym]
                im[i*3:i*3+3, j*3:j*3+3] = arr
    
    # fig, ax = plot_image(im)
    # plt.show()
    
    im = flood_fill(im)
    
    fig, ax = plot_image(im)
    # plt.show()
    
    for i in range(len(distances)):
        for j in range(len(distances[0])):
            if distances[i,j] != 0:
                im[i*3:i*3+3, j*3:j*3+3].fill(1)
    fig, ax = plot_image(im)
    plt.show()

    area = np.sum(im == 0)
    # area -= np.sum(distances != 0) * 9
    area /= 9
    area = int(area)
    
    return area

def find_area_inside(distances):
    im = distances > 0
    im = np.asarray(im, dtype=int)
    
    # pad top
    im = np.vstack((np.zeros((1, im.shape[1]), dtype=bool), im))
    im = np.vstack((im, np.zeros((1, im.shape[1]), dtype=bool)))
    im = np.hstack((np.zeros((im.shape[0], 1), dtype=bool), im))
    im = np.hstack((im, np.zeros((im.shape[0], 1), dtype=bool)))
    
    im = flood_fill(im)
    
    fig, ax = plot_image(im)
    ax.set_title("Flood fill")
    plt.show()
    
    print(f"max value: {np.max(im)}")
    print(f"min value: {np.min(im)}")
    
    return np.sum(im == 0)

def flood_fill(_im):
    im = np.copy(_im)
    pos = (0, 0)
    stack = [pos]
    while len(stack) > 0:
        pos = stack.pop()
        im[pos] = 2
        for delta in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_pos = (pos[0] + delta[0], pos[1] + delta[1])
            if new_pos[0] < 0 or new_pos[0] >= im.shape[0] or new_pos[1] < 0 or new_pos[1] >= im.shape[1]:
                # out of bounds
                continue
            if im[new_pos] == 0:
                stack.append(new_pos)
    return im

def tests():
    assert is_valid_connection((0,1), "F") == False

    m = np.asarray([
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
    ])
    
    assert is_inside((1,0), m) == False
    
    assert is_inside((2,2), m)
    assert is_inside((1,1), m) == False
    assert is_inside((1,2), m) == False
    assert is_inside((1,3), m) == False
    assert is_inside((2,1), m) == False
    assert is_inside((2,3), m) == False
    assert is_inside((3,1), m) == False
    assert is_inside((3,2), m) == False
    assert is_inside((3,3), m) == False
    assert is_inside((0,0), m) == False
    
    # top
    assert is_inside((0,0), m) == False
    assert is_inside((0,1), m) == False
    assert is_inside((0,2), m) == False
    assert is_inside((0,3), m) == False
    assert is_inside((0,4), m) == False
    
    # bottom
    assert is_inside((4,0), m) == False
    assert is_inside((4,1), m) == False
    assert is_inside((4,2), m) == False
    assert is_inside((4,3), m) == False
    assert is_inside((4,4), m) == False
    
    # left
    assert is_inside((1,0), m) == False
    assert is_inside((2,0), m) == False
    assert is_inside((3,0), m) == False
    
    assert is_inside((1,1), m) == False
    assert is_inside((2,1), m) == False
    assert is_inside((3,1), m) == False
    
    # right
    assert is_inside((1,4), m) == False
    assert is_inside((2,4), m) == False
    assert is_inside((3,4), m) == False

if __name__ == "__main__":
    # tests()

    # example = star1("example.txt")
    # print(f'Example: {example}')
    # assert(example == 8)
    
    # print(f'First star: {star1("input.txt")}')
    # assert(star1("input.txt") == 6838)
    
    example = star2("example2.txt")
    print(f"Star 2 example: {example}")
    assert example == 10
    
    assert star2("example3.txt") == 8

    ans = star2("input.txt")
    # assert ans == 12833235391111
    print(f'Second star: {ans}')

    # 6489 too high
    # 3534 too high
    # 712 too high