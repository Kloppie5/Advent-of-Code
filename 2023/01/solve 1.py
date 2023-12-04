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
    for line in data :
        first = re.match('^[^\d]*(?P<first>\d).*$', line).group('first')
        last  = re.match('^.*(?P<last>\d)[^\d]*$', line).group('last')
        result += int(first) * 10 + int(last)
    return result

if __name__ == "__main__" :
    print(f"Test result: {solve('test 1')}")
    print(f"Input result: {solve('input')}")
