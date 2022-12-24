import sys
sys.stdout.reconfigure(encoding='utf-8')

import math

def parse_input ( filename ) :
    from pathlib import Path
    with open(Path(__file__).parent / filename, "r") as f :
        data = f.read().splitlines()
    
    map = {}
    for x, line in enumerate(data) :
        for y, char in enumerate(line) :
            if char == "#" :
                map[(x, y)] = {"x": x, "y": y, "history": []}
    
    return map

def map_size ( map ) :
    min_x = min(x for x, y in map)
    max_x = max(x for x, y in map)
    min_y = min(y for x, y in map)
    max_y = max(y for x, y in map)

    return max_x - min_x + 1, max_y - min_y + 1

def round ( map, dir_offset ) :
    proposals = {}
    for x, y in map :
        if (x-1, y-1) not in map and (x-1, y) not in map and (x-1, y+1) not in map and (x, y-1) not in map and (x, y+1) not in map and (x+1, y-1) not in map and (x+1, y) not in map and (x+1, y+1) not in map :
            proposals[(x, y)] = proposals.get((x, y), []) + [(x, y)]
            continue
        for i in range(4) :
            dir = (i + dir_offset) % 4
            if dir == 0 and (x-1, y-1) not in map and (x-1, y) not in map and (x-1, y+1) not in map :
                proposals[(x-1, y)] = proposals.get((x-1, y), []) + [(x, y)]
                break
            elif dir == 1 and (x+1, y-1) not in map and (x+1, y) not in map and (x+1, y+1) not in map :
                proposals[(x+1, y)] = proposals.get((x+1, y), []) + [(x, y)]
                break
            elif dir == 2 and (x-1, y-1) not in map and (x, y-1) not in map and (x+1, y-1) not in map :
                proposals[(x, y-1)] = proposals.get((x, y-1), []) + [(x, y)]
                break
            elif dir == 3 and (x-1, y+1) not in map and (x, y+1) not in map and (x+1, y+1) not in map :
                proposals[(x, y+1)] = proposals.get((x, y+1), []) + [(x, y)]
                break
        else :
            proposals[(x, y)] = proposals.get((x, y), []) + [(x, y)]
    
    new_map = {}
    for x, y in proposals :
        if len(proposals[(x, y)]) > 1 :
            for source_x, source_y in proposals[(x, y)] :
                new_map[(source_x, source_y)] = map[(source_x, source_y)]
        else :
            new_map[(x, y)] = map[proposals[(x, y)][0]]

    return new_map

def print_map ( map ) :
    min_x = min(x for x, y in map)
    max_x = max(x for x, y in map)
    min_y = min(y for x, y in map)
    max_y = max(y for x, y in map)

    screen_width = max_y - min_y + 1
    screen_height = max_x - min_x + 1

    for x in range(min_x, max_x+1) :
        for y in range(min_y, max_y+1) :
            if (x, y) in map :
                print("#", end="")
            else :
                print(".", end="")
        print()

if __name__ == "__main__" :
    map = parse_input("input")

    for i in range(10) :
        map = round(map, i)
    print_map(map)
    
    map_height, map_width = map_size(map)
    empty_space = map_height * map_width - len(map)

    print(f"Part 1: {empty_space}")
