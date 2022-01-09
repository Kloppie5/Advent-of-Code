from pathlib import Path
input_file = Path(__file__).parent / "input"

def small_step (debug = False):
  floor = 0
  with input_file.open() as f:
    data = f.read().strip()
    for c in data:
      if c == "(":
        floor += 1
      elif c == ")":
        floor -= 1
      if debug:
        print(c, floor)
  return floor

def big_step (debug = False):
  with input_file.open() as f:
    data = f.read().strip()
    floor = data.count("(") - data.count(")")
    if debug:
      print(data)
      print(floor)
  return floor

if __name__ == "__main__":
  big_step(True)
