import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

def read_file(filename) :
    from pathlib import Path
    with open(Path(__file__).parent / filename, "r") as f :
        return f.read()

def test(filename, expected) :
    result = solve(filename)
    if (result != expected) :
        print(f"Test '{filename}' failed; Expected '{expected}' but got '{result}'")
        exit(1)

# ========================================

def parse_file(filename) :
    data = read_file(filename)
    data = data.splitlines()
    left = []
    right = []

    pattern = re.compile(r'^(?P<left>\d+)\s+(?P<right>\d+)$')
    for line in data :
        m = pattern.match(line)
        try :
            left.append(int(m.group('left')))
            right.append(int(m.group('right')))
        except :
            print(f"Failed to match pattern '{pattern}' to input '{line}'")

    return left, right


def solve(filename) :
    left, right = parse_file(filename)
    left.sort()
    right.sort()
    
    result_1 = 0
    for l, r in zip(left, right) :
        result_1 += abs(l - r)

    result_2 = 0
    leftcounts = dict((x, left.count(x)) for x in set(left))
    rightcounts = dict((x, right.count(x)) for x in set(right))
    for key in leftcounts :
        result_2 += key * leftcounts[key] * rightcounts.get(key, 0)   

    return result_1, result_2


def main():
    test('test', (11, 31))

    print(f"Input result: {solve('input')}")

# ========================================

if __name__ == "__main__" :
    main()
