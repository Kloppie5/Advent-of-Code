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

def surface_area ( droplets ) :
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

if __name__ == "__main__" :
    debug = []
    
    test_data = parse_input("test", debug)
    test_surface_area = surface_area(test_data)
    if test_surface_area != 64 :
        raise Exception(f"Test failed: {test_surface_area} != 64")

    data = parse_input("input", debug)
    data = surface_area(data)
    print(f"Part 1: {data}")
