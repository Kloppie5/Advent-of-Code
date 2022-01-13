from itertools import permutations

from pathlib import Path
input_file = Path(__file__).parent / "input"

def parse_input ( input_file, debug = False ) :
  data = []
  with open(input_file, "r") as f:
    for line in f.read().splitlines() :
      line = line[:-1]
      line = line.split()
      reindeer = line[0]
      speed = int(line[3])
      duration = int(line[6])
      rest = int(line[-2])
      data.append((reindeer, speed, duration, rest))
      if debug :
        print(f"{reindeer} : {speed} {duration} {rest}")
  return data

def race ( data, time, debug = False ) :
  results = {}
  for (reindeer, speed, duration, rest) in data :
    distance = 0
    full_cycles, remainder = divmod(time, duration + rest)
    if debug :
      print(f"{reindeer} gets {full_cycles} full cycles")
    distance += full_cycles * duration * speed
    if remainder > duration :
      remainder = duration
    distance += remainder * speed
    if debug :
      print(f"{reindeer} gets {remainder} seconds of remaining fly time")
    results[reindeer] = distance
  return results

if __name__ == "__main__":
  data = parse_input(input_file)
  results = race(data, 2503)
  winner = max(results, key=results.get)
  print(f"The winner is {winner} with a total distance of {results[winner]}")
