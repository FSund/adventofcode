def get_score_star2(a, b):
    str_to_score = {
        'rock': 1,
        'paper': 2,
        'scissors': 3,
    }
    map_str = {
        'A': 'rock', 
        'B': 'paper', 
        'C': 'scissors', 
        'X': 'loose', 
        'Y': 'draw', 
        'Z': 'win'}
    map2win = {
        'rock': 'paper', 
        'paper': 'scissors', 
        'scissors': 'rock'}
    map2loose = {
        'rock': 'scissors', 
        'paper': 'rock', 
        'scissors': 'paper'}

    if b == 'X':
        # loose
        return str_to_score[map2loose[map_str[a]]] + 0
    elif b == 'Y':
        # draw
        return str_to_score[map_str[a]] + 3
    else: # b == 'Z'
        # win
        return str_to_score[map2win[map_str[a]]] + 6


total_score = 0
with open("input.txt") as f:
    for line in f:
        a = line[0]
        b = line[2]
        total_score += get_score_star2(a, b)

print(total_score)  # 13600