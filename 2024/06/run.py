from typing import Tuple, List, Optional
import numpy as np
import numpy.typing as npt


Position = Tuple[int, int]
GridType = np.uint8


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

FREE = 0
BLOCKED = 1
VISITED = 2


class Guard:
    def __init__(self, pos: Position, orientation):
        self.x = pos[1]
        self.y = pos[0]
        
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
    
    def move(self, grid: npt.NDArray[GridType]):
        size = grid.shape[0]
        
        x = self.x + self.dx
        y = self.y + self.dy
        if x >= size or y >= size or x < 0 or y < 0:
            return 0  # exited grid

        while grid[y, x] == BLOCKED:
            self.turn_right()
            x = self.x + self.dx
            y = self.y + self.dy
        
        if x >= size or y >= size or x < 0 or y < 0:
            return 0  # exited grid

        grid[y, x] = VISITED
        self.x = x
        self.y = y

        return 1  # moved one tile
    
    def get_next_pos(self, grid: npt.NDArray[GridType]) -> Optional[Position]:
        n = m = grid.shape[0]
        
        x = self.x + self.dx
        y = self.y + self.dy
        if x >= n or y >= m or x < 0 or y < 0:
            return None  # exited grid

        while grid[y, x] == BLOCKED:
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
    size = len(lines)
    
    grid = np.zeros((size, size), dtype=GridType)
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == ".":
                grid[i,j] = 0
            elif c == "#":
                grid[i,j] = BLOCKED
            elif c in ["<", ">", "v", "^"]:
                # starting location
                guard = Guard((i, j), c)
                grid[i, j] = VISITED  # mark as visited
            else:
                raise RuntimeError()

    while guard.move(grid):
        pass
    
    if size < 20:
        print(grid)

    count = 0
    for i in range(size):
        for j in range(size):
            if grid[i, j] == VISITED:
                count += 1
                
    return count


class DirectionGrid:
    # Direction bits (4-bit number)
    NORTH: GridType = 0b1000  # 8
    EAST: GridType = 0b0100   # 4
    SOUTH: GridType = 0b0010  # 2
    WEST: GridType = 0b0001   # 1
    
    OK = 0
    LOOP = 1
    OUTSIDE = 2
    
    def __init__(self, size: int) -> None:
        """Initialize an n x n grid where each cell is a 4-bit number."""
        self.size: int = size
        self.grid: npt.NDArray[GridType] = np.zeros((size, size), dtype=GridType)
    
    def reset(self):
        self.grid.fill(0)
    
    def is_valid_position(self, pos: Position) -> bool:
        """Check if the given position is within grid bounds."""
        return 0 <= pos[0] < self.size and 0 <= pos[1] < self.size
    
    def has_been_entered_from(self, pos: Position, direction: GridType):
        """Check if a cell has already been entered from a specific direction."""
        if not self.is_valid_position(pos):
            return False
        return bool(self.grid[pos[0]][pos[1]] & direction)
    
    def enter_from_direction(self, pos: Position, direction: GridType):
        """Mark that a cell has been entered from a specific direction."""
        if not self.is_valid_position(pos):
            raise ValueError(f"Position ({pos}) is outside grid bounds")
            
        self.grid[pos[0]][pos[1]] |= direction
    
    def move_entity(self, from_pos: Position, to_pos: Position):
        """
        Move an entity from one position to another, updating direction bits.
        Returns True if the move creates a loop, False otherwise.
        """
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        if not (self.is_valid_position(from_pos) and 
                self.is_valid_position(to_pos)):
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
        if self.has_been_entered_from(to_pos, direction):
            return self.LOOP
            
        # Update the grid
        self.enter_from_direction(to_pos, direction)
        return self.OK


def star2(filename):
    # input grid is 130x130
    # 16900 positions to test

    # encode how each grid position has been visited by 0b0000, where the bits 
    # indicate which direction we came from?
    
    lines = get_input(filename)
    size = len(lines)
    
    # initialize grid
    grid = np.zeros((size, size), dtype=GridType)
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == ".":
                grid[i,j] = 0
            elif c == "#":
                grid[i,j] = BLOCKED
            elif c in ["<", ">", "v", "^"]:
                # starting location
                start_pos = (i, j)
                start_orientation = c
                grid[i, j] = VISITED  # mark as visited
            else:
                raise RuntimeError()

    guard = Guard(start_pos, start_orientation)
    while guard.move(grid):
        pass

    n_visited = np.sum(grid == VISITED)
    print(f"Visited {n_visited}")

    dgrid = DirectionGrid(size)
    n_loops = 0
    n_checked = 0
    is_loop = False
    for row in range(size):
        for col in range(size):
            pos = (row, col)
            # only try blocks that have been visited
            # don't try starting position
            if grid[pos] != VISITED and pos != start_pos:
                continue
            
            # check if makes loop
            guard = Guard(start_pos, start_orientation)
            grid[pos] = BLOCKED
            
            while True:
                from_pos = (guard.y, guard.x)
                to_pos = guard.get_next_pos(grid)
                if not to_pos:
                    # outside grid
                    is_loop = False
                    break

                ret = dgrid.move_entity(from_pos, to_pos)
                if ret == DirectionGrid.OUTSIDE:
                    is_loop = False
                    break
                elif ret == DirectionGrid.LOOP:
                    is_loop = True
                    break
            
            # reset grid
            grid[pos] = FREE
            dgrid.reset()

            n_loops += is_loop
            n_checked += 1
            if is_loop:
                print(f"{n_loops = }, checked {n_checked} of {n_visited} ({round(n_checked/n_visited*100, 1)} %)")
                
    return n_loops


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
    assert ans == 1984
