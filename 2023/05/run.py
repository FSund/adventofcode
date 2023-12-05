import numba
from numba import njit, int64
import concurrent.futures
import functools

def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))
    return lines

    
def get_range(line):
    destination_start, source_start, length = line.split(" ")
    return (int(destination_start), int(source_start), int(length))


def _get_destination(source: int, maps: list[tuple[int, int, int]]) -> int:
    for map in maps:
        destination_start, source_start, length = map
        if source_start <= source < source_start + length:
            offset = source - source_start
            return destination_start + offset

    return source


def get_destinations(sources, maps):
    dest = []
    for source in sources:
        dest.append(_get_destination(source, maps))
    return dest


def get_all_mappings(lines):
    i = 2
    maps = []
    all_maps = []
    while i < len(lines):
        line = lines[i]
        if line == "":
            all_maps.append(maps)
            maps = []
        elif ":" in line:
            pass
        else:
            maps.append(get_range(line))
            
        i += 1
        
    # final map
    all_maps.append(maps)
    
    return all_maps


def map_source(source: int, all_maps):
    for maps in all_maps:
        source = _get_destination(source, maps)

    return source

def find_min_in_range(start, end, all_maps):
    num_workers = 8
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        
        f = functools.partial(map_source, all_maps=all_maps)
        
        # Map the function to the range of numbers
        results = executor.map(f, range(start, end))

        # Find the minimum value
        return min(results)


def _star2(filename):
    lines = get_input(filename)
    all_maps = get_all_mappings(lines)
    
    sources = lines[0].strip("seeds: ").split(" ")
    sources = [int(source) for source in sources]

    start = sources[0::2]
    length = sources[1::2]
    min_loc = 1e100
    for start, length in zip(start, length):
        print(f"pair {start} {length}")
        # for source in range(start, start + length):
        #     loc = map_source(source, all_maps)
        #     if loc < min_loc:
        #         min_loc = loc
        #         print(min_loc)

        loc = find_min_in_range(start, start + length, all_maps)
        if loc < min_loc:
            min_loc = loc
            print(min_loc)
    
    return min_loc


def _star1(filename):
    lines = get_input(filename)
    
    sources = lines[0].strip("seeds: ").split(" ")
    sources = [int(source) for source in sources]
    
    # if star2:
    #     new_sources = []
    #     start = sources[0::2]
    #     length = sources[1::2]
    #     for start, length in zip(start, length):
    #         new_sources.extend(range(start, start + length))
    #     sources = new_sources
    
    i = 2
    maps = []
    mappings = 0
    while i < len(lines):
        line = lines[i]
        if line == "":
            # print("start mapping")
            sources = get_destinations(sources, maps)
            # print("did mapping")
            mappings += 1
        elif ":" in line:
            # print(line)
            maps = []
        else:
            maps.append(get_range(line))
            
        i += 1
    
    # final iteration
    if mappings < 7:
        sources = get_destinations(sources, maps)
        # print("did mapping")
    
    return sources
    

def main(filename, star2=False):
    if star2:
        sources = _star2(filename)
        return sources
    else:
        sources = _star1(filename)
        # print(sources)
        return min(sources)


def tests():
    lines = get_input("example.txt")
    
    assert get_range("50 98 2") == (50, 98, 2)
    
    assert get_range("3078006360 2182201339 30483272") == (3078006360, 2182201339, 30483272)
    
    assert _get_destination(0, [(0, 0, 1)]) == 0
    assert _get_destination(1, [(0, 0, 2)]) == 1
    assert _get_destination(5, [(4, 5, 1)]) == 4
    assert _get_destination(5, [(0, 1, 5)]) == 4
    
    # not in range
    assert _get_destination(5, [(0, 0, 1)]) == 5
    assert _get_destination(5, [(4, 6, 1)]) == 5
    
    # example
    assert _get_destination(79, [(52, 50, 48)]) == 81
    assert _get_destination(81, [(18, 25, 70)]) == 74
    
    assert _star1("example.txt") == [82, 43, 86, 35]
    
    all_maps = get_all_mappings(lines)
    assert len(list(all_maps)) == 7
    assert map_source(79, all_maps) == 82
    


if __name__ == "__main__":
    tests()

    example = main("example.txt")
    assert(example == 35)
    print(f'Example: {example}')
    
    print(f'First star: {main("input.txt")}')
    assert(main("input.txt") == 226172555)
    
    example = main("example.txt", star2=True)
    assert(example == 46)
    
    # print(f'Second star: {main("input.txt", star2=True)}')
    
    # tests()
    # example = star2("example.txt")
    # assert example == 30
    # print(f'Example: {example}')
    
    # s2 = star2("input.txt")
    # assert s2 == 23806951
    # print(f'Second star: {s2}')
