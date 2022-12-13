from pathlib import Path
input_file = Path(__file__).parent / "input"

def parse_input ( input_file = input_file ) :
    with open(input_file, "r") as f :
        data = f.read().splitlines()
    data = [ line.split() for line in data ]
    return data

def calculate_history ( data, debug = False ) :
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

    return history

def calculate_signal_strength ( history, debug = False ) :
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

def render_history ( history, debug = False ) :
    screen = ""
    for cycle in range(1, history[-1][0] + 1) :
        signal = [x for x in history if x[0] <= cycle][-1]
        x = signal[2] if signal[0] == cycle else signal[3]
        x_pos = (cycle - 1) % 40
        if debug :
            print(f"X at {cycle}: {x} | {x_pos}")
        screen += "#" if x >= x_pos-1 and x <= x_pos+1 else "."
        if x_pos == 39 :
            screen += "\n"
        if debug :
            print(f"Screen at {cycle}:")
            print(screen)
    return screen

if __name__ == "__main__" :
    data = parse_input(Path(__file__).parent / "test")
    history = calculate_history(data)
    signal_strength = calculate_signal_strength(history)
    if signal_strength != 13140 :
        raise Exception(f"Test failed: {signal_strength}")
    screen = render_history(history)
    if screen != (
      "##..##..##..##..##..##..##..##..##..##..\n"
      "###...###...###...###...###...###...###.\n"
      "####....####....####....####....####....\n"
      "#####.....#####.....#####.....#####.....\n"
      "######......######......######......####\n"
      "#######.......#######.......#######.....\n"
    ) :
        raise Exception(f"Test failed: {screen}")
    
    data = parse_input()
    history = calculate_history(data)
    signal_strength = calculate_signal_strength(history)
    print(f"Part 1: Signal strength: {signal_strength}")

    screen = render_history(history)
    print(f"Part 2: Screen:")
    print(screen)
    print(screen.replace(".", " "))
