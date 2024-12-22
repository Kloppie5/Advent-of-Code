import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

def read_file(filename) :
    from pathlib import Path
    with open(Path(__file__).parent / filename, "r") as f :
        return f.read()

def test(data, offset, expected) :
    result = solve(data, offset)
    if (result != expected) :
        print(f"Test '{data}' with offset '{offset}' failed; Expected '{expected}' but got '{result}'")
        exit(1)

# ========================================

def parse_file(filename) :
    data = read_file(filename)
    return data

def solve_file(filename, offset) :
    return solve(parse_file(filename), offset)

def solve(data, offset) :
    return sum([
        int(l) for (l, r) 
        in zip(data, data[offset:]+data[:offset])
        if l == r
    ])

def main() :
    test('1122', 1, 3)
    test('1111', 1, 4)
    test('12345', 1, 0)
    test('91212129', 1, 9)

    result = solve_file('input', 1)
    print(f"Result 1: {result}")
    
    test('1212', 2, 6)
    test('1221', 2, 0)
    test('123425', 3, 4)
    test('123123', 3, 12)
    test('12131415', 4, 4)
    
    data = parse_file('input')
    result = solve(data, len(data)//2)
    print(f"Result 2: {result}")

# ========================================

if __name__ == "__main__" :
    main()
