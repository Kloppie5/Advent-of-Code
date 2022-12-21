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

def calculate_monkey ( monkeys, target, debug = False ) :
    stack = [target]
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
        elif monkey["operation"] == "=" :
            if debug :
                print(f" < Equality Monkey; {values[monkey['source_1']]} == {values[monkey['source_2']]}")
            values[name] = values[monkey["source_1"]] == values[monkey["source_2"]]
        else :
            raise Exception(f"Encountered unexpected operation: {monkey['operation']} in {monkey}")
    
    return values[target]

def reframe_monkeys ( monkeys, equality_monkey, input_monkey, debug = False ) :
    monkeys[equality_monkey]["operation"] = "="
    for monkey in monkeys.values() :
        monkey["input"] = False
    monkeys[input_monkey]["input"] = True
    def mark_inputs ( monkey ) :
        if monkey["type"] == "number" :
            return
        if monkey["type"] == "operation" :
            mark_inputs(monkeys[monkey["source_1"]])
            mark_inputs(monkeys[monkey["source_2"]])
            if monkeys[monkey["source_1"]]["input"] or monkeys[monkey["source_2"]]["input"] :
                monkey["input"] = True
    mark_inputs(monkeys[equality_monkey])

    target_monkey = equality_monkey
    while target_monkey != input_monkey :
        monkey = monkeys[target_monkey]
        if monkey["type"] != "operation" or monkey["operation"] != "=" :
            raise Exception(f"Encountered target_monkey monkey: {monkey}")
        
        if monkeys[monkey["source_1"]]["input"] and not monkeys[monkey["source_2"]]["input"] :
            target, constant = monkey["source_1"], monkey["source_2"]
        elif monkeys[monkey["source_2"]]["input"] and not monkeys[monkey["source_1"]]["input"] :
            target, constant = monkey["source_2"], monkey["source_1"]
        else :
            raise Exception(f"Encountered unexpected multi-input monkey: {monkey}")
        
        if monkeys[target]["type"] == "number" :
            monkeys[target] = monkeys[constant]
            break
        
        target_L, target_R = monkeys[target]["source_1"], monkeys[target]["source_2"]
        if monkeys[target_L]["input"] and not monkeys[target_R]["input"] :
            if monkeys[target]["operation"] == "+" :
                new_1, new_L, new_op, new_R = target_L, constant, "-", target_R
            elif monkeys[target]["operation"] == "-" :
                new_1, new_L, new_op, new_R = target_L, constant, "+", target_R
            elif monkeys[target]["operation"] == "*" :
                new_1, new_L, new_op, new_R = target_L, constant, "/", target_R
            elif monkeys[target]["operation"] == "/" :
                new_1, new_L, new_op, new_R = target_L, constant, "*", target_R
            else :
                raise Exception(f"Encountered unexpected input: {monkey}")
        elif monkeys[target_R]["input"] and not monkeys[target_L]["input"] :
            if monkeys[target]["operation"] == "+" :
                new_1, new_L, new_op, new_R = target_R, constant, "-", target_L
            elif monkeys[target]["operation"] == "-" :
                new_1, new_L, new_op, new_R = target_R, target_L, "-", constant
            elif monkeys[target]["operation"] == "*" :
                new_1, new_L, new_op, new_R = target_R, constant, "/", target_L
            elif monkeys[target]["operation"] == "/" :
                new_1, new_L, new_op, new_R = target_R, target_L, "/", constant
            else :
                raise Exception(f"Encountered unexpected input: {monkey}")
        else :
            raise Exception(f"Encountered unexpected input: {monkey}")
        
        if debug :
            print(f"Reframing {target_L} {monkeys[target]['operation']} {target_R} ({target}) ={target_monkey}= {constant} to {new_1} ={target}= ({target_monkey}) {new_L} {new_op} {new_R}")

        monkeys[target_monkey] = {
            "type" : "operation",
            "source_1" : new_L,
            "operation" : new_op,
            "source_2" : new_R,
            "input" : False
        }
        monkeys[target] = {
            "type" : "operation",
            "source_1" : new_1,
            "operation" : "=",
            "source_2" : target_monkey,
            "input" : True
        }
        target_monkey = target

if __name__ == "__main__" :
    monkeys = parse_input("input")

    result_1 = calculate_monkey(monkeys, 'root')

    reframe_monkeys(monkeys, 'root', 'humn')
    result_2 = calculate_monkey(monkeys, 'humn')
    
    print(f"Part 1: {result_1}")
    print(f"Part 2: {result_2}")
