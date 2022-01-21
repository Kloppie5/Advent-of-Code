from pathlib import Path
input_file = Path(__file__).parent / "input"

def parse_input ( input_file, debug = False ) :
  with open(input_file, "r") as f:
    data = f.read().splitlines()
  return data

if __name__ == "__main__":
  data = parse_input(input_file)
  diff = [ int(y) - int(x) for x, y in zip(data[:-1], data[1:]) ]
  increasing = [ x for x in diff if x > 0 ]
  print(f"Part 1: {len(increasing)}")
