import numpy as np
import itertools

def get_input(filename="example.txt"):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))
    return lines

# ####

# .#.
# ###
# .#.

# ..#
# ..#
# ###

# #
# #
# #
# #

# ##
# ##

# make rock types
horiz = np.zeros((1, 4), dtype=np.byte)
horiz.fill(2)
star = np.zeros((3, 3), dtype=np.byte)
star[0,1] = 2
star[1,0] = 2
star[1,1] = 2
star[1,2] = 2
star[2,1] = 2
corner = np.zeros((3, 3), dtype=np.byte)
corner[0,2] = 2
corner[1,2] = 2
corner[2,2] = 2
corner[2,0] = 2
corner[2,1] = 2
vert = np.zeros((4, 1), dtype=np.byte)
vert.fill(2)
square = np.zeros((2, 2), dtype=np.byte)
square.fill(2)

rocks = [horiz, star, corner, vert, square]


def find_top_rock_idx(frame):
    i = np.argmax(
        np.sum(frame > 1, axis=1) > 0
    )
    return i


def find_spawn_idx(frame, rock):
    # rock "position" is top left pixel of rock
    i = find_top_rock_idx(frame)
    
    # print(f"top rock row idx: {i}")
    # print(frame[i-10:])
    # a = frame>1
    # print(a[i-10:])
    # b = np.sum(frame > 1, axis=1)
    # print(b[i-10:])
    # c = b > 0
    # print(c[i-10:])
    
    
    return i - 3  - rock.shape[0]


def frame_to_example_ascii(frame, irange=None):
    lines = []
    if irange is None:
        irange = range(frame.shape[0])
    for i in irange:
        line = ""
        for j in range(frame.shape[1]):
            if frame[i,j] == 0:  # free
                line += "."
            elif frame[i,j] == 2:  # moving rock
                line += "@"
            elif frame[i,j] == 4:  # stopped rock
                line += "#"
            elif frame[i,j] == 1:  # boundaries
                if i == frame.shape[0]-1:
                    if j == 0 or j == frame.shape[1]-1:
                        line += "+"
                    else:
                        line += "-"
                else:
                    line += "|"
        lines.append(line)
        
    return lines


def compare_frame_to_example_ascii(frame):
    lines_ex = []
    with open("example_ascii_final.txt") as f:
        for line in f:
            lines_ex.append(line.strip("\n"))
    
    lines = frame_to_example_ascii(frame, irange=range(frame.shape[0]-22, frame.shape[0]))
    for l0, l1 in zip(lines_ex, lines):
        assert(l0 == l1)
        if l0 != l1:
            raise RuntimeError("example not equal")


def print_full_frame(frame, irange=None):
    if irange is None:
        irange = range(frame.shape[0])
    for i in irange:
        line = f"{i:3d} "
        for j in range(frame.shape[1]):
            if frame[i,j] == 0:  # free
                line += "."
            elif frame[i,j] == 2:  # moving rock
                line += "@"
            elif frame[i,j] == 4:  # stopped rock
                line += "#"
            elif frame[i,j] == 1:  # boundaries
                if i == frame.shape[0]-1:
                    if j == 0 or j == frame.shape[1]-1:
                        line += "+"
                    else:
                        line += "—"
                else:
                    line += "|"
        print(line)


def print_part_frame_from_rock(frame, rock_pos):
    # print(np.sum(frame[0:-2, 1:-2], axis=1))
    # top_rock_idx = find_top_rock_idx(frame)
    # print(frame[41])
    # print(top_rock_idx-2)
    for i in range(rock_pos[0]-1, frame.shape[0]):
        line = f"{i:3d} "
        for j in range(frame.shape[1]):
            if frame[i,j] == 0:  # free
                line += "."
            elif frame[i,j] == 2:  # moving rock
                line += "@"
            elif frame[i,j] == 4:  # stopped rock
                line += "#"
            elif frame[i,j] == 1:  # boundaries
                if i == frame.shape[0]-1:
                    if j == 0 or j == frame.shape[1]-1:
                        line += "+"
                    else:
                        line += "—"
                else:
                    line += "|"
        print(line)



# The tall, vertical chamber is exactly seven units wide. 

# Each rock appears so that its left edge is two units away from the left wall
# and its bottom edge is three units above the highest rock in the room 
# (or the floor, if there isn't one).


def add_rock(frame, rock, position):
    # "position" is top left corner of rock
    i0 = position[0]
    i1 = i0 + rock.shape[0]
    j0 = position[1]
    j1 = j0 + rock.shape[1]

    frame[i0:i1, j0:j1] += rock


def remove_rock(frame, rock, position):
    # "position" is top left corner of rock
    i0 = position[0]
    i1 = i0 + rock.shape[0]
    j0 = position[1]
    j1 = j0 + rock.shape[1]

    frame[i0:i1, j0:j1] -= rock


