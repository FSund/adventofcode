colors = ["red", "green", "blue"]
max_cubes = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

def second_star(line):
    # game = line.split(":")[0].strip()
    # game_id = int(game.split(" ")[1])
    sets = line.split(":")[1].split(";")
    # print(sets)
    
    game = {}
    for color in colors:
        game[color] = 0

    for set in sets:
        # print(f"{set = }")
        cubes = set.split(", ")
        for cube in cubes:
            # print(f"{cube = }")
            count, color = cube.strip().split(" ")
            count = int(count)
            if count > game[color]:
                game[color] = count
            
    power = 1
    for color in colors:
        power *= game[color]

    return power

def first_star(line):
    game = line.split(":")[0].strip()
    game_id = int(game.split(" ")[1])
    sets = line.split(":")[1].split(";")
    # print(sets)
    
    # game = {}
    # for color in colors:
    #     game[color] = 0

    for set in sets:
        # print(f"{set = }")
        cubes = set.split(", ")
        for cube in cubes:
            # print(f"{cube = }")
            count, color = cube.strip().split(" ")
            count = int(count)
            if count > max_cubes[color]:
                return 0
            
    return game_id
    

def main(filename, first=True):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    if first:
        sum = 0
        for line in lines:
            sum += first_star(line)
        
        return sum
    else:
        sum = 0
        for line in lines:
            sum += second_star(line)
        
        return sum


if __name__ == "__main__":
    # run_tests()

    example = main("example.txt")
    assert(example == 8)
    print(f'Example: {example}')
    
    print(f'First star: {main("input.txt")}')
    assert(main("input.txt") == 2879)
    
    example = main("example.txt", first=False)
    assert(example == 2286)
    print(f'Example: {example}')
    
    print(f'Second star: {main("input.txt", first=False)}')
    # assert(main("input.txt", first_star=False) == 55343)

    
# 50129 too low
# 423871440 too high
# 54239
