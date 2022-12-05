from pathlib import Path
input_file = Path(__file__).parent / "input"

def parse_input ( debug = False ) :
    with open(input_file, "r") as f :
        data = f.read().splitlines()
        stack_data, procedure_data = data[:data.index('')], data[data.index('')+1:]
    stack_count = int(stack_data[-1].strip().split(' ')[-1])
    stack_data = stack_data[:-1]

    stacks = [''] * stack_count
    for line in stack_data :
        for i in range(stack_count) :
            crate = line[i*4:i*4+3]
            if crate != '   ' :
                stacks[i] = crate[1] + stacks[i]

    procedures = []
    for line in procedure_data :
        line = line[5:]
        count, line = line.split(' from ', 1)
        src, dest = line.split(' to ', 1)
        procedures.append((int(count), int(src), int(dest)))
    
    return stacks, procedures

def print_stacks ( stacks ) :
    highest_stack = max([len(stack) for stack in stacks])
    for i in range(highest_stack, 0, -1) :
        for stack in stacks :
            if len(stack) >= i :
                print(f"[{stack[i-1]}]", end=' ')
            else :
                print('   ', end=' ')
        print()
    for i in range(len(stacks)) :
        print(f" {i+1} ", end=' ')
    print()

if __name__ == "__main__":
    stacks, procedures = parse_input()

    print("Initial state:")
    print_stacks(stacks)

    for count, src, dest in procedures :
        move = stacks[src-1][-count:]
        stacks[src-1] = stacks[src-1][:-count]
        print(f"Moving {move} from {src} to {dest}")
        move = move[::-1]
        stacks[dest-1] += move
        print_stacks(stacks)
    
    final_message = ''.join([stack[-1] for stack in stacks])
    print(f"Final message: {final_message}")
