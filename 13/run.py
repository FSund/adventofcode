class Packet:
    def __init__(self, value):
        self.value = value
    
    @staticmethod
    def _make_left_right(this, other):
        if isinstance(this.value, list) and isinstance(other.value, list):
            # use Python's built-in list comparison
            left = [Packet(p) for p in this.value]
            right = [Packet(p) for p in other.value]
        
        if isinstance(other.value, int):
            left = this
            right = Packet([other.value])

        if isinstance(this.value, int):
            left = Packet([this.value])
            right = other
            
        return left, right
    
    # for nice printing
    def __repr__(self):
        return f"{self.value}"
    
    # less than (<)
    def __lt__(self, other):
        if isinstance(self.value, int) and isinstance(other.value, int):
            return self.value < other.value
        else:
            left, right = self._make_left_right(self, other)
            return left < right

    # equal (==)
    def __eq__(self, other):
        if isinstance(self.value, int) and isinstance(other.value, int):
            return self.value == other.value
        else:
            left, right = self._make_left_right(self, other)
            return left == right


def star1():
    lines = []
    with open("input.txt") as file:
        for line in file:
            lines.append(line.strip("\n"))
    
    # for example_input, packet 1, 2, 4, and 6 are in the right order
    
    right_order = []
    idx = 1
    while True:
        p1_idx = 3*(idx-1) + 0  # idx is 1-based...
        p2_idx = 3*(idx-1) + 1  # idx is 1-based...
        p1 = lines[p1_idx]
        p2 = lines[p2_idx]
        p1 = eval(p1)
        p2 = eval(p2)
        p1 = Packet(p1)
        p2 = Packet(p2)
        
        result = p1 < p2
        if result:
            # print(f"right order: {idx} ({lines[p1_idx]} and {lines[p2_idx]})")
            right_order.append(idx)
    
        idx += 1
        if 3*(idx - 1) >= len(lines):
            break

    # 5190 too low
    return sum(right_order)


def star2():
    lines = []
    with open("input.txt") as file:
        for line in file:
            lines.append(line.strip("\n"))
    
    lines.append("[[2]]")
    lines.append("[[6]]")
    
    packets = []
    for line in lines:
        if line == "":
            continue
        p = Packet(eval(line))
        packets.append(p)
    packets.sort()
    # for p in packets:
    #     print(p)
    
    i1 = 0
    i2 = 0
    for idx, p in enumerate(packets):
        if p.value == [[2]]:
            i1 = idx+1
        if p.value == [[6]]:
            i2 = idx+1
    
    return i1*i2


def testing():
    p1 = Packet([[[]]])
    p2 = Packet([])
    assert(p2 < p1)
    assert(p2 != p1)
    assert(not Packet([1]) < Packet([1]))
    assert(Packet([1]) < Packet([2]))
    print(Packet([1,1,3,1,1]) < Packet([1,1,5,1,1]))


if __name__ == "__main__":
    # Your puzzle answer was 5340.
    v1 = star1()
    print(f"first star: {v1}")
    assert(v1 == 5340)
    
    # testing()
    
    v2 = star2()
    print(f"star 2: {v2}")
    assert(v2 == 21276)
