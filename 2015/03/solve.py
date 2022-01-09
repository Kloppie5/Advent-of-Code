from pathlib import Path
input_file = Path(__file__).parent / "input"

def visit_houses ( debug = False ) :
  houses = {(0, 0): 1}
  with input_file.open() as f:
    data = f.read().strip()
    x = 0
    y = 0
    for c in data:
      if c == "^":
        y += 1
      elif c == "v":
        y -= 1
      elif c == "<":
        x -= 1
      elif c == ">":
        x += 1
      else:
        raise Exception(f"Unknown direction: {c}")
      if debug:
        print(f"Visiting ({x}, {y})")
      if (x, y) not in houses:
        houses[(x, y)] = 1
      else:
        houses[(x, y)] += 1
  return houses

def visit_houses_parallel ( debug = False ) :
  houses = {(0, 0): 2}
  robo_step = 0
  with input_file.open() as f:
    data = f.read().strip()
    x = [0, 0]
    y = [0, 0]
    for c in data:
      if c == "^":
        y[robo_step] += 1
      elif c == "v":
        y[robo_step] -= 1
      elif c == "<":
        x[robo_step] -= 1
      elif c == ">":
        x[robo_step] += 1
      else:
        raise Exception(f"Unknown direction: {c}")
      if debug:
        print(f"Visiting[{robo_step}] ({x[robo_step]}, {y[robo_step]})")
      if (x[robo_step], y[robo_step]) not in houses:
        houses[(x[robo_step], y[robo_step])] = 1
      else:
        houses[(x[robo_step], y[robo_step])] += 1
      robo_step = 1 - robo_step # (robo_step + 1) % n
  return houses

if __name__ == "__main__":
  r = visit_houses()
  print(f"Part 1: {len(r)} houses receive at least one present.")
  r = visit_houses_parallel()
  print(f"Part 2: {len(r)} houses receive at least one present.")
