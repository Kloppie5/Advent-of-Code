import sys
sys.stdout.reconfigure(encoding='utf-8')

def parse_input ( filename, debug = [] ) :
    if "functions" in debug :
        print(f"parse_input({filename})")
    from pathlib import Path
    with open(Path(__file__).parent / filename, "r") as f :
        data = f.read().splitlines()
    for i in range(len(data)) :
        x, y, z, = data[i].split(",")
        data[i] = (int(x), int(y), int(z))
    
    return data

def calculate_surface_area ( droplets ) :
    total_surface_area = 0
    checked_droplets = set()
    for droplet in droplets :
        if droplet in checked_droplets :
            print(f"  > Droplet {droplet} already checked")
            continue
        checked_droplets.add(droplet)
        total_surface_area += 6
        if (droplet[0], droplet[1], droplet[2] - 1) in droplets :
            total_surface_area -= 1
        if (droplet[0], droplet[1], droplet[2] + 1) in droplets :
            total_surface_area -= 1
        if (droplet[0], droplet[1] - 1, droplet[2]) in droplets :
            total_surface_area -= 1
        if (droplet[0], droplet[1] + 1, droplet[2]) in droplets :
            total_surface_area -= 1
        if (droplet[0] - 1, droplet[1], droplet[2]) in droplets :
            total_surface_area -= 1
        if (droplet[0] + 1, droplet[1], droplet[2]) in droplets :
            total_surface_area -= 1
    return total_surface_area

def find_bubbles ( droplets ) :
    min_x = min(droplet[0] for droplet in droplets)-1
    max_x = max(droplet[0] for droplet in droplets)+1
    min_y = min(droplet[1] for droplet in droplets)-1
    max_y = max(droplet[1] for droplet in droplets)+1
    min_z = min(droplet[2] for droplet in droplets)-1
    max_z = max(droplet[2] for droplet in droplets)+1

    queue = [(min_x, min_y, min_z)]
    outer_reachable = set()
    while len(queue) > 0 :
        droplet = queue.pop(0)
        print(f"  [{len(queue)}] > Checking {droplet}")
        if droplet in droplets :
            continue

        if droplet[0] > min_x and (droplet[0] - 1, droplet[1], droplet[2]) not in outer_reachable :
            queue.append((droplet[0] - 1, droplet[1], droplet[2]))
            outer_reachable.add((droplet[0] - 1, droplet[1], droplet[2]))
        if droplet[0] < max_x and (droplet[0] + 1, droplet[1], droplet[2]) not in outer_reachable :
            queue.append((droplet[0] + 1, droplet[1], droplet[2]))
            outer_reachable.add((droplet[0] + 1, droplet[1], droplet[2]))
        if droplet[1] > min_y and (droplet[0], droplet[1] - 1, droplet[2]) not in outer_reachable :
            queue.append((droplet[0], droplet[1] - 1, droplet[2]))
            outer_reachable.add((droplet[0], droplet[1] - 1, droplet[2]))
        if droplet[1] < max_y and (droplet[0], droplet[1] + 1, droplet[2]) not in outer_reachable :
            queue.append((droplet[0], droplet[1] + 1, droplet[2]))
            outer_reachable.add((droplet[0], droplet[1] + 1, droplet[2]))
        if droplet[2] > min_z and (droplet[0], droplet[1], droplet[2] - 1) not in outer_reachable :
            queue.append((droplet[0], droplet[1], droplet[2] - 1))
            outer_reachable.add((droplet[0], droplet[1], droplet[2] - 1))
        if droplet[2] < max_z and (droplet[0], droplet[1], droplet[2] + 1) not in outer_reachable :
            queue.append((droplet[0], droplet[1], droplet[2] + 1))
            outer_reachable.add((droplet[0], droplet[1], droplet[2] + 1))
        
    print(f"  > Outer reachable: {outer_reachable}")
    bubbles = []
    for x in range(min_x, max_x + 1) :
        for y in range(min_y, max_y + 1) :
            for z in range(min_z, max_z + 1) :
                if (x, y, z) not in droplets and (x, y, z) not in outer_reachable :
                    print(f"  > Bubble found: {x}, {y}, {z}")
                    droplets.append((x, y, z))
    return bubbles

if __name__ == "__main__" :
    debug = []
    
    test_data = parse_input("test", debug)
    test_surface_area = calculate_surface_area(test_data)
    if test_surface_area != 64 :
        raise Exception(f"Test failed: {test_surface_area} != 64")

    data = parse_input("input", debug)
    surface_area = calculate_surface_area(data)

    bubbles = find_bubbles(data)
    filled_surface_area = calculate_surface_area(data + bubbles)
    print(f"Part 1: {surface_area}")
    print(f"Part 2: {filled_surface_area}")
