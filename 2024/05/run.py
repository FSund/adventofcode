def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def is_according_to_rules(update, idx, rules):
    # check that number at idx is according to rules
    for rule in rules:
        if rule[0] == update[idx]:
            # check that no numbers before idx is rule[1]
            for i in range(idx):
                if update[i] == rule[1]:
                    return False
    
    return True


def is_in_correct_order(update, rules):
    n = len(update)
    for i in range(n):
        if not is_according_to_rules(update, i, rules):
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
        
    


def tests():
    update = [75,47,61,53,29]
    rules = []
    assert is_according_to_rules(update, 2, rules)
    rules = [[61, 53]]  # 61 should appear before 53
    assert is_according_to_rules(update, 2, rules)
    rules = [[61, 47]]  # 61 should appear before 47
    assert not is_according_to_rules(update, 2, rules)
    
    
    ans = star1("example.txt")
    print(f"example star 1: {ans}")
    assert ans == 143, f"wrong answer: {ans}"
    
    # ans = star2("example.txt")
    # print(f"example star 2: {ans}")
    # assert ans == 9, f"wrong answer: {ans}"

if __name__ == "__main__":
    tests()
    
    ans = star1("input.txt")
    print(f"star 1: {ans}")
    assert ans == 7365

    # ans = star2("input.txt")
    # print(f"star 2: {ans}")
    # assert ans == 1824
