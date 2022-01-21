from pathlib import Path
input_file = Path(__file__).parent / "input"

def parse_input ( input_file, debug = False ) :
  data = []
  with open(input_file, "r") as f:
    for line in f.read().splitlines() :
      line = line.split(' ')
      direction = line[0]
      distance = int(line[1])
      data.append((direction, distance))
  return data

def final_destination ( data ) :
  forwards = [ x[1] for x in data if x[0] == 'forward' ]
  downwards = [ x[1] for x in data if x[0] == 'down' ]
  upwards = [ x[1] for x in data if x[0] == 'up' ]
  return ( sum(forwards), sum(downwards) - sum(upwards) )

def aimed_navigation ( data, debug = False ) :
  pos = 0
  depth = 0
  aim = 0
  for direction, distance in data :
    if direction == 'forward' :
      pos += distance
      depth += aim * distance
    elif direction == 'down' :
      aim += distance
    elif direction == 'up' :
      aim -= distance
    else :
      print(f"Unknown direction: {direction}")
      exit(1)
    if debug :
      print(f"pos: {pos}, depth: {depth}, aim: {aim}")
  return pos, depth

if __name__ == "__main__":
  data = parse_input(input_file)
  final_dist, final_depth = final_destination(data)
  print(f"Part 1: {final_dist*final_depth}")
  final_dist, final_depth = aimed_navigation(data)
  print(f"Part 2: {final_dist*final_depth}")
