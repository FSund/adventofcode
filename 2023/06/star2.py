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

def check_range(source_start, source_length, maps):
    # overlaps = []
    start = source_start
    end = source_start + source_length
    for map in maps:
        map_destination_start, map_source_start, map_length = map
        map_end = map_source_start + map_length
        if map_source_start <= start < map_end:
            if map_end <= end:
                
    

def check_map(source_start, source_length, all_maps_idx, all_maps):
    maps = all_maps[all_maps_idx]

    for map in maps:
        map_destination_start, map_source_start, map_length = map
        if map_source_start <= source_start < map_source_start + map_length:
            offset = source_start - map_source_start
            return map_destination_start + offset
        
    
    


def star2(filename):
    lines = get_input(filename)
    all_maps = get_all_mappings(lines)
    
    sources = lines[0].strip("seeds: ").split(" ")
    sources = [int(source) for source in sources]
    
    start = sources[0::2]
    length = sources[1::2]


if __name__ == "__main__":
    print(f'Second star: {star2("input.txt", star2=True)}')
    
    # tests()
    # example = star2("example.txt")
    # assert example == 30
    # print(f'Example: {example}')
    
    # s2 = star2("input.txt")
    # assert s2 == 23806951
    # print(f'Second star: {s2}')
