from pathlib import Path
input_file = Path(__file__).parent / "input"

def parse_input ( debug = False ) :
    with open(input_file, "r") as f :
        data = f.read().strip()
    return data
    
def find_start_of_packet ( stream, group_size, debug = False ) :
    moving_window = ' ' * group_size
    indices = [0] * group_size
    for i, c in enumerate(stream) :
        if debug : print(f"({i}, {c}) | \"{moving_window}\"")
        index = moving_window.rfind(c)

        if debug : print(f"  m{index}")
        if index == -1 :
            if debug : print(f"  indices: {indices}")
            for j in range(group_size) :
                if indices[j] != -1 and indices[j] < j :
                    if debug : print(f"  Failed on {j}; {indices[j]}")
                    break
            else :
                if debug : print(f"  Found \"{moving_window[1:] + c}\"")
                return i + 1
        
        indices = indices[1:] + [group_size - index if index >= 0 else -1]
        moving_window = moving_window[1:] + c
        if debug : print(f"  indices: {indices}")
    return -1

def tests ( ) :
    failures = 0
    if find_start_of_packet('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 4) != 7 :
        print(f"Test 1 failed; expected 7, got {find_start_of_packet('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 4, True)}")
        failures += 1
    if find_start_of_packet('bvwbjplbgvbhsrlpgdmjqwftvncz', 4) != 5 :
        print(f"Test 2 failed; expected 5, got {find_start_of_packet('bvwbjplbgvbhsrlpgdmjqwftvncz', 4, True)}")
        failures += 1
    if find_start_of_packet('nppdvjthqldpwncqszvftbrmjlhg', 4) != 6 :
        print(f"Test 3 failed; expected 6, got {find_start_of_packet('nppdvjthqldpwncqszvftbrmjlhg', 4, True)}")
        failures += 1
    if find_start_of_packet('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 4) != 10 :
        print(f"Test 4 failed; expected 10, got {find_start_of_packet('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 4, True)}")
        failures += 1
    if find_start_of_packet('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 4) != 11 :
        print(f"Test 5 failed; expected 11, got {find_start_of_packet('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 4, True)}")
        failures += 1
    
    if find_start_of_packet('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 14) != 19 :
        print(f"Test 6 failed; expected 19, got {find_start_of_packet('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 14, True)}")
        failures += 1
    if find_start_of_packet('bvwbjplbgvbhsrlpgdmjqwftvncz', 14) != 23 :
        print(f"Test 7 failed; expected 15, got {find_start_of_packet('bvwbjplbgvbhsrlpgdmjqwftvncz', 14, True)}")
        failures += 1
    if find_start_of_packet('nppdvjthqldpwncqszvftbrmjlhg', 14) != 23 :
        print(f"Test 8 failed; expected 16, got {find_start_of_packet('nppdvjthqldpwncqszvftbrmjlhg', 14, True)}")
        failures += 1
    if find_start_of_packet('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 14) != 29 :
        print(f"Test 9 failed; expected 20, got {find_start_of_packet('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 14, True)}")
        failures += 1
    if find_start_of_packet('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 14) != 26 :
        print(f"Test 10 failed; expected 21, got {find_start_of_packet('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 14, True)}")
        failures += 1
    
    if failures == 0 :
        print("All tests passed!")
    else :
        print(f"{failures} tests failed.")

if __name__ == "__main__":
    tests()

    data = parse_input()
    print(f"Part 1: {find_start_of_packet(data, 4)}")
    print(f"Part 2: {find_start_of_packet(data, 14)}")
