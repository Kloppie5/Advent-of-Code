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
    cards = [
        list(m.group('n') for m in re.finditer(r" (?P<n>[\d]+)(?= .*?\|.*? (?P=n)(?: |$))", line))
        for line in data
    ]
    return cards

def solve ( filename ) :
    cards = parse_file(filename)
    return sum([int(2**(len(card)-1)) for card in cards])

if __name__ == "__main__" :
    print(f"Test result: {solve('test 1')}")
    print(f"Input result: {solve('input')}")
