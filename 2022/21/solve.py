import sys
sys.stdout.reconfigure(encoding='utf-8')

def parse_input ( filename ) :
    from pathlib import Path
    with open(Path(__file__).parent / filename, "r") as f :
        data = f.read().splitlines()
    
    monkeys = {}
    for line in data :
        line = line.split(" ")
        name = line[0][:-1]
        monkey = {}
        if len(line) == 2 :
            monkey["type"] = "number"
            monkey["value"] = int(line[1])
        elif len(line) == 4 :
            monkey["type"] = "operation"
            monkey["source_1"] = line[1]
            monkey["operation"] = line[2]
            monkey["source_2"] = line[3]
        else :
            raise Exception(f"Encountered unexpected line: {line}")
        monkeys[name] = monkey
    return monkeys

def calculate_root ( monkeys, debug = False ) :
    stack = ['root']
    values = {}
    while len(stack) > 0 :
        if debug :
            print(f"== Stack[{len(stack)}] == Values[{len(values)}] ==")
        name = stack.pop()
        monkey = monkeys[name]
        if debug :
            print(f"Calculating {name}; {monkey}")
        if name in values :
            if debug :
                print(f" < Already calculated {values[name]}")
            continue
        if monkey["type"] == "number" :
            if debug :
                print(f" < Number Monkey; {monkey['value']}")
            values[name] = monkey["value"]
            continue
        
        if monkey["source_1"] not in values or monkey["source_2"] not in values :
            if debug :
                print(f" < Not all sources calculated; pushing back onto stack")
            stack.append(name)
            stack.append(monkey["source_1"])
            stack.append(monkey["source_2"])
            continue
        
        if monkey["operation"] == "+" :
            if debug :
                print(f" < Addition Monkey; {values[monkey['source_1']]} + {values[monkey['source_2']]}")
            values[name] = values[monkey["source_1"]] + values[monkey["source_2"]]
        elif monkey["operation"] == "-" :
            if debug :
                print(f" < Subtraction Monkey; {values[monkey['source_1']]} - {values[monkey['source_2']]}")
            values[name] = values[monkey["source_1"]] - values[monkey["source_2"]]
        elif monkey["operation"] == "*" :
            if debug :
                print(f" < Multiplication Monkey; {values[monkey['source_1']]} * {values[monkey['source_2']]}")
            values[name] = values[monkey["source_1"]] * values[monkey["source_2"]]
        elif monkey["operation"] == "/" :
            if debug :
                print(f" < Division Monkey; {values[monkey['source_1']]} / {values[monkey['source_2']]}")
            values[name] = values[monkey["source_1"]] / values[monkey["source_2"]]
        else :
            raise Exception(f"Encountered unexpected operation: {monkey['operation']} in {monkey}")
    
    return values["root"]

if __name__ == "__main__" :
    monkeys = parse_input("input")

    result = calculate_root(monkeys)
    
    print(f"Part 1: {result}")
