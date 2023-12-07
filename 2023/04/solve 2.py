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
    wins = [
        list(m.group('n') for m in re.finditer(r" (?P<n>[\d]+)(?= .*?\|.*? (?P=n)(?: |$))", line))
        for line in data
    ]
    return wins

def solve ( filename ) :
    wins = parse_file(filename)
    wins = [len(win) for win in wins]
    cards = [1 for _ in range(len(wins))]
    for i in range(len(cards)) :
        for j in range(i+1, min(i+wins[i]+1, len(cards))) :
            cards[j] += cards[i]
    return sum(cards)

if __name__ == "__main__" :
    print(f"Test result: {solve('test 1')}")
    print(f"Input result: {solve('input')}")
