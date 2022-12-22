import sys
sys.stdout.reconfigure(encoding='utf-8')

import math

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

def connect_map ( map ) :
    edges = []
    for x, y in map :
        if (x-1, y) in map :
            map[(x, y)]["^"] = (x-1, y, "^")
        else :
            edges.append((x, y, "^"))
        if (x+1, y) in map :
            map[(x, y)]["v"] = (x+1, y, "v")
        else :
            edges.append((x, y, "v"))
        if (x, y-1) in map :
            map[(x, y)]["<"] = (x, y-1, "<")
        else :
            edges.append((x, y, "<"))
        if (x, y+1) in map :
            map[(x, y)][">"] = (x, y+1, ">")
        else :
            edges.append((x, y, ">"))
    return edges

def wrap_map ( map, edges ) :
    for x, y, dir in edges :
        if dir == "^" :
            i = 0
            while (x+i+1, y) in map :
                i += 1
            map[(x, y)]["^"] = (x+i, y, "^")
      
        if dir == "v" :
            i = 0
            while (x-i-1, y) in map :
                i += 1
            map[(x, y)]["v"] = (x-i, y, "v")
      
        if dir == "<" :
            i = 0
            while (x, y+i+1) in map :
                i += 1
            map[(x, y)]["<"] = (x, y+i, "<")
      
        if dir == ">" :
            i = 0
            while (x, y-i-1) in map :
                i += 1
            map[(x, y)][">"] = (x, y-i, ">")

def cube_wrap_map ( map, edges ) :
    map_height = max(x for x, y in map) + 1
    map_width = max(y for x, y in map) + 1
    grid_size = math.ceil(math.sqrt(len(map) // 6))

    edge_stack = []
    inwards_corners = []
    edge = edges[0]
    outwards_edges = 0
    while len(edge_stack) < len(edges) :
        edge_stack.append(edge)
        outwards_edges += 1
        x, y, dir = edge
        # Cant be arsed to make the x and y offsets directly dependend on the direction
        if dir == "^" :
            tries = [((x-1)%map_height, (y+1)%map_width, "<"), (x, (y+1)%map_width, "^"), (x, y, ">")]
        elif dir == "v" :
            tries = [((x+1)%map_height, (y-1)%map_width, ">"), (x, (y-1)%map_width, "v"), (x, y, "<")]
        elif dir == "<" :
            tries = [((x-1)%map_height, (y-1)%map_width, "v"), ((x-1)%map_height, y, "<"), (x, y, "^")]
        elif dir == ">" :
            tries = [((x+1)%map_height, (y+1)%map_width, "^"), ((x+1)%map_height, y, ">"), (x, y, "v")]
        else :
            raise Exception(f"Invalid direction {dir}")
        
        for i, try_edge in enumerate(tries) :
            if try_edge in edges :
                if i == 0 :
                    inwards_corners.append((try_edge, outwards_edges))
                    outwards_edges = 0
                edge = try_edge
                break
        else :
            raise Exception(f"Could not find edge for ({x}, {y}, {dir})")
    inwards_corners[0] = (inwards_corners[0][0], inwards_corners[0][1] + outwards_edges)
    
    while len(inwards_corners) > 0 :
        smallest_corner = min(size for _, size in inwards_corners)
        smallest_distance = smallest_corner // 2
        smallest_distance -= smallest_distance % grid_size
        if smallest_distance < grid_size :
            print("Smallest distance is too small, merging corners")
            too_short = [(corner, size) for corner, size in inwards_corners if size == smallest_corner][0]
            next_corner = inwards_corners[inwards_corners.index(too_short) + 1]
            inwards_corners[inwards_corners.index(too_short) + 1] = (next_corner[0], next_corner[1] + too_short[1])
            inwards_corners.remove(too_short)
            print(f"New corner {(next_corner[0], next_corner[1] + too_short[1])}, removed corner {too_short}")
            continue
        
        for i, (inner_corner, _) in enumerate(inwards_corners) :
            print(f"Folding corner {inner_corner}, distance {smallest_distance}")
            print(inwards_corners)
            print(edge_stack)
            for _ in range(smallest_distance) :
                left_index = (edge_stack.index(inner_corner) - 1) % len(edge_stack)
                right_index = edge_stack.index(inner_corner)
                next_index = (edge_stack.index(inner_corner) + 1) % len(edge_stack)
                edge1 = edge_stack[left_index]
                edge2 = edge_stack[right_index]
                next_edge = edge_stack[next_index]
                print(f"Connecting {edge1} and {edge2} [{left_index}, {right_index}, {next_index}]")
                map[(edge1[0], edge1[1])][edge1[2]] = (edge2[0], edge2[1], turn(edge2[2], "O"))
                map[(edge2[0], edge2[1])][edge2[2]] = (edge1[0], edge1[1], turn(edge1[2], "O"))
                edge_stack.remove(edge1)
                edge_stack.remove(edge2)
                if len(edge_stack) == 0 :
                    break
                inner_corner = next_edge
            inwards_corners[i] = (inner_corner, inwards_corners[i][1] - smallest_distance * 2)
        
        print(inwards_corners)
        for i, (inner_corner, size) in enumerate(inwards_corners) :
            if size == 0 :
                inwards_corners[(i+1) % len(inwards_corners)] = (inwards_corners[i][0], inwards_corners[(i+1) % len(inwards_corners)][1])
        print(inwards_corners)
        inwards_corners = [(corner, size) for corner, size in inwards_corners if size > 0]
    
dir_cycle = [">", "v", "<", "^"]
def turn ( dir, turn ) :
    if turn == "R" :
        return dir_cycle[(dir_cycle.index(dir) + 1) % len(dir_cycle)]
    elif turn == "L" :
        return dir_cycle[(dir_cycle.index(dir) - 1) % len(dir_cycle)]
    elif turn == "O" :
        return dir_cycle[(dir_cycle.index(dir) + 2) % len(dir_cycle)]
    else :
        raise Exception(f"Invalid turn: {turn}")
    
def walk_map ( map, path, start ) :
    x, y, dir = start
    for step in path :
        if step == "R" or step == "L" :
            dir = turn(dir, step)
        else :
            for _ in range(step) :
                map[(x, y)]["char"] = dir
                target = map[(x, y)][dir]
                if map[(target[0], target[1])]["char"] != "#" :
                    x, y, dir = target            
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

    edges = connect_map(map)
    wrap_map(map, edges)
    
    end_1 = walk_map(map, path, (1, min(y for x, y in map if x == 1), '>'))
    password_1 = password(end_1)

    print_map(map)
    
    map, path = parse_input("input")

    edges = connect_map(map)
    cube_wrap_map(map, edges)
    end_2 = walk_map(map, path, (1, min(y for x, y in map if x == 1), '>'))
    password_2 = password(end_2)

    print_map(map)

    print(f"Part 1: {end_1} -> {password_1}")
    print(f"Part 2: {end_2} -> {password_2}")
