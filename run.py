
# def compare(p1, p2):
#     i = 0
#     while True:
#         v1 = p1[i]
#         v2 = p2[i]
#         if isinstance(v1, int) and isinstance(v2, int):
#             if v1 < v2:
#                 return True
            
#         return False

class Packet:
    def __init__(self, content):
        self.content = content
    
    def __eq__(self, other):
        return self.content == other.content
    
    # defining less than
    def __lt__(self, other):
        # an element of a packet can be "1", "[]" or "None" (if packet = "[]")
        
        # If the left integer is lower than the right integer, the inputs are in the right order. 
        # If the left integer is higher than the right integer, the inputs are not in the right order. 
        # Otherwise, the inputs are the same integer; continue checking the next part of the input.
        if isinstance(self.content, int) and isinstance(other.content, int):
            if self == other:
                return None
            else:
                return self < other

        elif isinstance(self.content, list) and isinstance(other.content, list):
            # If the lists are the same length and no comparison makes a decision about the order,
            # continue checking the next part of the input.
            while True:
                # If the left list runs out of items first, the inputs are in the right order
                try:
                    new_left = self.content.pop(0)
                except IndexError:
                    left_empty = True
                else:
                    left_empty = False
                
                try:
                    new_right = other.pop(0)
                except IndexError:
                    right_empty = True
                else:
                    right_empty = False

                if left_empty and not right_empty:
                    return True
                if right_empty and not left_empty:
                    return False
                if left_empty and right_empty:
                    return None
                
                out = compare(new_left, new_right)
                if out is None:
                    continue
                else:
                    return out

        elif isinstance(self.content, list) and isinstance(other.content, int):
            return self > [other]

        elif isinstance(self, int) and isinstance(other, list):
            return compare([self], other)
    
    raise RuntimeError
    
    # defining greater than
    def __gt__(self, other):
        return self.f > other.f

# recursive
def compare(left, right):
    # an element of a packet can be "1", "[]" or "None" (if packet = "[]")
    
    # If the left integer is lower than the right integer, the inputs are in the right order. 
    # If the left integer is higher than the right integer, the inputs are not in the right order. 
    # Otherwise, the inputs are the same integer; continue checking the next part of the input.
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return None
        else:
            return left < right

    elif isinstance(left, list) and isinstance(right, list):
        # If the lists are the same length and no comparison makes a decision about the order,
        # continue checking the next part of the input.
        while True:
            # If the left list runs out of items first, the inputs are in the right order
            try:
                new_left = left.pop(0)
            except IndexError:
                left_empty = True
            else:
                left_empty = False
            
            try:
                new_right = right.pop(0)
            except IndexError:
                right_empty = True
            else:
                right_empty = False

            if left_empty and not right_empty:
                return True
            if right_empty and not left_empty:
                return False
            if left_empty and right_empty:
                return None
            
            out = compare(new_left, new_right)
            if out is None:
                continue
            else:
                return out

    elif isinstance(left, list) and isinstance(right, int):
        return compare(left, [right])

    elif isinstance(left, int) and isinstance(right, list):
        return compare([left], right)
    
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
        
        # i = 0
        # while True:
        #     v1 = p1[i]
        #     v2 = p2[i]
        #     if isinstance(v1, int) and isinstance(v2, int):
        #         if v1 < v2:
        #             right_order.append(True)
        #             break
        #     elif isinstance(v1, list) and isinstance(v2, list)
            
        #     i += 1
        
        result = compare(p1, p2)
        if result is None:
            raise RuntimeError
        if result:
            # print(f"right order: {idx} ({lines[p1_idx]} and {lines[p2_idx]})")
            right_order.append(idx)
    
        idx += 1
        if 3*(idx - 1) >= len(lines):
            break
    
    print(f"first star: {sum(right_order)}")
        
    # 5190 too low