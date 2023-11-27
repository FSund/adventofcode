def get_priority(char):
    if char.islower():
        return ord(char) - 97 + 1
    else:
        return ord(char) - 65 + 27

def intersection(lst1, lst2):
    return [value for value in lst1 if value in lst2]

def is_fully_contained_in_other(r1, r2):
    if r1[0] <= r2[0] and r1[1] >= r2[1]:
        return True
    elif r2[0] <= r1[0] and r2[1] >= r1[1]:
        return True
    else:
        return False

def has_some_overlap(r1, r2):
    # r1[0]   r1[1]
    #      r2[0]     r2[1]
    if r1[0] <= r2[0] and r1[1] >= r2[0]:
        return True
    #      r1[0]     r1[1]
    # r2[0]   r2[1]
    if r2[0] <= r1[0] and r2[1] >= r1[0]:
        return True

    return False
    

sum = 0
with open("input.txt") as file:
    for line in file:
        r1, r2 = line.split(",")
        r1 = [int(r) for r in r1.split("-")]
        r2 = [int(r) for r in r2.split("-")]
        # sum += is_fully_contained_in_other(r1, r2)
        sum += has_some_overlap(r1, r2)
        
print(sum)  # 285 too low
# 550 too low