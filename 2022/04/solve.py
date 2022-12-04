from pathlib import Path
input_file = Path(__file__).parent / "input"

def parse_input ( debug = False ) :
    with open(input_file, "r") as f:
        data = f.read().splitlines()
    data = [line.split(',') for line in data]
    data = [[assignment.split('-') for assignment in line] for line in data]
    data = [[[int(assignment[0]), int(assignment[1])] for assignment in line] for line in data]
    return data

if __name__ == "__main__":
    assignments = parse_input()
    
    complete_overlaps = 0
    for assignment in assignments :
        if assignment[0][0] <= assignment[1][0] <= assignment[0][1] and assignment[0][0] <= assignment[1][1] <= assignment[0][1] :
            complete_overlaps += 1
        elif assignment[1][0] <= assignment[0][0] <= assignment[1][1] and assignment[1][0] <= assignment[0][1] <= assignment[1][1] :
            complete_overlaps += 1
    
    print(f"Part 1: {complete_overlaps} overlaps")

    overlaps = 0
    for assignment in assignments :
        if assignment[0][0] <= assignment[1][0] <= assignment[0][1] or assignment[0][0] <= assignment[1][1] <= assignment[0][1] :
            overlaps += 1
        elif assignment[1][0] <= assignment[0][0] <= assignment[1][1] or assignment[1][0] <= assignment[0][1] <= assignment[1][1] :
            overlaps += 1

    print(f"Part 2: {overlaps} overlaps")
