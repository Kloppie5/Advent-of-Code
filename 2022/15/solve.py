import sys
sys.stdout.reconfigure(encoding='utf-8')

def parse_input ( filename ) :
    from pathlib import Path
    with open(Path(__file__).parent / filename, "r") as f :
        data = f.read().splitlines()
    for i in range(len(data)) :
        line = data[i].split(": ")

        sx, sy, = line[0].split(", ")
        sx = int(sx.split("x=")[1])
        sy = int(sy.split("y=")[1])
        
        bx, by, = line[1].split(", ")
        bx = int(bx.split("x=")[1])
        by = int(by.split("y=")[1])

        data[i] = {
            "sensor" : (sx, sy),
            "beacon" : (bx, by)
        }
    return data

def translate_to_line ( data, target_y ) :
    intervals = []
    for entry in data :
        distance = abs(entry["beacon"][0] - entry["sensor"][0]) + abs(entry["beacon"][1] - entry["sensor"][1])
        effect = distance - abs(entry["sensor"][1] - target_y)
        print(f"Sensor {entry} at distance {distance} has effect {effect}")
        if effect > 0 :
            intervals += [(entry["sensor"][0] - effect, entry["sensor"][0] + effect)]
            print(f"Interval: {intervals[-1]}")
    return intervals

def combine_intervals ( intervals ) :
    intervals.sort()
    i = 0
    while i < len(intervals) - 1 :
        if intervals[i][1] >= intervals[i + 1][0] :
            print(f"Combining {intervals[i]} and {intervals[i + 1]}")
            intervals[i] = (intervals[i][0], max(intervals[i][1], intervals[i + 1][1]))
            print(f"Result: {intervals[i]}")
            intervals.pop(i + 1)
        else :
            i += 1
    return intervals

if __name__ == "__main__" :
    data = parse_input("input")
    target_y = 2000000

    beacons_on_the_line = set([entry["beacon"][0] for entry in data if entry["beacon"][1] == target_y])
    print(beacons_on_the_line)
    data = translate_to_line(data, target_y)
    data = combine_intervals(data)
    print(data)
    positions = sum([interval[1] - interval[0] + 1 for interval in data])
    print(f"Part 1: {positions} {beacons_on_the_line} => {positions - len(beacons_on_the_line)}")

    data = parse_input("input")
    sum_lines = []
    diff_lines = []
    for i in range(len(data)) :
        distance = abs(data[i]["beacon"][0] - data[i]["sensor"][0]) + abs(data[i]["beacon"][1] - data[i]["sensor"][1])
        sum_lines += [data[i]["sensor"][0] + data[i]["sensor"][1] - distance - 1]
        sum_lines += [data[i]["sensor"][0] + data[i]["sensor"][1] + distance + 1]
        diff_lines += [data[i]["sensor"][0] - data[i]["sensor"][1] - distance - 1]
        diff_lines += [data[i]["sensor"][0] - data[i]["sensor"][1] + distance + 1]
    sum_lines.sort()
    diff_lines.sort()

    sum_lines = [sum_lines[i] for i in range(len(sum_lines)-1) if sum_lines[i] == sum_lines[i+1]]
    diff_lines = [diff_lines[i] for i in range(len(diff_lines)-1) if diff_lines[i] == diff_lines[i+1]]

    possibilities = []
    for sum_line in sum_lines :
        for diff_line in diff_lines :
            if (sum_line + diff_line) % 2 == 0 :
                x = (sum_line + diff_line) // 2
                y = (sum_line - diff_line) // 2
                possibilities += [(x, y)]
    print(f"Possibilities: {possibilities}")

    solution_x = 0
    solution_y = 0
    for x, y in possibilities :
        print(f"Checking ({x}, {y})")
        for entry in data :
            distance = abs(entry["beacon"][0] - entry["sensor"][0]) + abs(entry["beacon"][1] - entry["sensor"][1])
            if abs(entry["sensor"][0] - x) + abs(entry["sensor"][1] - y) < distance :
                print(f" X ({x}, {y}) falls within range of {entry}")
                break
        else :
            print(f" ! ({x}, {y}) is a valid position")
            solution_x = x
            solution_y = y
    
    print(f"Part 2: {solution_x} {solution_y} => {solution_x * 4000000 + solution_y}")
    

        
