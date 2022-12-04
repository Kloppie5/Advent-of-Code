from pathlib import Path
input_file = Path(__file__).parent / "input"

def parse_input ( debug = False ) :
    with open(input_file, "r") as f:
        data = f.read().splitlines()
    return data

if __name__ == "__main__":
    rucksacks = parse_input()
    
    total_priority = 0
    for rucksack in rucksacks:
        left_compartment, right_compartment = rucksack[:(len(rucksack)-1)//2+1], rucksack[(len(rucksack)-1)//2+1:]
        # find letter in both
        matching_letter = None
        for letter in left_compartment:
            if letter in right_compartment:
                matching_letter = letter
                break
        else:
            print("No matching letter found")
    
        priority = ord(matching_letter) - 38 if matching_letter.isupper() else ord(matching_letter) - 96
        total_priority += priority
    print(f"Part 1: total priority is {total_priority}")
