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
    x_min -= 1
    x_max += 1
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


def step(frame, pos, source=[0, 500]):
    new_sand = False
    if frame[pos[0]+1, pos[1]] == 0:
        frame[pos[0], pos[1]] = 0
        pos = [pos[0]+1, pos[1]]
        frame[pos[0], pos[1]] = 2
    elif frame[pos[0]+1, pos[1]-1] == 0:
        frame[pos[0], pos[1]] = 0
        pos = [pos[0]+1, pos[1]-1]
        frame[pos[0], pos[1]] = 2
    elif frame[pos[0]+1, pos[1]+1] == 0:
        frame[pos[0], pos[1]] = 0
        pos = [pos[0]+1, pos[1]+1]
        frame[pos[0], pos[1]] = 2
    else:
        # sand has arrived at final destination
        frame[pos[0], pos[1]] = 1
        pos = source
        new_sand = True
    
    return pos, new_sand
            
    
if __name__ == "__main__":
    input = parse_input()
    for i in range(len(input)):
        row = "".join([input[i][j] for j in range(494, 504)])
        
        print(f"{i} {row}")

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
                sources.append([i, j])

    
    print(frame[:, 494:])
    moving_sand = sources[0]
    sand_count = 0
    while sand_count < 25:
        try:
            moving_sand, new_sand = step(frame, moving_sand, sources[0])
        except:
            break
        sand_count += new_sand
        # print(moving_sand)
        # print(frame[:, 494:])
        
    print(frame[:, 494:])
