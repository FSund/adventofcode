import numpy as np
from datetime import datetime
from pathlib import Path
from collections import OrderedDict

def get_input(filename):
    return Path(filename).read_text().strip()

def HASH(s):
    value = 0
    for c in s:
        value += ord(c)
        value *= 17
        value = value % 256
    return value

def star1(filename):
    line = get_input(filename)
    seq = line.split(",")
    
    total = 0
    for s in seq:
        total += HASH(s)
    
    return total

def split_s(s):
    if "=" in s:
        return (s[:-2], s[-2:])
    elif "-" in s:
        return (s[:-1], s[-1:])

# def insert_front(original_dict, key, value):
#     new_dict = OrderedDict([(key, value)])
#     new_dict.update(original_dict)
#     return new_dict

def insert_front_in_place(ordered_dict, key, value):
    ordered_dict.update({key: value})
    # ordered_dict.move_to_end(key, last=False)

def fill_boxes(seq):
    boxes = [OrderedDict() for i in range(256)]
    for s in seq:
        label, operation = split_s(s)
        box_idx = HASH(label)
        box = boxes[box_idx]
        if "=" in operation:
            focal_length = int(operation[-1])
            if label in box:
                box[label] = focal_length
            else:
                box = insert_front_in_place(box, label, focal_length)
        elif "-" in operation:
            if label in box:
                box.pop(label)
        else:
            raise Exception(f"unknown command {s}")
    
    return boxes

def star2(filename):
    line = get_input(filename)
    seq = line.split(",")
    boxes = fill_boxes(seq)

    
    non_empty_boxes = [box for box in boxes if len(box) > 0]
    
    total_power = 0
    for idx in range(len(boxes)):
        box = boxes[idx]
        box_list = list(box)
        # power = 1
        for label, focal_length in box.items():
            slot = box_list.index(label)
            total_power += (1 + idx) * (slot + 1) * focal_length
    
    return total_power

def tests():
    assert HASH("HASH") == 52
    
    a = OrderedDict()
    a["hei"] = 1
    insert_front_in_place(a, "hopp", 2)
    # print(a)
    
    line = get_input("example.txt")
    seq = line.split(",")
    boxes = fill_boxes(seq)
    for idx in range(256):
        if idx in [0, 3]:
            assert len(boxes[idx])
        else:
            assert len(boxes[idx]) == 0
           
    print(boxes[0])
    print(boxes[0].values())
    assert list(boxes[0].values())[0] == 1
    assert list(boxes[0].values())[1] == 2
    
    assert list(boxes[3].values())[0] == 7
    assert list(boxes[3].values())[1] == 5
    assert list(boxes[3].values())[2] == 6

if __name__ == "__main__":
    tests()

    example = star1("example.txt")
    print(f"example star 1: {example}")
    assert example == 1320
    
    example = star1("input.txt")
    print(f"star 1: {example}")
    
    example = star2("example.txt")
    print(f"example star 2: {example}")
    assert example == 145
    
    example = star2("input.txt")
    print(f"star 2: {example}")
    # assert example == 145
    
    