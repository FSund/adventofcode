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
            print(x)
            print(y)
            if x > x_max:
                x_max = x
            if x < x_min:
                x_min = x
            if y > y_max:
                y_max = y
            if y < y_min:
                y_min = y

    return x_min, x_max, y_min, y_max


if __name__ == "__main__":

    lines = []
    with open("input.txt") as file:
        for line in file:
            lines.append(line.strip("\n"))

    x_min, x_max, y_min, y_max = find_boundaries(lines)
    x_min -= 1
    x_max += 1
    # y_min -= 1
    # y_max += 1
    y_min = 0
    y_max = 9
    
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
    
    
    for i in range(len(frame)):
        row = "".join([frame[i][j] for j in range(494, 504)])
        
        print(f"{i} {row}")