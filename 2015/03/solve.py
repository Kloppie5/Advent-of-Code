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

if __name__ == "__main__":
  r = visit_houses()
  print(f"Part 1: {len(r)} houses receive at least one present.")
