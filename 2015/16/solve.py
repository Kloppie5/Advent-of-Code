from pathlib import Path
input_file = Path(__file__).parent / "input"

def parse_input ( input_file, debug = False ) :
  data = {}
  with open(input_file, "r") as f:
    for line in f.read().splitlines() :
      line = line.split(' ')
      sue = line[1][:-1]
      prop1 = line[2][:-1]
      prop1value = int(line[3][:-1])
      prop2 = line[4][:-1]
      prop2value = int(line[5][:-1])
      prop3 = line[6][:-1]
      prop3value = int(line[7])

      data[sue] = {prop1: prop1value, prop2: prop2value, prop3: prop3value}
      if debug :
        print(f"{sue} ({prop1}: {prop1value}, {prop2}: {prop2value}, {prop3}: {prop3value})")
  return data

def find_sues ( data, ticker_tape, debug = False ) :
  sues = []
  for sue in data :
    sue_data = data[sue]
    correct = True
    for prop in ticker_tape :
      if prop in sue_data and sue_data[prop] != ticker_tape[prop] :
        if debug :
          print(f"{sue} does not have {prop} {ticker_tape[prop]}, but {sue_data[prop]}")
        correct = False
        break
    if correct :
      sues.append(sue)
  return sues

def find_real_sues ( data, ticker_tape, debug = False ) :
  sues = []
  for sue in data :
    sue_data = data[sue]
    correct = True
    for prop in ticker_tape :
      if prop in sue_data :
        if prop in ["cats", "trees"] :
          if sue_data[prop] <= ticker_tape[prop] :
            if debug :
              print(f"{sue} has too few {prop} ({sue_data[prop]} vs {ticker_tape[prop]})")
            correct = False
            break
          continue

        if prop in ["pomeranians", "goldfish"] :
          if sue_data[prop] >= ticker_tape[prop] :
            if debug :
              print(f"{sue} has too many {prop} ({sue_data[prop]} vs {ticker_tape[prop]})")
            correct = False
            break
          continue

        if sue_data[prop] != ticker_tape[prop] :
          if debug :
            print(f"{sue} has an invalid amount of {prop} ({sue_data[prop]} vs {ticker_tape[prop]})")
          correct = False
          break

    if correct :
      sues.append(sue)
  return sues

if __name__ == "__main__":
  data = parse_input(input_file)
  ticker_tape = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1
  }
  sue = find_sues(data, ticker_tape)
  print(f"Part 1: Sues {sue}")
  sue = find_real_sues(data, ticker_tape)
  print(f"Part 2: Sues {sue}")
