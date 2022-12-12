from pathlib import Path
input_file = Path(__file__).parent / "input"

def parse_input ( debug = False ) :
    with open(input_file, "r") as f :
        data = f.read().splitlines()
    return data

def print_map ( map ) :
    for row in map :
        print("".join(row))

def create_vision_map ( data, debug = False ) :
    width = len(data[0])
    height = len(data)
    vision_map = [ [ '-' for i in range(width) ] for j in range(height)]

    # Top
    for i in range(width) :
        current_height = -1
        for j in range(height) :
            tree_height = int(data[j][i])
            if tree_height > current_height :
                current_height = tree_height
                vision_map[j][i] = "#"
    # Left
    for j in range(height) :
        current_height = -1
        for i in range(width) :
            tree_height = int(data[j][i])
            if tree_height > current_height :
                current_height = tree_height
                vision_map[j][i] = "#"
    # Right
    for j in range(height) :
        current_height = -1
        for i in range(width - 1, -1, -1) :
            tree_height = int(data[j][i])
            if tree_height > current_height :
                current_height = tree_height
                vision_map[j][i] = "#"
    # Bottom
    for i in range(width) :
        current_height = -1
        for j in range(height - 1, -1, -1) :
            tree_height = int(data[j][i])
            if tree_height > current_height :
                current_height = tree_height
                vision_map[j][i] = "#"
  
    return vision_map

if __name__ == "__main__":
    data = parse_input()

    vision_map = create_vision_map(data)
    print_map(vision_map)

    visible_trees = sum([ row.count("#") for row in vision_map ])
    print(f"Part 1: {visible_trees}")
