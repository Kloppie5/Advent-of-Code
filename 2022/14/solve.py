import sys
sys.stdout.reconfigure(encoding='utf-8')

def parse_input ( filename ) :
    from pathlib import Path
    with open(Path(__file__).parent / filename, "r") as f :
        data = f.read().splitlines()
    return data

def make_world ( paths, floor = False ) :
    walls = []
    for path in paths :
        points = path.split(" -> ")
        for i in range(len(points) - 1) :
            start_x, start_y = points[i].split(",")
            start_x, start_y = int(start_x), int(start_y)
            end_x, end_y = points[i+1].split(",")
            end_x, end_y = int(end_x), int(end_y)

            x_step = 1 if start_x <= end_x else -1
            for x in range(start_x, end_x + x_step, x_step) :
                y_step = 1 if start_y <= end_y else -1
                for y in range(start_y, end_y + y_step, y_step) :
                    walls += [(x, y)]

    width = max([wall[0] for wall in walls]) + 1
    height = max([wall[1] for wall in walls]) + 1 + 2
    world = [["." for x in range(width)] for y in range(height)]
    for wall in walls :
        world[wall[1]][wall[0]] = "#"
    if floor :
        world[height - 1] = "X" * width
    return world

def print_world ( world ) :
    for line in world :
        print("".join(line))

def add_sand ( world, pos ) :
    x, y = pos
    if world[y][x] == "o" :
        return False
    while y < len(world) - 1 :
        if x == len(world[y]) - 1 :
            print(f"Expanding world to the right")
            for i in range(y, len(world)-1) :
                world[i] += "."
            world[-1] += world[-1][-1]
        if world[y + 1][x] == "." :
            y += 1
        elif x > 0 and world[y + 1][x - 1] == "." :
            x -= 1
            y += 1
        elif x < len(world[y]) - 1 and world[y + 1][x + 1] == "." :
            x += 1
            y += 1
        else :
            world[y][x] = "o"
            return True
    return False

def fill_world ( world, source ) :
    while add_sand(world, source) :
        pass

if __name__ == "__main__" :
    paths = parse_input("input")

    world = make_world(paths)
    world[0][500] = "+"
    fill_world(world, (500, 0))
    print_world(world)
    print(f"Part 1: {sum([line.count('o') for line in world])}")
    
    world = make_world(paths, floor = True)
    world[0][500] = "+"
    fill_world(world, (500, 0))
    print_world(world)
    print(f"Part 2: {sum([line.count('o') for line in world])}")
