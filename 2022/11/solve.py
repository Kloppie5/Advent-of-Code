
def parse_input ( filename ) :
    from pathlib import Path
    with open(Path(__file__).parent / filename, "r") as f :
        data = f.read().split("\n\n")
    # Parse
    # Monkey 0:
    # Starting items: 61
    # Operation: new = old * 11
    # Test: divisible by 5
    #   If true: throw to monkey 7
    #   If false: throw to monkey 4

    for i, d in enumerate(data) :
        lines = d.splitlines()
        data[i] = {}
        data[i]["monkey"] = int(lines[0].split()[1][:-1])
        data[i]["starting_items"] = [int(x) for x in lines[1].split(": ")[1].split(", ")]
        data[i]["operation"] = lines[2].split(": ")[1].split(" = ")[1].replace("old", "x")
        data[i]["test"] = int(lines[3].split(" ")[5])
        data[i]["if_true"] = int(lines[4].split(": ")[1].split(' ')[3])
        data[i]["if_false"] = int(lines[5].split(": ")[1].split(' ')[3])
        data[i]["activity"] = 0
    return data

def turn ( monkeys, index, stress_reduction, division_cap, debug = False ) :
    monkey = monkeys[index]
    if debug :
        print(f"Monkey {index}:")
    for i in range(len(monkey["starting_items"])) :
        worry = monkey["starting_items"].pop(0)
        if debug :
            print(f"  Monkey inspects an item with a worry level of {worry}.")
        worry = (eval(monkey["operation"], {"x":worry})) % division_cap
        if debug :
            print(f"    Monkey applies the operation. The worry level is now {worry}.")
        worry = worry // stress_reduction
        if debug :
            print(f"    :| Monkey gets bored easily. The worry level is now {worry}.")
        if worry % monkey["test"] == 0 :
            if debug :
                print(f"    :) Monkey is happy. The worry level is divisible by {monkey['test']}.")
            monkeys[monkey["if_true"]]["starting_items"].append(worry)
            if debug :
                print(f"    Monkey throws the item to monkey {monkey['if_true']}.")
        else :
            if debug :
                print(f"    :( Monkey is sad. The worry level is not divisible by {monkey['test']}.")
            monkeys[monkey["if_false"]]["starting_items"].append(worry)
            if debug :
                print(f"    Monkey throws the item to monkey {monkey['if_false']}.")
        monkey["activity"] += 1
    
def print_monkeys ( monkeys ) :
    for i, monkey in enumerate(monkeys) :
        print(f"Monkey {i}: [{monkey['activity']}] {monkey['starting_items']}")
    print()

def round ( monkeys, stress_reduction, division_cap, debug = False ) :
    for i in range(len(monkeys)) :
        turn(monkeys, i, stress_reduction, division_cap, debug)


if __name__ == "__main__" :
    monkeys = parse_input("input")
    print_monkeys(monkeys)
    division_cap = 1
    for monkey in monkeys :
        division_cap *= monkey["test"]

    for i in range(20) :
        round(monkeys, 3, division_cap)
        print_monkeys(monkeys)
    
    activity = sorted([monkey["activity"] for monkey in monkeys])
    print(f"Part 1: {activity[-2:]} = {activity[-2] * activity[-1]}")

    monkeys = parse_input("input")
    for i in range(10000) :
        if i % 100 == 0 :
            print(f"Round {i:5}: " + "|" * (i // 100) + "." * (100 - (i // 100)))
        round(monkeys, 1, division_cap)
    
    activity = sorted([monkey["activity"] for monkey in monkeys])
    print(f"Part 2: {activity[-2:]} = {activity[-2] * activity[-1]}")
