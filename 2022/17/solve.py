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

def drop_block ( map, block_type, jets, step, debug = [] ) :
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
        jet = jets[step%len(jets)]
        step += 1
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
    return step

def drop_blocks ( map, blocks, jets, debug = [] ) :

    heights = [[0, 0, 0, 0, 0]]
    steps = [[0, 0, 0, 0, 0]]
    diffs = [[0, 0, 0, 0, 0]]
    
    step = 0
    period = (-1, -1)
    for block in range(blocks) :
        step = drop_block(map, block%5, jets, step, debug)

        heights[block//5][block%5] = len(map)-1
        steps[block//5][block%5] = step%len(jets)
        diffs[block//5][block%5] = heights[block//5][block%5] - heights[block//5-1][block%5]
        
        if block%5 == 4 :
            # check for repeating pattern
            for offset in range(len(heights)) :
                length = len(heights)-offset-1
                if length == 0 :
                    continue
                if steps[offset] == steps[offset+length] and diffs[offset] == diffs[offset+length] :
                    period = (offset, length)
                    break
            else :
                heights.append([0, 0, 0, 0, 0])
                steps.append([0, 0, 0, 0, 0])
                diffs.append([0, 0, 0, 0, 0])
                continue
            break
    else :
        return heights[blocks//5][blocks%5]
    
    blocks -= 1
    
    full_period_length = 0
    for i in range(period[1]) :
        full_period_length += diffs[period[0]+i][0]
    
    cycles = (blocks//5 - period[0])//period[1]
    remaining = blocks - cycles*period[1]*5
    base_height = heights[remaining//5][remaining%5]
    
    print(f"Period: {period}")
    print(f"Full period length: {full_period_length}")
    print(f"Cycles: {cycles}")
    print(f"Remaining: {remaining}")
    print(f"Base height: {base_height}")
    print(f"Cycle height: {cycles*full_period_length}")
    print(heights)

    total_height = base_height + cycles*full_period_length
    
    return total_height

def print_map ( map ) :
    for line in map[::-1] :
        print(line)

if __name__ == "__main__" :
    debug = ["jets", "falling", "map"]
    debug = []
    
    jets = parse_input("input", debug)

    map = ['+-------+']
    height_1 = drop_blocks(map, 2022, jets, debug)

    map = ['+-------+']
    height_2 = drop_blocks(map, 1000000000000, jets, debug)

    print(f"Part 1: {height_1}")
    print(f"Part 2: {height_2}")
