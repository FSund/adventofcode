
# def compare(p1, p2):
#     i = 0
#     while True:
#         v1 = p1[i]
#         v2 = p2[i]
#         if isinstance(v1, int) and isinstance(v2, int):
#             if v1 < v2:
#                 return True
            
#         return False


# recursive
def compare(left, right):
    # an element of a packet can be "1", "[]" or "None" (if packet = "[]")
    
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return True
        elif left > right:
            return False
        else:
            return None

    if isinstance(left, list) and isinstance(right, list):
        # If the lists are the same length and no comparison makes a decision about the order,
        # continue checking the next part of the input.
        left_empty = False
        right_empty = False
        while True:
            # If the left list runs out of items first, the inputs are in the right order
            try:
                new_left = left.pop(0)
            except IndexError:
                left_empty = True
            
            try:
                new_right = right.pop(0)
            except IndexError:
                right_empty = True
                
            if left_empty and not right_empty:
                return True
            if right_empty and not left_empty:
                return False
            if left_empty and right_empty:
                return None
            
            out = compare(new_left, new_right)
            if out is not None:
                return out

    if isinstance(left, list) and isinstance(right, int):
        return compare(left, [right])

    if isinstance(left, int) and isinstance(right, list):
        return compare([left], right)
    
    return False


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
        
        if compare(p1, p2):
            print(f"right order: {idx} ({lines[p1_idx]} and {lines[p2_idx]})")
            right_order.append(idx)
    
        idx += 1
        if 3*idx >= len(lines):
            break
    
    print(f"first star: {sum(right_order)}")
        
    # 5190 too low