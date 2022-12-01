from pathlib import Path
input_file = Path(__file__).parent / "input"

def parse_input ( debug = False ) :
    with open(input_file, "r") as f:
        data = f.read().splitlines()
    
    result = []
    elf = []
    for line in data:
        if debug : print(f"Line: \"{line}\"")
        if line == '' :
            if debug : print(f"End of Elf; {elf}")
            result.append(elf)
            elf = []
            continue
        elf.append(line.strip())
    if elf != [] :
        if debug : print(f"End of File; {elf}")
        result.append(elf)
    
    return result

def total_calories_for_elf ( elf ) :
    return sum([ int(x) for x in elf ])

if __name__ == "__main__":
    elves = parse_input()

    total_calories = [ total_calories_for_elf(elf) for elf in elves ]
    most_calories = max(total_calories)
    print(f"Part 1: {most_calories}")

    sorted_calories = sorted(total_calories)
    top_3 = sorted_calories[-3:]
    sum_of_top_3 = sum(top_3)
    print (f"Part 2: {sum_of_top_3}")
