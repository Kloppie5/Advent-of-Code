from itertools import permutations

from pathlib import Path
input_file = Path(__file__).parent / "input"

def parse_input ( input_file, debug = False ) :
  data = {}
  with open(input_file, "r") as f:
    for line in f.read().splitlines() :
      line = line[:-1]
      line = line.split()
      source = line[0]
      if line[2] == "gain" :
        gain = int(line[3])
      else :
        gain = -int(line[3])
      target = line[-1]
      if debug :
        print(f"{source} -> {target} : {gain}")
      data[source] = data.get(source, {})
      data[target] = data.get(target, {})
      data[source][target] = data[source].get(target, 0) + gain
      data[target][source] = data[target].get(source, 0) + gain
  return data

def find_optimal_arrangement ( data, debug = False ) :
  arrangements = {}
  for arrangement in permutations(data.keys()) :
    score = 0
    for i in range(len(arrangement)) :
      source = arrangement[i]
      target = arrangement[(i + 1) % len(arrangement)]
      score += data[source][target]
    arrangements[arrangement] = score
    if debug :
      print(arrangement, score)
  best_arrangement = max(arrangements, key=arrangements.get)
  return best_arrangement, arrangements[best_arrangement]

if __name__ == "__main__":
  debug = False
  data = parse_input(input_file)
  if debug :
    print(data)

  print(f"Part 1: {find_optimal_arrangement(data, debug)[1]}")
