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
    result = []
    for line in data :
        id    = int(re.match('^Game (?P<id>[\d]+):', line).group('id'))
        red   = [int(m.group('red'))   for m in re.finditer('(?P<red>[\d]+) red', line)]
        green = [int(m.group('green')) for m in re.finditer('(?P<green>[\d]+) green', line)]
        blue  = [int(m.group('blue'))  for m in re.finditer('(?P<blue>[\d]+) blue', line)]
        result.append((id, red, green, blue))
    return result

def solve ( filename ) :
    games = parse_file(filename)
    result = 0
    for (id, red, green, blue) in games :
        if max(red) <= 12 and max(green) <= 13 and max(blue) <= 14 :
            result += id
    return result

if __name__ == "__main__" :
    print(f"Test result: {solve('test 1')}")
    print(f"Input result: {solve('input')}")
