import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

def read_file ( filename ) :
    from pathlib import Path
    with open(Path(__file__).parent / filename, "r") as f :
        return f.read()

def parse_file ( filename ) :
    data = read_file(filename)
    data = data.splitlines()
    numbers = {}
    symbols = {}
    for i, line in enumerate(data) :
        for m in re.finditer('(?P<number>[\d]+)', line) :
            numbers[(i, m.start())] = m.group('number')
        for m in re.finditer('(?P<symbol>[^\d.])', line) :
            symbols[(i, m.start())] = m.group('symbol')
    return numbers, symbols

def solve ( filename ) :
    numbers, symbols = parse_file(filename)
    olms = [(-3, -1, 3), (-2, -1, 2), (-1, -1, 1), (0, -1, 1), (1, -1, 1),
            (-3,  0, 3), (-2,  0, 2), (-1,  0, 1),             (1,  0, 1),
            (-3,  1, 3), (-2,  1, 2), (-1,  1, 1), (0,  1, 1), (1,  1, 1)]
    result = 0
    for (row, col), symbol in symbols.items() :
        for dx, dy, l in olms :
            if (row+dy, col+dx) in numbers and len(numbers[(row+dy, col+dx)]) >= l :
                result += int(numbers[(row+dy, col+dx)])
                del numbers[(row+dy, col+dx)]
    return result

if __name__ == "__main__" :
    print(f"Test result: {solve('test 1')}")
    print(f"Input result: {solve('input')}")