def spawn_rock(frame, rock):
    # rock_idx = rock_idx % (len(rocks) - 1)
    position = [0, 0]
    position[0] = find_spawn_idx(frame, rock)
    position[1] = 3
    
    add_rock(frame, rock, position)

    return position


def _push(frame, rock, pos, dy):
    # remove current rock
    frame[pos[0]:pos[0] + rock.shape[0], pos[1]:pos[1] + rock.shape[1]] -= rock
    
    # new rock position
    i0 = pos[0]
    i1 = pos[0] + rock.shape[0]
    j0 = pos[1] + dy
    j1 = pos[1] + dy + rock.shape[1]
    
    # check if new position is free
    if np.any(np.logical_and(frame[i0:i1, j0:j1], rock)):
        success = False
        # add back rock
        frame[pos[0]:pos[0] + rock.shape[0], pos[1]:pos[1] + rock.shape[1]] += rock
    else:
        success = True
        frame[i0:i1, j0:j1] += rock
        pos[1] += dy
    
    return pos, success


def push(frame, rock, pos, move):
    # "<" means a push to the left, 
    # while ">" means a push to the right
    if move == "<":
        dy = -1
    elif move == ">":
        dy = +1
    
    return _push(frame, rock, pos, dy)


def fall(frame, rock, pos, dx=1):
    # remove existing rock
    frame[pos[0]:pos[0] + rock.shape[0], pos[1]:pos[1] + rock.shape[1]] -= rock

    # new rock position
    i0 = pos[0] + dx
    i1 = pos[0] + dx + rock.shape[0]
    j0 = pos[1]
    j1 = pos[1] + rock.shape[1]

    # check if new position is free    
    if np.any(np.logical_and(frame[i0:i1, j0:j1], rock)):
        success = False
        # add fixed rock
        frame[pos[0]:pos[0] + rock.shape[0], pos[1]:pos[1] + rock.shape[1]] += 2*rock
    else:
        success = True
        frame[i0:i1, j0:j1] += rock
        pos[0] += dx
    
    return pos, success

def step(frame, rock, rocks_it, next_action, rock_position, moves_it, n_rocks):
    if next_action == 0:
        # spawn
        rock = next(rocks_it)
        position = spawn_rock(frame, rock)
        next_action = 1
        # print(f"spawn at {position}")
        n_rocks += 1
    elif next_action == 1:  # PUSH
        # push if possible
        move = next(moves_it)
        position, success = push(frame, rock, rock_position, move)
        # print(f"push {success}")
        next_action = 2
    elif next_action == 2:  # FALL
        # fall, if possible
        position, success = fall(frame, rock, rock_position)
        # print(f"fall {success}")
        if success:
            # push
            next_action = 1
        else:
            # spawn new
            next_action = 0
    
    return position, next_action, rock, n_rocks


# def test_moves(moves):
#     move = next(moves)
#     print(move)

def check_example():
    frame = np.zeros((5000, 9), dtype=np.byte)
    
    # chamber limits
    frame[-1,:] = 1
    frame[:,0] = 1
    frame[:,-1] = 1
    
    # spawn first rock manually
    rock_position = [frame.shape[0] - 4 - rocks[0].shape[0], 3]
    add_rock(frame, rocks[0], rock_position)
    
    lines = get_input("example.txt")
    
    moves = []
    for c in lines[0]:
        moves.append(c)

    n_rocks = 1
    next_action = 1  # 0: spawn, 1: push, 3: fall
    moves_it = itertools.cycle(moves)
    rocks_it = itertools.cycle(rocks)
    rock = next(rocks_it)  # get first rock
    n_rocks = 1
    while n_rocks < 11:
        rock_position, next_action, rock, n_rocks = step(frame, rock, rocks_it, next_action, rock_position, moves_it, n_rocks)

    compare_frame_to_example_ascii(frame)
    assert(np.all(frame <= 4))
    
    return True


def get_height(frame):
    idx = find_top_rock_idx(frame)
    return frame.shape[0] - idx - 1


