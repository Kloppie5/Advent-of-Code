from pathlib import Path
input_file = Path(__file__).parent / "input"

def parse_input ( input_file, debug = False ) :
  with open(input_file, "r") as f:
    data = f.read().splitlines()
    data = [ int(x) for x in data ]
  return data

def sliding_window_sum ( data, size ) :
  return [ sum(data[i:i+size]) for i in range(len(data)-size+1) ]

def increasing ( data ) :
  diff = [ y - x for x, y in zip(data[:-1], data[1:]) ]
  increasing = [ x for x in diff if x > 0 ]
  return len(increasing)

if __name__ == "__main__":
  data = parse_input(input_file)
  print(f"Part 1: {increasing(data)}")
  print(f"Part 2: {increasing(sliding_window_sum(data, 3))}")
