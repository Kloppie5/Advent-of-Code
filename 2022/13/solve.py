import sys
sys.stdout.reconfigure(encoding='utf-8')

def parse_input ( filename, mode ) :
    from pathlib import Path
    with open(Path(__file__).parent / filename, "r") as f :
        data = f.read()

    if mode == "pairs" :
        data = data.split("\n\n")
        data = [line.splitlines() for line in data]
        data = [(eval(left), eval(right)) for left, right in data]
    elif mode == "singles" :
        data = data.splitlines()
        data = [line for line in data if line]
        data = [eval(line) for line in data]
    else :
        raise Exception("Unknown mode")
    
    return data

def compare_pair ( left, right ) :
    """
      -2: Critical error
      -1: False
       0: Continue
       1: True
    """

    if isinstance(left, int) and isinstance(right, int):
        if left < right : return 1
        if left > right : return -1
        return 0
    if isinstance(left, list) and isinstance(right, list):
        for i in range(len(left)) :
            if i >= len(right) : return -1
            result = compare_pair(left[i], right[i])
            if result != 0 : return result
        if len(left) < len(right) : return 1
        return 0
    if isinstance(left, int) and isinstance(right, list):
        return compare_pair([left], right)
    if isinstance(left, list) and isinstance(right, int):
        return compare_pair(left, [right])
    return -2

if __name__ == "__main__" :
    pairs = parse_input("input", "pairs")
    
    right_order = []
    for i, pair in enumerate(pairs):
        result = compare_pair(pair[0], pair[1])
        print(f"Result {i+1}: {result}")
        if result == 1:
            right_order.append(i+1)
    print(f"Right order: {right_order}")
    print(f"Part 1: {sum(right_order)}")

    packets = parse_input("input", "singles")
    pre_2 = 0
    pre_6 = 0
    for i, packet in enumerate(packets):
        result = compare_pair(packet, [[2]])
        if result == 1:
            pre_2 += 1
        result = compare_pair(packet, [[6]])
        if result == 1:
            pre_6 += 1

    index_2 = pre_2 + 1
    index_6 = pre_6 + 2
    print(f"Index 2: {index_2}")
    print(f"Index 6: {index_6}")
    print(f"Part 2: {index_2 * index_6}")
