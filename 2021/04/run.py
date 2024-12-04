def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def get_boards(lines):
    boards = []
    board = []
    for line in lines[2:]:
        if len(line):
            # board.append(line)
            # parse ints
            board.append([int(val) for val in line.split()])
        else:
            boards.append(board)
            board = []
    
    # remember final board
    boards.append(board)
    
    return boards

marked_value = 10000

def check_if_winner(board):
    for line in board:
        s = sum(line)
        if s == 5*marked_value:
            return True
    
    
    for j in range(5):
        s = 0
        for i in range(5):
            s += board[i][j]
        if s == 5*marked_value:
            return True

    return False


def mark_number(board, number):
    for i in range(5):
        for j in range(5):
            if board[i][j] == number:
                board[i][j] = marked_value


def get_sum_of_unmarked(board):
    s = 0
    for i in range(5):
        for j in range(5):
            s += board[i][j]
    
    return s % marked_value


def star1(filename):
    lines = get_input(filename)
    drawings = lines[0]
    drawings = [int(val) for val in drawings.split(",")]
    boards = get_boards(lines)
    
    for number in drawings:
        for board in boards:
            mark_number(board, number)
            if check_if_winner(board):
                s = get_sum_of_unmarked(board)
                # print(f"Winning number: {number}")
                # print(f"Winning board:\n{board}")
                return s*number



def star2(filename):
    lines = get_input(filename)
    drawings = lines[0]
    drawings = [int(val) for val in drawings.split(",")]
    boards = get_boards(lines)
    
    n_boards = len(boards)
    winners = 0
    for number in drawings:
        for i in list(range(len(boards)))[::-1]:  # reverse order so we can pop
            board = boards[i]
            mark_number(board, number)
            if check_if_winner(board):
                winners += 1
                if winners == n_boards:
                    s = get_sum_of_unmarked(board)
                    # print(f"Winning number: {number}")
                    # print(f"Winning board:\n{board}")
                    return s*number
                else:
                    boards.pop(i)


def tests():
    lines = get_input("example.txt")
    boards = get_boards(lines)
    assert len(boards) == 3

    ans = star1("example.txt")
    print(f"example star 1: {ans}")
    assert ans == 4512, f"wrong answer: {ans}"
    
    ans = star2("example.txt")
    print(f"example star 2: {ans}")
    assert ans == 1924, f"wrong answer: {ans}"

if __name__ == "__main__":
    tests()
    
    ans = star1("input.txt")
    print(f"star 1: {ans}")
    assert ans == 11774

    ans = star2("input.txt")
    print(f"star 2: {ans}")
    assert ans == 4495

