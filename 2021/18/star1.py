from pathlib import Path


def get_input(filename):
    script_dir = Path(__file__).parent
    lines = []
    with open(script_dir / filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


class Pair:
    # def __init__(self, left, right, parent=None):
    #     self.parent = parent
    #     if left.isdigit():
    #         self.left = int(left)
    #     else:
    #         ll, rr = get_left_and_right(left)
    #         self.left = Pair(ll, rr, self)
    #     if right.isdigit():
    #         self.right = int(right)
    #     else:
    #         ll, rr = get_left_and_right(right)
    #         self.right = Pair(ll, rr, self)
    
    def __init__(self, line, parent=None):
        left, right = get_left_and_right(line)
        self.parent = parent
        if left.isdigit():
            self.left = int(left)
        else:
            self.left = Pair(left, self)
        if right.isdigit():
            self.right = int(right)
        else:
            self.right = Pair(right, self)

    def count_parents(self) -> int:
        parent = self.parent
        count = 0
        while parent:
            count += 1
            parent = parent.parent

        return count
    
    def should_explode(self) -> bool:
        # If any pair is nested inside four pairs, the leftmost such pair explodes.
        return self.count_parents() >= 4
    
    def explode(self):
        assert isinstance(self.left, int) and isinstance(self.right, int)
        assert self.parent
        self.parent.add_left(self.left)
        self.parent.add_right(self.right)

    def add_left(self, number: int):
        """ Add `number` to the first regular number to the left of the exploding pair
        """
        if isinstance(self.left, int):
            # if this pair's left element is a regular number, add it
            self.left += number
        else:
            if self.parent is None:
                # don't add this number to anything if there are no regular numbers to the left 
                pass
            else:
                # up one level
                self.parent.add_left(number)

    def add_right(self, number: int):
        """ Add `number` to the first regular number to the right of the exploding pair
        """
        if isinstance(self.right, int):
            self.right += number
        else:
            if self.parent is None:
                pass
            else:
                self.parent.add_right(number)

def get_left(line):
    # find left part of pair
    assert line[0] == "["

    if line[1].isdigit():
        return line[1]
    else:
        return get_left(line[1:])

    # left = ""
    # for idx, c in line:
    #     if c == ",":
    #         # check if left half is closed
    #         pass
    #     elif c.isdigit():
            



def get_left_and_right(line):
    # all lines have an outer bracket, and a left and right part
    # [<anything>, <anything>]
    # where <anything> can be a number or more pair(s)
    assert " " not in line, "Line should have no spaces"
    left = ""
    right = ""
    for idx, c in enumerate(line):
        if c == "," and left.count("[") == left.count("]") + 1:  # plus one for the outer bracket
            right = line[idx+1:]
            return left[1:], right[:-1]
        else:
            left += c

    raise RuntimeError("Should never get here")


# def make_pairs(line):
#     parent = None
#     left, right = get_left_and_right(line)
#     while not left.isdigit():



def aoc(filename):
    lines = get_input(filename)



    return None


def tests():
    assert get_left_and_right("[1,2]") == ("1", "2")
    assert get_left_and_right("[[1,2],3]") == ("[1,2]", "3")
    assert get_left_and_right("[[1,2],[3,4]]") == ("[1,2]", "[3,4]")

    pair = Pair("[1,2]")
    assert isinstance(pair.left, int)
    assert isinstance(pair.right, int)

    pair = Pair("[[1,2],3]")
    assert isinstance(pair.left, Pair)
    assert isinstance(pair.right, int)

    pair = Pair("[[1,2],[3,4]]")
    assert isinstance(pair.left, Pair)
    assert isinstance(pair.right, Pair)
    assert not pair.should_explode()

    pair = Pair("[[[[[9,8],1],2],3],4]")
    assert isinstance(pair.left, Pair)
    assert isinstance(pair.left.left, Pair)
    assert isinstance(pair.left.left.left, Pair)
    assert isinstance(pair.left.left.left.left, Pair)
    assert isinstance(pair.left.left.left.left.left, int)
    assert pair.left.left.left.left.should_explode()
    assert not pair.left.left.left.should_explode()
    assert not pair.left.left.should_explode()
    assert not pair.left.should_explode()
    assert not pair.should_explode()

    

    # assert get_left("[[1,2],3]") == "[1,2]"
    # assert get_left("[1,2]") == "1"


    # ans = aoc("example.txt")
    # print(f"example: {ans}")
    # assert ans == 4140, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    # ans = aoc("input")
    # print(f"{ans = }")