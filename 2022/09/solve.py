from pathlib import Path
input_file = Path(__file__).parent / "input"

def parse_input ( debug = False ) :
    with open(input_file, "r") as f :
        data = f.read().splitlines()
    data = [ line.split() for line in data ]
    return data

def mark_map ( data, debug = False ) :
    hx = 0
    hy = 0
    tx = 0
    ty = 0
    marks = {0:[0]}
    for line in data:
        if debug :
            print(f"H({hx},{hy}) | T({tx},{ty}) | {line}")
        if line[0] == "U" :
            for i in range(int(line[1])) :
                if hy - ty == 1 :
                    tx = hx
                    ty = hy
                    if tx in marks :
                        marks[tx].append(ty)
                    else :
                        marks[tx] = [ty]
                    if debug :
                        print(f"Marked {tx},{ty}")
                hy += 1            
        elif line[0] == "D" :
            for i in range(int(line[1])) :
                if ty - hy == 1 :
                    tx = hx
                    ty = hy
                    if tx in marks :
                        marks[tx].append(ty)
                    else :
                        marks[tx] = [ty]
                    if debug :
                        print(f"Marked {tx},{ty}")
                hy -= 1
        elif line[0] == "L" :
            for i in range(int(line[1])) :
                if tx - hx == 1 :
                    tx = hx
                    ty = hy
                    if tx in marks :
                        marks[tx].append(ty)
                    else :
                        marks[tx] = [ty]
                    if debug :
                        print(f"Marked {tx},{ty}")
                hx -= 1
        elif line[0] == "R" :
            for i in range(int(line[1])) :
                if hx - tx == 1 :
                    tx = hx
                    ty = hy
                    if tx in marks :
                        marks[tx].append(ty)
                    else :
                        marks[tx] = [ty]
                    if debug :
                        print(f"Marked {tx},{ty}")
                hx += 1
        else :
            print("ERROR")
            exit(1)
    return marks

def deduplicate_marks ( marks ) :
    for x in marks :
        marks[x] = list(set(marks[x]))
    return marks

def print_map_to_file ( marks ) :
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
    with open(Path(__file__).parent / "map.txt", "w") as f :
        for line in map :
            f.write("".join(line) + "\n")

if __name__ == "__main__" :
    data = parse_input()

    marks = mark_map(data)
    marks = deduplicate_marks(marks)
    print_map_to_file(marks)
    mark_count = sum([ len(marks[x]) for x in marks ])
    print(f"Marked {mark_count} locations")
