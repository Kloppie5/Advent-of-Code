import sys
sys.stdout.reconfigure(encoding='utf-8')

def parse_input ( filename ) :
    from pathlib import Path
    with open(Path(__file__).parent / filename, "r") as f :
        data = f.read().splitlines()
    data = [int(x) for x in data]
    return data

# Encryption moves every number forward by their value, in their original order
# Decryption therefore moves what number would reach the target position by moving
#  backwards by their value
# I'm an idiot; I just need to mix it once
def mix ( data, rounds ) :
    mutation_table = [i for i in range(len(data))]
    for r in range(rounds) :
        for i, value in enumerate(data) :
            index = mutation_table.index(i)
            mutation_table.pop(index)
            mutation_table.insert((index + value) % len(mutation_table), i)
    return [data[x] for x in mutation_table]

if __name__ == "__main__" :
    raw_data = parse_input("input")
    
    data = raw_data.copy()
    mixed = mix(data, 1)
    zero_index = mixed.index(0)
    print(f"Part 1: ({mixed[(zero_index + 1000)%len(mixed)]}, {mixed[(zero_index + 2000)%len(mixed)]}, {mixed[(zero_index + 3000)%len(mixed)]}) = {mixed[(zero_index + 1000)%len(mixed)] + mixed[(zero_index + 2000)%len(mixed)] + mixed[(zero_index + 3000)%len(mixed)]}")

    data = raw_data.copy()
    data = [data[i] * 811589153 for i in range(len(data))]
    mixed = mix(data, 10)
    zero_index = mixed.index(0)
    print(f"Part 2: ({mixed[(zero_index + 1000)%len(mixed)]}, {mixed[(zero_index + 2000)%len(mixed)]}, {mixed[(zero_index + 3000)%len(mixed)]}) = {mixed[(zero_index + 1000)%len(mixed)] + mixed[(zero_index + 2000)%len(mixed)] + mixed[(zero_index + 3000)%len(mixed)]}")
