from pathlib import Path
input_file = Path(__file__).parent / "input"

def parse_input ( debug = False ) :
    with open(input_file, "r") as f :
        data = f.read().splitlines()
    data = [ line.split() for line in data ]
    return data

def follow_point ( tx, ty, hx, hy, debug = [] ) :
    if "follow_point" in debug :
        print(f"Follow point; ({tx},{ty}) follows ({hx},{hy})")
    if hy - ty == 2 : # Up
        if hx - tx < 0 : ## Left
            return tx - 1, ty + 1
        if hx - tx == 0 : ## Up
            return tx, ty + 1
        if hx - tx > 0 : ## Right
            return tx + 1, ty + 1
    if hy - ty == -2 : # Down
        if hx - tx < 0 : ## Left
            return tx - 1, ty - 1
        if hx - tx == 0 : ## Down
            return tx, ty - 1
        if hx - tx > 0 : ## Right
            return tx + 1, ty - 1
    if hx - tx == 2 : # Right
        if hy - ty < 0 : ## Up
            return tx + 1, ty - 1
        if hy - ty == 0 : ## Right
            return tx + 1, ty
        if hy - ty > 0 : ## Down
            return tx + 1, ty + 1
    if hx - tx == -2 : # Left
        if hy - ty < 0 : ## Up
            return tx - 1, ty - 1
        if hy - ty == 0 : ## Left
            return tx - 1, ty
        if hy - ty > 0 : ## Down
            return tx - 1, ty + 1
    return tx, ty # No change

def update_knots ( knots, hx, hy ) :
    tx = hx
    ty = hy
    for i in range(len(knots)) :
        knots[i] = follow_point(knots[i][0], knots[i][1], tx, ty)
        tx = knots[i][0]
        ty = knots[i][1]
    return knots

def mark_map ( data, knot_count, debug = False ) :
    hx = 0
    hy = 0
    knots = [ (0,0) for i in range(knot_count) ]
    marks = {0:[0]}

    for line in data:
        if line[0] == "U" :
            for i in range(int(line[1])) :
                hy += 1
                knots = update_knots(knots, hx, hy)
                marks[knots[-1][0]] = marks.get(knots[-1][0], []) + [knots[-1][1]]
        elif line[0] == "D" :
            for i in range(int(line[1])) :
                hy -= 1
                knots = update_knots(knots, hx, hy)
                marks[knots[-1][0]] = marks.get(knots[-1][0], []) + [knots[-1][1]]
        elif line[0] == "L" :
            for i in range(int(line[1])) :
                hx -= 1
                knots = update_knots(knots, hx, hy)
                marks[knots[-1][0]] = marks.get(knots[-1][0], []) + [knots[-1][1]]
        elif line[0] == "R" :
            for i in range(int(line[1])) :
                hx += 1
                knots = update_knots(knots, hx, hy)
                marks[knots[-1][0]] = marks.get(knots[-1][0], []) + [knots[-1][1]]
        else :
            print("ERROR")
            exit(1)
    return marks

def deduplicate_marks ( marks ) :
    for x in marks :
        marks[x] = list(set(marks[x]))
    return marks

def print_map_to_file ( marks, filename ) :
    min_x = min(marks.keys())
    max_x = max(marks.keys())
    min_y = min([ min(marks[x]) for x in marks ])
    max_y = max([ max(marks[x]) for x in marks ])
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    map = [ [ '.' for x in range(width) ] for y in range(height) ]
    for x in marks :
        for y in marks[x] :
            map[y - min_y][x - min_x] = '#'
    with open(Path(__file__).parent / filename, "w") as f :
        for line in map :
            f.write("".join(line) + "\n")

if __name__ == "__main__" :
    data = parse_input()

    marks = mark_map(data, 1)
    marks = deduplicate_marks(marks)
    print_map_to_file(marks, "map_1.txt")
    mark_count = sum([ len(marks[x]) for x in marks ])
    print(f"Part 1: Marked {mark_count} locations")

    marks = mark_map(data, 9)
    marks = deduplicate_marks(marks)
    print_map_to_file(marks, "map_9.txt")
    mark_count = sum([ len(marks[x]) for x in marks ])
    print(f"Part 2: Marked {mark_count} locations")
