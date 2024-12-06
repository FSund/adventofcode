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
    def __init__(self, row, col, orientation):
        self.x = col
        self.y = row
        
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
    
    def get_next_pos(self, grid):
        m = len(grid)
        n = len(grid[0])
        
        x = self.x + self.dx
        y = self.y + self.dy
        if x >= n or y >= m or x < 0 or y < 0:
            return None  # exited grid

        while grid[y][x] == "#":
            self.turn_right()
            x = self.x + self.dx
            y = self.y + self.dy
        
        if x >= n or y >= m or x < 0 or y < 0:
            return None  # exited grid

        self.x = x
        self.y = y

        return y, x
        


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
                guard = Guard(i, j, grid[i][j])
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


class DirectionGrid:
    # Direction bits (4-bit number)
    NORTH = 0b1000  # 8
    EAST  = 0b0100  # 4
    SOUTH = 0b0010  # 2
    WEST  = 0b0001  # 1
    
    OK = 0
    LOOP = 1
    OUTSIDE = 2
    
    def __init__(self, size):
        """Initialize an n x n grid where each cell is a 4-bit number."""
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
    
    def is_valid_position(self, row, col):
        """Check if the given position is within grid bounds."""
        return 0 <= row < self.size and 0 <= col < self.size
    
    # def get_entry_directions(self, row, col):
    #     """Get a list of directions from which this cell has been entered."""
    #     if not self.is_valid_position(row, col):
    #         return []
            
    #     directions = []
    #     cell = self.grid[row][col]
        
    #     if cell & self.NORTH:
    #         directions.append('North')
    #     if cell & self.EAST:
    #         directions.append('East')
    #     if cell & self.SOUTH:
    #         directions.append('South')
    #     if cell & self.WEST:
    #         directions.append('West')
        
    #     return directions
    
    def has_been_entered_from(self, row, col, direction):
        """Check if a cell has already been entered from a specific direction."""
        if not self.is_valid_position(row, col):
            return False
        return bool(self.grid[row][col] & direction)
    
    def enter_from_direction(self, row, col, direction):
        """Mark that a cell has been entered from a specific direction."""
        if not self.is_valid_position(row, col):
            raise ValueError(f"Position ({row}, {col}) is outside grid bounds")
            
        self.grid[row][col] |= direction
    
    def move_entity(self, from_pos, to_pos):
        """
        Move an entity from one position to another, updating direction bits.
        Returns True if the move creates a loop, False otherwise.
        """
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        if not (self.is_valid_position(from_row, from_col) and 
                self.is_valid_position(to_row, to_col)):
            raise self.OUTSIDE
        
        # Determine direction of movement and corresponding entry direction
        direction = None
        if to_row < from_row:    # Moving North
            direction = self.SOUTH
        elif to_row > from_row:  # Moving South
            direction = self.NORTH
        elif to_col < from_col:  # Moving West
            direction = self.EAST
        elif to_col > from_col:  # Moving East
            direction = self.WEST
        else:
            raise ValueError("From and to positions are the same")
            
        # Check for loop
        if self.has_been_entered_from(to_row, to_col, direction):
            return self.LOOP
            
        # Update the grid
        self.enter_from_direction(to_row, to_col, direction)
        return self.OK


def check_if_makes_loop(start_row, start_col, row, col, lines):
    grid = []
    for line in lines:
        grid.append([])
        for c in line:
            grid[-1].append(c)

    dgrid = DirectionGrid(len(grid))
    orientation = grid[start_row][start_col]
    guard = Guard(start_row, start_col, orientation)
    
    grid[row][col] = "#"
    
    while True:
        from_pos = (guard.y, guard.x)
        to_pos = guard.get_next_pos(grid)
        if not to_pos:
            return False  # outside grid

        ret = dgrid.move_entity(from_pos, to_pos)
        if ret == DirectionGrid.OUTSIDE:
            return False
        elif ret == DirectionGrid.LOOP:
            return True
        else:
            continue


def star2(filename):
    # input grid is 130x130
    # 16900 positions to test

    # encode how each grid position has been visited by 0b0000, where the bits 
    # indicate which direction we came from?
    
    lines = get_input(filename)
    
    assert len(lines) == len(lines[0])
    
    grid = []
    for line in lines:
        grid.append([])
        for c in line:
            grid[-1].append(c)
    
    start_row = None
    start_col = None
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] != "." and grid[row][col] != "#":
                start_row = row
                start_col = col

    loops = 0
    n_possible = len(grid) * len(grid[0])
    n_checked = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            is_loop = check_if_makes_loop(start_row, start_col, row, col, grid)
            loops += is_loop
            n_checked += 1
            if is_loop:
                print(f"{loops = }, checked {n_checked} of {n_possible} ({n_checked/n_possible*100} %)")
                
    return loops


def tests():
    ans = star1("example.txt")
    print(f"example star 1: {ans}")
    assert ans == 41, f"wrong answer: {ans}"
    
    ans = star2("example.txt")
    print(f"example star 2: {ans}")
    assert ans == 6, f"wrong answer: {ans}"

if __name__ == "__main__":
    tests()
    
    ans = star1("input.txt")
    print(f"star 1: {ans}")
    assert ans == 5404

    ans = star2("input.txt")
    print(f"star 2: {ans}")
    # assert ans == 5770