def star2_example(filename="example.txt", block_size=200):
    n = block_size
    frame = np.zeros((n, 9), dtype=np.byte)
    
    # chamber limits
    frame[-1,:] = 1
    frame[:,0] = 1
    frame[:,-1] = 1
    
    # print(rocks)
    
    # spawn first rock manually
    rock_position = [frame.shape[0] - 4 - rocks[0].shape[0], 3]
    add_rock(frame, rocks[0], rock_position)
    # print(frame)
    
    # print_part_frame_from_rock(frame, rock_position)
    
    lines = get_input(filename)
    
    moves = []
    for c in lines[0]:
        moves.append(c)
    # print(moves)
    
    # rock_idx = 1
    n_rocks = 1
    next_action = 1  # 0: spawn, 1: push, 3: fall
    moves_it = itertools.cycle(moves)
    rocks_it = itertools.cycle(rocks)
    rock = next(rocks_it)  # get first rock
    first_cycle = False
    iterations = 0
    total_shifted = 0
    while n_rocks < 2023:
        rock_position, next_action, rock, n_rocks = step(frame, rock, rocks_it, next_action, rock_position, moves_it, n_rocks)
        if rock_position[0] < n/8:
            # print_full_frame(frame[rock_position[0]-2:rock_position[0]+20,:])
            
            # shift frame down by n/2
            nhalf = int(n/2)
            # frame[0:nhalf, :] = frame[nhalf:, :]
            # frame[nhalf:-1, :][1:9] = 0
            
            # move top half to bottom half
            frame[nhalf:, :] = frame[0:nhalf,:]
            frame[-1,:].fill(1)  # wall
            
            # zero out top half (except walls)
            frame[0:nhalf, 1:8].fill(0)
            
            # shift rock position down by n/2
            rock_position[0] += nhalf
            
            total_shifted += nhalf
            
            # print_full_frame(frame[rock_position[0]-2:rock_position[0]+20,:])
            
            # print("SHIFT")
            
        # if iterations % 10000 == 0:
        #     print(f"{n_rocks = }")
        # print(rock_position)
        # print(n_rocks)
        # print_frame(frame, rock_position)
        
        iterations += 1
    
    remove_rock(frame, rock, rock_position)
    
    height = get_height(frame) + total_shifted
    
    # print(f"star 1: {get_height(frame)}")
    # print(f"{total_shifted = }")
    # print(f"star 2: {height}")
    
    assert(np.all(frame <= 4))
    
    # print_full_frame(frame, range(idx-10, idx+10))
    
    return height



def star2(filename="example.txt", max_n_rocks=1_000_000_000_000, block_size=4000):
    n = block_size
    frame = np.zeros((n, 9), dtype=np.byte)
    
    # chamber limits
    frame[-1,:] = 1
    frame[:,0] = 1
    frame[:,-1] = 1
    
    # print(rocks)
    
    # spawn first rock manually
    rock_position = [frame.shape[0] - 4 - rocks[0].shape[0], 3]
    add_rock(frame, rocks[0], rock_position)
    # print(frame)
    
    # print_part_frame_from_rock(frame, rock_position)
    
    lines = get_input(filename)
    
    moves = []
    for c in lines[0]:
        moves.append(c)
    # print(moves)
    
    # rock_idx = 1
    n_rocks = 1
    next_action = 1  # 0: spawn, 1: push, 3: fall
    moves_it = itertools.cycle(moves)
    rocks_it = itertools.cycle(rocks)
    rock = next(rocks_it)  # get first rock
    first_cycle = False
    iterations = 0
    total_shifted = 0
    while n_rocks < max_n_rocks:
        rock_position, next_action, rock, n_rocks = step(frame, rock, rocks_it, next_action, rock_position, moves_it, n_rocks)
        if rock_position[0] < n/8:
            # print_full_frame(frame[rock_position[0]-2:rock_position[0]+20,:])
            
            # shift frame down by n/2
            nhalf = int(n/2)
            # frame[0:nhalf, :] = frame[nhalf:, :]
            # frame[nhalf:-1, :][1:9] = 0
            
            # move top half to bottom half
            frame[nhalf:, :] = frame[0:nhalf,:]
            frame[-1,:].fill(1)  # wall
            
            # zero out top half (except walls)
            frame[0:nhalf, 1:8].fill(0)
            
            # shift rock position down by n/2
            rock_position[0] += nhalf
            
            total_shifted += nhalf
            
            # print_full_frame(frame[rock_position[0]-2:rock_position[0]+20,:])
            
            # print("SHIFT")
            
        if iterations % 10000 == 0:
            print(f"{n_rocks = }")
        # print(rock_position)
        # print(n_rocks)
        # print_frame(frame, rock_position)
        
        iterations += 1
    
    remove_rock(frame, rock, rock_position)
    
    height = get_height(frame) + total_shifted
    
    # print(f"star 1: {get_height(frame)}")
    print(f"{total_shifted = }")
    print(f"star 2: {height}")
    
    assert(np.all(frame <= 4))
    
    # print_full_frame(frame, range(idx-10, idx+10))
    
    return height


if __name__ == "__main__":
    if not check_example():
        print("TESTS FAILED")
        raise RuntimeError("TESTS FAILED")

    assert(star2_example("example.txt", block_size=200) == 3068)
    # star2("input.txt")
    star2("input.txt", 100_000, 200)