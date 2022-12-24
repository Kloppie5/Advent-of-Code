import sys
sys.stdout.reconfigure(encoding='utf-8')

import math

def parse_input ( filename ) :
    from pathlib import Path
    with open(Path(__file__).parent / filename, "r") as f :
        data = f.read().splitlines()
    
    map = {"walls": [], "blizzards": {}, "flood": []}
    for x, line in enumerate(data) :
        for y, char in enumerate(line) :
            if char == "#" :
                map["walls"].append((x, y))
            elif char != "." :
                map["blizzards"][(x, y)] = [char]
    
    map["flood"].append((0, 1))

    return map

def print_map ( map ) :
    min_x = min(x for x, y in map["walls"])
    max_x = max(x for x, y in map["walls"])
    min_y = min(y for x, y in map["walls"])
    max_y = max(y for x, y in map["walls"])

    screen_height = max_x - min_x + 1
    screen_width = max_y - min_y + 1

    for x in range(screen_height) :
        for y in range(screen_width) :
            if (x, y) in map["walls"] :
                print("#", end="")
            elif (x, y) in map["blizzards"] :
                if len(map["blizzards"][(x, y)]) > 1 :
                    print(len(map["blizzards"][(x, y)]), end="")
                else :
                    print(map["blizzards"][(x, y)][0], end="")
            elif (x, y) in map["flood"] :
                print("X", end="")
            else :
                print(".", end="")
        print()

def round ( map ) :
    new_map = {"walls": [], "blizzards": {}, "flood": []}
    map_height = max(x for x, y in map["walls"]) + 1
    map_width = max(y for x, y in map["walls"]) + 1
    for x, y in map["walls"] :
        new_map["walls"].append((x, y))
    for x, y in map["blizzards"] :
        for dir in map["blizzards"][(x, y)] :
            if dir == "^" :
                if (x - 1, y) not in map["walls"] :
                    new_map["blizzards"][(x - 1, y)] = new_map["blizzards"].get((x - 1, y), []) + [dir]
                else :
                    new_map["blizzards"][(x + map_height - 3, y)] = new_map["blizzards"].get((x + map_height - 3, y), []) + [dir]
            elif dir == "v" :
                if (x + 1, y) not in map["walls"] :
                    new_map["blizzards"][(x + 1, y)] = new_map["blizzards"].get((x + 1, y), []) + [dir]
                else :
                    new_map["blizzards"][(x - map_height + 3, y)] = new_map["blizzards"].get((x - map_height + 3, y), []) + [dir]
            elif dir == "<" :
                if (x, y - 1) not in map["walls"] :
                    new_map["blizzards"][(x, y - 1)] = new_map["blizzards"].get((x, y - 1), []) + [dir]
                else :
                    new_map["blizzards"][(x, y + map_width - 3)] = new_map["blizzards"].get((x, y + map_width - 3), []) + [dir]
            elif dir == ">" :
                if (x, y + 1) not in map["walls"] :
                    new_map["blizzards"][(x, y + 1)] = new_map["blizzards"].get((x, y + 1), []) + [dir]
                else :
                    new_map["blizzards"][(x, y - map_width + 3)] = new_map["blizzards"].get((x, y - map_width + 3), []) + [dir]
    
    for x, y in map["flood"] :
        if x > 0 and (x-1, y) not in new_map["walls"] and (x-1, y) not in new_map["blizzards"] and (x-1, y) not in new_map["flood"] :
            new_map["flood"].append((x-1, y))
        if x < map_height-1 and (x+1, y) not in new_map["walls"] and (x+1, y) not in new_map["blizzards"] and (x+1, y) not in new_map["flood"] :
            new_map["flood"].append((x+1, y))
        if y > 0 and (x, y-1) not in new_map["walls"] and (x, y-1) not in new_map["blizzards"] and (x, y-1) not in new_map["flood"] :
            new_map["flood"].append((x, y-1))
        if y < map_width-1 and (x, y+1) not in new_map["walls"] and (x, y+1) not in new_map["blizzards"] and (x, y+1) not in new_map["flood"] :
            new_map["flood"].append((x, y+1))
        if (x, y) not in new_map["blizzards"] :
            new_map["flood"].append((x, y))
    
    return new_map

if __name__ == "__main__" :
    map = parse_input("input")
    map_height = max(x for x, y in map["walls"]) + 1
    map_width = max(y for x, y in map["walls"]) + 1
    start = (0, 1)
    end = (map_height-1, map_width - 2)

    i = 0
    goal = end
    while True :
        if i % 10 == 0 :
            print(f"Round {i+1}")
            print_map(map)
        map = round(map)
        i += 1
        if goal in map["flood"] :
            break
    
    part_1 = i


    map["flood"] = [end]
    goal = start
    while True :
        if i % 10 == 0 :
            print(f"Round {i+1}")
            print_map(map)
        map = round(map)
        i += 1
        if goal in map["flood"] :
            break
    
    print(f"Back again")

    map["flood"] = [start]
    goal = end
    while True :
        if i % 10 == 0 :
            print(f"Round {i+1}")
            print_map(map)
        map = round(map)
        i += 1
        if goal in map["flood"] :
            break

    part_2 = i


    print(f"Part 1: {part_1}")
    print(f"Part 2: {part_2}")
