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
            for left, right in zip(self.value, other.value):
                left = Packet(left) 
                right = Packet(right)
                if left == right:
                    continue
                return left < right
            if len(self.value) < len(other.value):
                return True  # There were more items in the second tuple
            else:
                return False  # The first tuple had more items or they are equal
        
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
            return equal
        
        raise RuntimeError
        

if __name__ == "__main__":
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
        
        result = p1 > p2
        if result:
            # print(f"right order: {idx} ({lines[p1_idx]} and {lines[p2_idx]})")
            right_order.append(idx)
    
        idx += 1
        if 3*(idx - 1) >= len(lines):
            break
    
    print(f"first star: {sum(right_order)}")
    # 5190 too low
    
    lines.append("[[2]]")
    lines.append("[[6]]")
    packets = []
    for line in lines:
        if line == "":
            continue
        p = Packet(eval(line))
        packets.append(p)
    packets.sort()
    for p in packets:
        print(p)
