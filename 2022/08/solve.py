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

def create_scenic_map ( data, debug = False ) :
    width = len(data[0])
    height = len(data)
    scenic_map = [ [ { "height" : int(data[j][i]), "x" : i, "y" : j } for i in range(width) ] for j in range(height)]

    # Top
    for i in range(width) :
        previous_tree = [-1]*10
        for j in range(height) :
            tree_height = scenic_map[j][i]["height"]
            for k in range(0, tree_height) :
                previous_tree[k] = 0
            for k in range(tree_height, 10) :
                previous_tree[k] += 1
            scenic_map[j][i]["top"] = previous_tree.copy()
            previous_tree[tree_height] = 0
    # Left
    for j in range(height) :
        previous_tree = [-1]*10
        for i in range(width) :
            tree_height = scenic_map[j][i]["height"]
            for k in range(0, tree_height) :
                previous_tree[k] = 0
            for k in range(tree_height, 10) :
                previous_tree[k] += 1
            scenic_map[j][i]["left"] = previous_tree.copy()
            previous_tree[tree_height] = 0
    # Right
    for j in range(height) :
        previous_tree = [-1]*10
        for i in range(width - 1, -1, -1) :
            tree_height = scenic_map[j][i]["height"]
            for k in range(0, tree_height) :
                previous_tree[k] = 0
            for k in range(tree_height, 10) :
                previous_tree[k] += 1
            scenic_map[j][i]["right"] = previous_tree.copy()
            previous_tree[tree_height] = 0
    # Bottom
    for i in range(width) :
        previous_tree = [-1]*10
        for j in range(height - 1, -1, -1) :
            tree_height = scenic_map[j][i]["height"]
            for k in range(0, tree_height) :
                previous_tree[k] = 0
            for k in range(tree_height, 10) :
                previous_tree[k] += 1
            scenic_map[j][i]["bottom"] = previous_tree.copy()
            previous_tree[tree_height] = 0
    
    # Scenic Scores
    for i in range(width) :
        for j in range(height) :
            tree_height = scenic_map[j][i]["height"]
            scenic_map[j][i]["scenic_score"]\
              = scenic_map[j][i]["top"][tree_height]\
              * scenic_map[j][i]["left"][tree_height]\
              * scenic_map[j][i]["right"][tree_height]\
              * scenic_map[j][i]["bottom"][tree_height]
    
    return scenic_map

if __name__ == "__main__":
    data = parse_input()

    vision_map = create_vision_map(data)
    print_map(vision_map)

    visible_trees = sum([ row.count("#") for row in vision_map ])
    print(f"Part 1: {visible_trees}")

    scenic_map = create_scenic_map(data)
    max_scenic_score = max([ max([ tree["scenic_score"] for tree in row ]) for row in scenic_map ])
    print(f"Part 2: {max_scenic_score}")
