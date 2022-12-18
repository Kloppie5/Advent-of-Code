import sys
sys.stdout.reconfigure(encoding='utf-8')

def parse_input ( filename, debug = [] ) :
    if "functions" in debug :
        print(f"parse_input({filename})")
    from pathlib import Path
    with open(Path(__file__).parent / filename, "r") as f :
        raw_data = f.read().strip()
    if "input" in debug :
        print(f"  > Input: {raw_data}")
    return raw_data

def drop_block ( map, block_type, jets, debug = [] ) :
    # The tall, vertical chamber is exactly seven units wide. Each rock appears so that its left edge is two units away from the left wall and its bottom edge is three units above the highest rock in the room (or the floor, if there isn't one).
    map.append("|.......|")
    map.append("|.......|")
    map.append("|.......|")
    
    pos = len(map)

    if block_type == 0 :
        map.append("|..@@@@.|")
    elif block_type == 1 :
        map.append("|...@...|")
        map.append("|..@@@..|")
        map.append("|...@...|")
    elif block_type == 2 :
        map.append("|..@@@..|")
        map.append("|....@..|")
        map.append("|....@..|")
    elif block_type == 3 :
        map.append("|..@....|")
        map.append("|..@....|")
        map.append("|..@....|")
        map.append("|..@....|")
    elif block_type == 4 :
        map.append("|..@@...|")
        map.append("|..@@...|")
    else :
        raise Exception(f"Unknown block type: {block_type}")

    while True :
        jet = jets[0]
        jets = jets[1:] + jet
        if jet == '>' and not any("@#" in map[i] or "@|" in map[i] for i in range(pos, min(pos + 4, len(map)))) :
            if "jets" in debug :
                print(f"  > jet moves block right")
            for i in range(pos, min(pos + 4, len(map))) :
                newline = [c if c != '@' else '.' for c in map[i]]
                for j in range(1, 8) :
                    if map[i][j] == '@' :
                        newline[j + 1] = '@'
                map[i] = "".join(newline)
            if "map" in debug :
                print_map(map)
        elif jet == '<' and not any("#@" in map[i] or "|@" in map[i] for i in range(pos, min(pos + 4, len(map)))) :
            if "jets" in debug :
                print(f"  < jet moves block left")
            for i in range(pos, min(pos + 4, len(map))) :
                newline = [c if c != '@' else '.' for c in map[i]]
                for j in range(2, 9) :
                    if map[i][j] == '@' :
                        newline[j - 1] = '@'
                map[i] = "".join(newline)
            if "map" in debug :
                print_map(map)
        else :
            if "jets" in debug :
                print(f"  {jet} jet does nothing")
        
        if not any("#@" in map[i-1][j]+map[i][j] or "-@" in map[i-1][j]+map[i][j] for i in range(pos, min(pos + 4, len(map))) for j in range(1, 8)) :
            if "falling" in debug :
                print(f"  V block falls")
            for i in range(pos - 1, min(pos + 4 - 1, len(map) - 1)) :
                newline = [c if c != '@' else '.' for c in map[i]]
                for j in range(1, 8) :
                    if map[i+1][j] == '@' :
                        newline[j] = '@'
                map[i] = "".join(newline)
            map[min(pos + 4 - 1, len(map) - 1)] = map[min(pos + 4 - 1, len(map) - 1)].replace('@', '.')
            pos -= 1
            if "map" in debug :
                print_map(map)
        else :
            if "falling" in debug :
                print(f"  X block stops")
            for i in range(pos, min(pos + 4, len(map))) :
                map[i] = map[i].replace('@', '#')
            while map[-1] == "|.......|" :
                map.pop()
            break
    return jets

def print_map ( map ) :
    for line in map[::-1] :
        print(line)

if __name__ == "__main__" :
    debug = ["jets", "falling", "map"]
    debug = []
    
    jets = parse_input("input", debug)

    map = ['+-------+']

    for i in range(2022) :
        jets = drop_block(map, i%5, jets, debug)
    
    print_map(map)

    print(f"Total Blocks: {sum(line.count('#') for line in map)}")
    print(f"Total Height: {len(map)-1}")
