import sys
sys.stdout.reconfigure(encoding='utf-8')

def parse_input ( filename ) :
    from pathlib import Path
    with open(Path(__file__).parent / filename, "r") as f :
        data = f.read().splitlines()
    
    map_data = data[:data.index("")]
    path_data = list(data[data.index("") + 1])

    map = {}
    for i, line in enumerate(map_data) :
        for j, char in enumerate(line) :
            if char != " " :
                map[(i+1, j+1)] = {"x": i+1, "y": j+1, "char": char}
    
    path = []
    while len(path_data) > 0 :
        R_index = path_data.index("R") if "R" in path_data else len(path_data)
        L_index = path_data.index("L") if "L" in path_data else len(path_data)
        if R_index == 0 :
            path.append(path_data.pop(0))
        elif L_index == 0 :
            path.append(path_data.pop(0))
        elif R_index == -1 and L_index == -1 :
            path.append(int("".join(path_data)))
            path_data = []
        else :
            path.append(int("".join(path_data.pop(0) for _ in range(min(max(R_index, 0), max(L_index, 0))))))

    return map, path

def wrap_map ( map ) :
    for x, y in map :
        if (x-1, y) in map :
            map[(x, y)]["^"] = (x-1, y)
        else :
            i = 0
            while (x+i+1, y) in map :
                i += 1
            map[(x, y)]["^"] = (x+i, y)
        if (x+1, y) in map :
            map[(x, y)]["v"] = (x+1, y)
        else :
            i = 0
            while (x-i-1, y) in map :
                i += 1
            map[(x, y)]["v"] = (x-i, y)
        if (x, y-1) in map :
            map[(x, y)]["<"] = (x, y-1)
        else :
            i = 0
            while (x, y+i+1) in map :
                i += 1
            map[(x, y)]["<"] = (x, y+i)
        if (x, y+1) in map :
            map[(x, y)][">"] = (x, y+1)
        else :
            i = 0
            while (x, y-i-1) in map :
                i += 1
            map[(x, y)][">"] = (x, y-i)

dir_cycle = [">", "v", "<", "^"]
def turn ( dir, turn ) :
    if turn == "R" :
        return dir_cycle[(dir_cycle.index(dir) + 1) % len(dir_cycle)]
    elif turn == "L" :
        return dir_cycle[(dir_cycle.index(dir) - 1) % len(dir_cycle)]
    
def walk_map ( map, path, start ) :
    x, y, dir = start
    for step in path :
        if step == "R" or step == "L" :
            dir = turn(dir, step)
        else :
            for _ in range(step) :
                target = map[(x, y)][dir]
                map[(x, y)]["char"] = dir
                if map[target]["char"] != "#" :
                    x, y = target            
    return (x, y, dir)

def print_map ( map ) :
    width = max(x for x, y in map) + 1
    height = max(y for x, y in map) + 1
    screen = [[" " for _ in range(height)] for _ in range(width)]
    for x, y in map :
        screen[x][y] = map[(x, y)]["char"]
    for line in screen :
        print("".join(line))

def password ( point ) :
    x, y, dir = point
    return x * 1000 + y * 4 + dir_cycle.index(dir)

if __name__ == "__main__" :
    map, path = parse_input("input")

    wrap_map(map)
    
    end_1 = walk_map(map, path, (1, min(y for x, y in map if x == 1), '>'))
    password_1 = password(end_1)

    print_map(map)
    
    print(f"Part 1: {end_1} -> {password_1}")
