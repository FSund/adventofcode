def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def should_move_left(update, idx, rules):
    # check that number at idx is according to rules
    for rule in rules:
        if rule[0] == update[idx]:
            # check that no numbers _before_ idx is rule[1]
            for i in range(idx):
                if update[i] == rule[1]:
                    return True
    
    return False


def should_move_right(update, idx, rules):
    # check that number at idx is according to rules
    for rule in rules:
        if rule[1] == update[idx]:
            # check that no numbers _after_ idx is rule[1]
            for i in range(idx+1, len(update)):
                if update[i] == rule[0]:
                    return True
    
    return False



def is_in_correct_order(update, rules):
    n = len(update)
    for i in range(n):
        if should_move_left(update, i, rules):
            return False

    return True


# The first rule, 47|53, means that  if an update includes both page number 47 
# and page number 53, then page number 47 must be printed at some point before
# page number 53.


def star1(filename):
    lines = get_input(filename)
    
    rules = []
    updates = []
    for line in lines:
        if "|" in line:
            rule = [int(d) for d in line.split("|")]
            rules.append(rule)
        elif "," in line:
            update = [int(d) for d in line.split(",")]
            updates.append(update)
    
    result = 0
    for update in updates:
        if is_in_correct_order(update, rules):
            i = int(len(update) / 2)
            result += update[i]
    
    return result


def fix_ordering(update, rules):
    n = len(update)
    while not is_in_correct_order(update, rules):
        # loop through all until they are in the correct order
        # for i in range(n-1, -1, -1):  # reverse loop
        #     j = i
        #     while not should_move_left(update, j, rules):
        #         # swap current_pos with current_pos+1
        #         this = update[j]
        #         right = update[j + 1]
        #         update[j] = right
        #         update[j+1] = this
        #         j+= 1
        #         if j == n:
        #             break
        for i in range(n-1):  # skip last number
            j = i
            while should_move_right(update, j, rules):
                # swap number at pos j with j+1
                this = update[j]
                right = update[j+1]
                update[j] = right
                update[j+1] = this
                j += 1
                if j == n:
                    break
    
    return update


def star2(filename):
    lines = get_input(filename)
    
    rules = []
    updates = []
    for line in lines:
        if "|" in line:
            rule = [int(d) for d in line.split("|")]
            rules.append(rule)
        elif "," in line:
            update = [int(d) for d in line.split(",")]
            updates.append(update)
    
    result = 0
    for update in updates:
        if not is_in_correct_order(update, rules):
            update = fix_ordering(update, rules)
            i = int(len(update) / 2)
            result += update[i]
            
    
    return result    


def tests():
    update = [75,47,61,53,29]
    rules = []
    assert not should_move_left(update, 2, rules)
    rules = [[61, 53]]  # 61 should appear before 53
    assert not should_move_left(update, 2, rules)
    rules = [[61, 47]]  # 61 should appear before 47
    assert should_move_left(update, 2, rules)
    
    ans = star1("example.txt")
    print(f"example star 1: {ans}")
    assert ans == 143, f"wrong answer: {ans}"
    
    
    update = [75,47,61,53,29]
    rules = []
    assert fix_ordering(update, rules) == [75,47,61,53,29]
    update = [75,47,61,53,29]
    rules = [[47, 75]]
    assert fix_ordering(update, rules) == [47,75,61,53,29]
    
    ans = star2("example.txt")
    print(f"example star 2: {ans}")
    assert ans == 123, f"wrong answer: {ans}"

if __name__ == "__main__":
    tests()
    
    ans = star1("input.txt")
    print(f"star 1: {ans}")
    assert ans == 7365

    ans = star2("input.txt")
    print(f"star 2: {ans}")
    assert ans == 5770
