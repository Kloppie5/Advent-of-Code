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
    return data

def solve ( filename ) :
    data = parse_file(filename)
    result = 0
    translate = {
        '1' : 1, 'one'  : 1,
        '2' : 2, 'two'  : 2,
        '3' : 3, 'three': 3,
        '4' : 4, 'four' : 4,
        '5' : 5, 'five' : 5,
        '6' : 6, 'six'  : 6,
        '7' : 7, 'seven': 7,
        '8' : 8, 'eight': 8,
        '9' : 9, 'nine' : 9
    }
    for line in data :
        first = re.match('^' '[^\d]*?' '(?P<first>\d|one|two|three|four|five|six|seven|eight|nine)'      '.*' '$', line).group('first')
        last  = re.match('^'      '.*' '(?P<last>\d|one|two|three|four|five|six|seven|eight|nine)'  '[^\d]*?' '$', line).group('last')
        first = translate[first]
        last = translate[last]
        result += int(first) * 10 + int(last)
    return result

if __name__ == "__main__" :
    print(f"Test result: {solve('test 2')}")
    print(f"Input result: {solve('input')}")
