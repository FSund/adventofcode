import numpy as np

def find_max(lines):
    x_max = 0
    y_max = 0
    for line in lines:
        coords = line.split(" -> ")
        for pos in coords:
            x, y = (int(c) for c in pos.split(","))
            print(x)
            print(y)
            if x > x_max:
                x_max = x
            if y > y_max:
                y_max = y

    return x_max, y_max

def find_boundaries(lines):
    x_max = 0
    x_min = 1e9
    y_max = 0
    y_min = 1e9
    for line in lines:
        coords = line.split(" -> ")
        for pos in coords:
            x, y = (int(c) for c in pos.split(","))
            # print(x)
            # print(y)
            if x > x_max:
                x_max = x
            if x < x_min:
                x_min = x
            if y > y_max:
                y_max = y
            if y < y_min:
                y_min = y

    return x_min, x_max, y_min, y_max

    
def parse_input():
    lines = []
    with open("input.txt") as file:
        for line in file:
            lines.append(line.strip("\n"))

    x_min, x_max, y_min, y_max = find_boundaries(lines)
    print(f"{x_min = }")
    print(f"{x_max = }")
    # x_min -= 1
    # x_max += 1
    x_min = 0
    x_max = 1000
    y_min -= 1
    y_max += 1
    # y_min = 0
    # y_max = 9
    
    # use full frame, only print part of it
    x_min = 0
    y_min = 0

    # Your scan traces the path of each solid rock structure and reports the 
    # x,y coordinates that form the shape of the path, 
    # where x represents distance to the right and 
    # y represents distance down. 
    # 
    # Each path appears as a single line of text in your scan. 
    # After the first point of each path, each point indicates the end of 
    # a straight horizontal or vertical line to be drawn from the previous point.
    frame = [["."]*(x_max - x_min) for y in range(y_min, y_max)]
    
    # source of sand
    frame[0][500] = "+"
    
    # set up walls
    for line in lines:
        coords = line.split(" -> ")
        for idx in range(len(coords) - 1):
            i0 = int(coords[idx].split(",")[1])  # use index 1 for i and 0 for j
            j0 = int(coords[idx].split(",")[0])
            i1 = int(coords[idx+1].split(",")[1])
            j1 = int(coords[idx+1].split(",")[0])
            
            if i1 < i0:
                # print(f"{i0} -> {i1}")
                i0, i1 = i1, i0
                # print(f"{i0} -> {i1}\n")
            if j1 < j0:
                # print(f"{j0} -> {j1}")
                j0, j1 = j1, j0
                # print(f"{j0} -> {j1}\n")

            # print(f"{i0}, {j0} -> {i1}, {j1}")
            if i0 == i1:
                i = i0
                for j in range(j0, j1+1):
                    frame[i][j] = "#"
            if j0 == j1:
                j = j0
                for i in range(i0, i1+1):
                    frame[i][j] = "#"
    
    
    # for i in range(len(frame)):
    #     row = "".join([frame[i][j] for j in range(494, 504)])
        
    #     print(f"{i} {row}")
    
    return frame


def step(frame, pos, source=(0, 500)):
    # 0 is empty
    # 1 is wall
    # 2 is moving sand
    # 3 is static sand
    
    new_sand = False
    if not len(pos):
        # spawn sand
        pos = [source[0], source[1]]
        frame[pos[0], pos[1]] = 2
        new_sand = True
    else:
        # check if done
        if sum(frame[pos[0]+1:, pos[1]] > 0) == 0:
            raise RuntimeError

        i = np.argmax(frame[pos[0]+1:, pos[1]] > 0)
        # print(i)
        if i > 0:
            frame[pos[0], pos[1]] = 0
            pos[0] += i
            frame[pos[0], pos[1]] = 2
        elif frame[pos[0]+1, pos[1]-1] == 0:
            frame[pos[0], pos[1]] = 0
            pos[0] += 1
            pos[1] -= 1
            # pos = [pos[0]+1, pos[1]-1]
            frame[pos[0], pos[1]] = 2
        elif frame[pos[0]+1, pos[1]+1] == 0:
            frame[pos[0], pos[1]] = 0
            pos[0] += 1
            pos[1] += 1
            # pos = [pos[0]+1, pos[1]+1]
            frame[pos[0], pos[1]] = 2
        else:
            # sand has arrived at final destination
            frame[pos[0], pos[1]] = 3
            # pos = [source[0]+1, source[1]]
            # frame[pos[0], pos[1]] = 2
            pos = []
    
    return pos, new_sand


def print_np_frame(frame):
    for i in range(frame.shape[0]):
        line = f"{i:3d} "
        for j in range(frame.shape[1]):
            if frame[i][j] == 0:
                line += "."
            elif frame[i][j] == 1:
                line += "#"
            elif frame[i][j] == 2:
                line += "o"
            elif frame[i][j] == 3:
                line += "x"
        print(line)


def get_np_frame():
    input = parse_input()
    frame = np.zeros((len(input), len(input[0])))
    sources = []
    for i in range(frame.shape[0]):
        for j in range(frame.shape[1]):
            if input[i][j] == ".":
                frame[i,j] = 0
            elif input[i][j] == "#":
                frame[i,j] = 1
            elif input[i][j] == "+":
                frame[i,j] = 0
                sources.append((i, j))
    
    return frame, sources

    
def star1():
    frame, sources = get_np_frame()
    
    
    # print(frame[:, 494:])
    moving_sand = []
    sand_count = 0
    # print_np_frame(frame[:, 494:])
    while True:
        try:
            moving_sand, new_sand = step(frame, moving_sand, sources[0])
        except:
            break
        sand_count += new_sand
        # print(moving_sand)
        # print(frame[:, 494:])
        # print_np_frame(frame[:, 494:])
        
    # remove final sand that goes into the abyss
    sand_count -= 1

    # print(frame[:, 494:])
    # print_np_frame(frame[:, 494:])
    print(f"star 1: {sand_count}")  # 828
    
    print(frame.shape)

def star2():
    frame, sources = get_np_frame()

    bottom = np.zeros((2, frame.shape[1]))
    bottom[-1,:] = 1
    frame = np.vstack([frame, bottom])
    print(frame.shape)
    # print_np_frame(frame[:, 494:])
    
    # make walls to reduce simulation time
    # x_min = 473
    # x_max = 530
    # frame[:, 450] = 1
    # frame[:, 550] = 1
    
    moving_sand = []
    sand_count = 0
    while True:
        try:
            moving_sand, new_sand = step(frame, moving_sand, sources[0])
            if new_sand:
                source = sources[0]
                if frame[source[0]+1, source[1]] and frame[source[0]+1, source[1]+1] and frame[source[0]+1, source[1]-1]:
                    break
        except:
            break
        sand_count += new_sand
        
        if new_sand and (sand_count % 10 == 0):
            print(sand_count)

    # remove final sand that goes into the abyss
    sand_count -= 1
    
    # print_np_frame(frame[:, 470:531])
    
    # add triangles outside walls
    
    
    print(f"star 2: {np.sum(np.sum(frame == 3)) + 1}")
    # 12061 too low
    # 25171 too low


if __name__ == "__main__":
    # star1()
    star2()