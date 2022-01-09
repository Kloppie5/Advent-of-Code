from pathlib import Path
input_file = Path(__file__).parent / "input"

def small_step_final_floor (debug = False):
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

def big_step_final_floor (debug = False):
  with input_file.open() as f:
    data = f.read().strip()
    floor = data.count("(") - data.count(")")
    if debug:
      print(data)
      print(floor)
  return floor

def small_step_first_time_basement (debug = False):
  floor = 0
  with input_file.open() as f:
    data = f.read().strip()
    for i in range(len(data)):
      if data[i] == "(":
        floor += 1
      elif data[i] == ")":
        floor -= 1
      if debug:
        print(i, floor)
      if floor == -1:
        return i + 1
  return -1

if __name__ == "__main__":
  r = big_step_final_floor()
  print(f"Part 1: The final floor is {r}")
  r = small_step_first_time_basement()
  print(f"Part 2: The first time Santa enters the basement is at {r}")
