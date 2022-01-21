from pathlib import Path
input_file = Path(__file__).parent / "input"

def parse_input ( input_file, debug = False ) :
  with open(input_file, "r") as f:
    data = f.read().splitlines()
  return data

def diagnostics ( data ) :
  length = len(data)
  # transpose and cast to int
  data = [ map(int, x) for x in zip(*[ list(x) for x in data ]) ]
  # most common bit
  data = [ int(sum(x) > length / 2) for x in data ]

  gamma_rate = int(''.join(map(str, data)), 2)
  epsilon_rate = (1 << len(data)) - gamma_rate - 1

  return gamma_rate, epsilon_rate

if __name__ == "__main__":
  data = parse_input(input_file)
  gamma_rate, epsilon_rate = diagnostics(data)
  print(f"Part 1: {gamma_rate*epsilon_rate}")
