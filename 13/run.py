class Packet:
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"{self.value}"
    
    # less than
    def __lt__(self, other):
        if isinstance(self.value, int) and isinstance(other.value, int):
            # print("case int int")
            return self.value < other.value
        
        if isinstance(self.value, list) and isinstance(other.value, int):
            # print("case list int")
            other.value = [other.value]
            return self < other

        if isinstance(self.value, int) and isinstance(other.value, list):
            # print("case int list")
            self.value = [self.value]
            return self < other
        
        if isinstance(self.value, list) and isinstance(other.value, list):
            # print("case list list")
            for left, right in zip(self.value, other.value):
                left = Packet(left) 
                right = Packet(right)
                if left == right:
                    continue
                else:
                    return left < right
            
            # If the left list runs out of items first, the inputs are in the right order.
            if len(self.value) < len(other.value):
                return True
            else:
                return False
        
        raise RuntimeError

    def __eq__(self, other):
        if isinstance(self.value, int) and isinstance(other.value, int):
            # print("case int int")
            return self.value == other.value
        
        if isinstance(self.value, list) and isinstance(other.value, int):
            # print("case list int")
            other.value = [other.value]
            return self == other

        if isinstance(self.value, int) and isinstance(other.value, list):
            # print("case int list")
            self.value = [self.value]
            return self == other
        
        if isinstance(self.value, list) and isinstance(other.value, list):
            equal = True
            for left, right in zip(self.value, other.value):
                left = Packet(left) 
                right = Packet(right)
                if left == right:
                    pass
                else:
                    equal = False
            if equal:
                if len(self.value) == len(other.value):
                    return True
                else:
                    return False
            else:
                return False
        
        raise RuntimeError


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
    
    print(f"first star: {sum(right_order)}")
    # 5190 too low


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
    print(f"star 2: {i1*i2}")


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
    star1()
    
    # testing()
    
    star2()
