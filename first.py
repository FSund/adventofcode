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
horiz = np.zeros((1, 4), dtype=int)
horiz.fill(2)
star = np.zeros((3, 3), dtype=int)
star[0,1] = 2
star[1,0] = 2
star[1,1] = 2
star[1,2] = 2
star[2,1] = 2
corner = np.zeros((3, 3), dtype=int)
corner[0,2] = 2
corner[1,2] = 2
corner[0,2] = 2
corner[1,2] = 2
corner[2,2] = 2
vert = np.zeros((4, 1), dtype=int)
vert.fill(2)
square = np.zeros((2, 2), dtype=int)
square.fill(2)

rocks = [horiz, star, corner, vert, square]


def find_top_rock_idx(frame):
    i = np.argmax(
        np.sum(
            frame > 1,  # look for everything except walls
            axis=1) > 1)
    return i


def find_spawn_idx(frame, rock):
    # rock "position" is top left pixel of rock
    i = find_top_rock_idx(frame)
    return i - 3  - rock.shape[0]


def print_frame(frame):
    # print(np.sum(frame[0:-2, 1:-2], axis=1))
    top_rock_idx = find_top_rock_idx(frame)
    for i in range(top_rock_idx-2, frame.shape[0]):
        line = ""
        for j in range(frame.shape[1]):
            if frame[i,j] == 0:  # free
                line += "."
            elif frame[i,j] == 2:  # moving rock
                line += "@"
            elif frame[i,j] == 3:  # stopped rock
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
        frame[pos[0]:pos[0] + rock.shape[0], pos[1]:pos[1] + rock.shape[1]] += rock + 1
    else:
        success = True
        frame[i0:i1, j0:j1] += rock
        pos[0] += dx
    
    return pos, success

def step(frame, rock, rocks_it, next_action, rock_position, moves_it):
    if next_action == 0:
        # spawn
        rock = next(rocks_it)
        position = spawn_rock(frame, rock)
        next_action = 1
        print(f"spawn at {position}")
    elif next_action == 1:  # PUSH
        # push if possible
        move = next(moves_it)
        position, success = push(frame, rock, rock_position, move)
        print(f"push {success}")
        next_action = 2
    elif next_action == 2:  # FALL
        # fall, if possible
        position, success = fall(frame, rock, rock_position)
        print(f"fall {success}")
        if success:
            # push
            next_action = 1
        else:
            # spawn new
            next_action = 0
    
    return position, next_action, rock


# def test_moves(moves):
#     move = next(moves)
#     print(move)


if __name__ == "__main__":
    frame = np.zeros((20, 9), dtype=int)
    
    # chamber limits
    frame[-1,:] = 1
    frame[:,0] = 1
    frame[:,-1] = 1
    
    # print(rocks)
    
    # spawn first rock manually
    rock_position = [frame.shape[0] - 4 - rocks[0].shape[0], 3]
    add_rock(frame, rocks[0], rock_position)
    # print(frame)
    
    print_frame(frame)
    
    lines = get_input("example.txt")
    
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
    for i in range(10):
        rock_position, next_action, rock = step(frame, rock, rocks_it, next_action, rock_position, moves_it)
        print(rock_position)
        print_frame(frame)
