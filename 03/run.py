def get_priority(char):
    if char.islower():
        return ord(char) - 97 + 1
    else:
        return ord(char) - 65 + 27

def intersection(lst1, lst2):
    return [value for value in lst1 if value in lst2]

sum = 0
with open("input.txt") as file:
    while True:
        line1 = file.readline()[:-1]
        line2 = file.readline()[:-1]
        line3 = file.readline()[:-1]
        inter = intersection(line1, line2)
        inter = intersection(inter, line3)
        if len(inter) == 0:
            break
        print(inter)
        sum += get_priority(inter[0])
            
        
    # for line in file:
    #     i += 1
    #     L = int(len(line)/2)
    #     # print(L)
    #     print(line)
    #     a = list(line[:L])
    #     b = list(line[L:-1])
    #     print(a)
    #     print(b)
        
    #     for letter in a:
    #         if letter in b:
                
    #             print(letter)
    #             sum += get_priority(letter)
    #             break
                
print(sum)
print(i)

# 11871 too high