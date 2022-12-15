import sys
sys.stdout.reconfigure(encoding='utf-8')

def parse_input ( filename ) :
    from pathlib import Path
    with open(Path(__file__).parent / filename, "r") as f :
        data = f.read().splitlines()
    data = [[i for i in line] for line in data]

    S = (0, 0)
    E = (0, 0)
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == "S":
                S = (i, j)
            elif data[i][j] == "E":
                E = (i, j)
    
    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] = {
              "letter" : data[i][j],
              "height" : ord(data[i][j]) - 97,
              "i" : i,
              "j" : j
            }
    
    data[S[0]][S[1]]["height"] = ord('a') - 97
    data[E[0]][E[1]]["height"] = ord('z') - 97 # Had 26 instead of 25; dont use magic numbers

    return data, S, E

def calculate_directions ( heightmap ) :
    for i in range(len(heightmap)):
        for j in range(len(heightmap[i])):
            heightmap[i][j]["up"] = i > 0 and heightmap[i-1][j]["height"] <= heightmap[i][j]["height"] + 1
            heightmap[i][j]["down"] = i < len(heightmap) - 1 and heightmap[i+1][j]["height"] <= heightmap[i][j]["height"] + 1
            heightmap[i][j]["left"] = j > 0 and heightmap[i][j-1]["height"] <= heightmap[i][j]["height"] + 1
            heightmap[i][j]["right"] = j < len(heightmap[i]) - 1 and heightmap[i][j+1]["height"] <= heightmap[i][j]["height"] + 1

def print_heightmap_directions ( heightmap ) :
    boi_characters = [
      "╳", # 
      "╺", #  R
      "╸", # L
      "━", # LR
      "╻", #   D
      "┏", #  RD
      "┓", # L D
      "┳", # LRD
      "╹", #    U
      "┗", #  R U
      "┛", # L  U
      "┻", # LR U
      "┃", #   DU
      "┣", #  RDU
      "┫", # L DU
      "╋", # LRDU
    ]
    for i in range(len(heightmap)):
        for j in range(len(heightmap[i])):
            character = heightmap[i][j]["up"] * 8 + heightmap[i][j]["down"] * 4 + heightmap[i][j]["left"] * 2 + heightmap[i][j]["right"]
            print(boi_characters[character], end="")
        print()

def calculate_distances ( heightmap, queue ) :
    while len(queue) > 0:
        (i, j) = queue.pop(0)
        if heightmap[i][j]["up"] and i > 0 and "distance" not in heightmap[i-1][j]:
            heightmap[i-1][j]["distance"] = heightmap[i][j]["distance"] + 1
            queue.append((i-1, j))
        if heightmap[i][j]["down"] and i < len(heightmap) - 1 and "distance" not in heightmap[i+1][j]:
            heightmap[i+1][j]["distance"] = heightmap[i][j]["distance"] + 1
            queue.append((i+1, j))
        if heightmap[i][j]["left"] and j > 0 and "distance" not in heightmap[i][j-1]:
            heightmap[i][j-1]["distance"] = heightmap[i][j]["distance"] + 1
            queue.append((i, j-1))
        if heightmap[i][j]["right"] and j < len(heightmap[i]) - 1 and "distance" not in heightmap[i][j+1]:
            heightmap[i][j+1]["distance"] = heightmap[i][j]["distance"] + 1
            queue.append((i, j+1))

def calculate_distances_to_start ( heightmap, S ) :
    queue = [S]
    heightmap[S[0]][S[1]]["distance"] = 0
    calculate_distances(heightmap, queue)

def calculate_distances_to_any_a ( heightmap ) :
    queue = []
    for i in range(len(heightmap)):
        for j in range(len(heightmap[i])):
            if heightmap[i][j]["height"] == 0:
                heightmap[i][j]["distance"] = 0
                queue.append((i, j))
    calculate_distances(heightmap, queue)

def print_heightmap_distances ( heightmap ) :
    for i in range(len(heightmap)):
        for j in range(len(heightmap[i])):
            print(f"{heightmap[i][j]['distance'] if 'distance' in heightmap[i][j] else 'iii':3} ", end="")
        print()

def print_heightmap_path ( heightmap, E ) :
    screen = [[' ' for i in range(len(heightmap[0]))] for j in range(len(heightmap))]
    i, j = E
    distance = heightmap[i][j]["distance"]
    screen[i][j] = "E"
    while distance > 0:
        if i > 0 and heightmap[i-1][j]["distance"] == distance - 1:
            i -= 1
            screen[i][j] = "v"
        elif i < len(heightmap) - 1 and heightmap[i+1][j]["distance"] == distance - 1:
            i += 1
            screen[i][j] = "^"
        elif j > 0 and heightmap[i][j-1]["distance"] == distance - 1:
            j -= 1
            screen[i][j] = ">"
        elif j < len(heightmap[i]) - 1 and heightmap[i][j+1]["distance"] == distance - 1:
            j += 1
            screen[i][j] = "<"
        distance -= 1

    for i in range(len(screen)):
        print("".join(screen[i]))

if __name__ == "__main__" :
    heightmap, S, E = parse_input("input")
    calculate_directions(heightmap)
    print_heightmap_directions(heightmap)
    
    calculate_distances_to_start(heightmap, S)
    print_heightmap_distances(heightmap)

    print_heightmap_path(heightmap, E)

    print(f"Part 1: {heightmap[E[0]][E[1]]['distance']}")

    ## ----

    heightmap, S, E = parse_input("input")
    calculate_directions(heightmap)
    print_heightmap_directions(heightmap)
    
    calculate_distances_to_any_a(heightmap)
    print_heightmap_distances(heightmap)

    print_heightmap_path(heightmap, E)

    print(f"Part 2: {heightmap[E[0]][E[1]]['distance']}")
