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

    stacks_9000 = stacks
    stacks_9001 = stacks.copy()

    for count, src, dest in procedures :
        print('-'*20)
        move_9000 = stacks_9000[src-1][-count:]
        stacks_9000[src-1] = stacks_9000[src-1][:-count]
        print(f"9000: Moving {move_9000} from {src} to {dest}")
        move_9000 = move_9000[::-1]
        stacks_9000[dest-1] += move_9000
        print_stacks(stacks_9000)

        move_9001 = stacks_9001[src-1][-count:]
        stacks_9001[src-1] = stacks_9001[src-1][:-count]
        print(f"9001: Moving {move_9001} from {src} to {dest}")
        stacks_9001[dest-1] += move_9001
        print_stacks(stacks_9001)
    
    final_message_9000 = ''.join([stack[-1] for stack in stacks_9000])
    print(f"Final message CrateMover 9000: {final_message_9000}")
    final_message_9001 = ''.join([stack[-1] for stack in stacks_9001])
    print(f"Final message CrateMover 9001: {final_message_9001}")
