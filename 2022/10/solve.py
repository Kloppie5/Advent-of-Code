from pathlib import Path
input_file = Path(__file__).parent / "input"

def parse_input ( input_file = input_file ) :
    with open(input_file, "r") as f :
        data = f.read().splitlines()
    data = [ line.split() for line in data ]
    return data

def calculate_signal_strength ( data, debug = False ) :
    X = 1
    cycle = 0
    history = [(cycle, "init", X, X)]

    for line in data:
        if line[0] == "noop" :
            cycle += 1
            history.append((cycle, "noop", X, X))
        elif line[0] == "addx" :
            inc = int(line[1])
            cycle += 2
            history.append((cycle, "addx", X, X+inc))
            X += inc

    if debug :
        print("History:")
        for cycle, op, x, x2 in history :
            print(f"{cycle:3} {op:4} {x:3} {x2:3}")

    total_signal = 0
    for signal_index in range(20, 220 + 1, 40) :
        signal = [x for x in history if x[0] <= signal_index][-1]
        if debug :
            print(f"Signal at {signal_index}: {signal}")
        x = signal[2] if signal[0] == signal_index else signal[3]
        if debug :
            print(f"X at {signal_index}: {x}")
        total_signal += signal_index * x

    if debug :
        print(f"Total signal: {total_signal}")
    return total_signal

if __name__ == "__main__" :
    data = parse_input(Path(__file__).parent / "test")
    signal_strength = calculate_signal_strength(data)
    if signal_strength != 13140 :
        raise Exception(f"Test failed: {signal_strength}")
    
    data = parse_input()
    signal_strength = calculate_signal_strength(data)
    print(f"Part 1: Signal strength: {signal_strength}")
