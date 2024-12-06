def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines

# dx: 1 0 -1  0
# dy: 0 1  0 -1

ormap = {
    ">": [1, 0],
    "v": [0, 1],
    "<": [-1, 0],
    "^": [0, -1],
}


class Guard:
    def __init__(self, x, y, orientation):
        self.x = x
        self.y = y
        
        dxdy = ormap[orientation]
        self.dx = dxdy[0]
        self.dy = dxdy[1]
    
    def turn_right(self):
        if self.dx == 1:
            self.dx = 0
            self.dy = 1
        elif self.dy == 1:
            self.dx = -1
            self.dy = 0
        elif self.dx == -1:
            self.dx = 0
            self.dy = -1
        elif self.dy == -1:
            self.dx = 1
            self.dy = 0
    
    def move(self, grid):
        m = len(grid)
        n = len(grid[0])
        
        x = self.x + self.dx
        y = self.y + self.dy
        if x >= n or y >= m or x < 0 or y < 0:
            return 0  # exited grid

        while grid[y][x] == "#":
            self.turn_right()
            x = self.x + self.dx
            y = self.y + self.dy
        
        if x >= n or y >= m or x < 0 or y < 0:
            return 0  # exited grid

        grid[y][x] = "x"
        self.x = x
        self.y = y

        return 1  # moved one tile


def star1(filename):
    lines = get_input(filename)
    
    grid = []
    for line in lines:
        grid.append([])
        for c in line:
            grid[-1].append(c)
    
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != "." and grid[i][j] != "#":
                x = j
                y = i
                guard = Guard(x, y, grid[i][j])
                grid[i][j] = "x"
    
    while guard.move(grid):
        pass
    
    if len(grid) < 20:
        for i in range(len(grid)):
            print(grid[i])

    count = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "x":
                count += 1
                
    return count
 

def tests():    
    ans = star1("example.txt")
    print(f"example star 1: {ans}")
    assert ans == 41, f"wrong answer: {ans}"
    
    # ans = star2("example.txt")
    # print(f"example star 2: {ans}")
    # assert ans == 123, f"wrong answer: {ans}"

if __name__ == "__main__":
    tests()
    
    ans = star1("input.txt")
    print(f"star 1: {ans}")
    assert ans == 5404

    # ans = star2("input.txt")
    # print(f"star 2: {ans}")
    # assert ans == 5770
