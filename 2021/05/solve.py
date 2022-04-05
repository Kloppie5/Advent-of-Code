import copy

from pathlib import Path
input_file = Path(__file__).parent / "input"

def parse_input ( input_file, debug = False ) :
  vents = []
  with open(input_file, "r") as f:
    for line in f.read().splitlines() :
      start, end = line.split(' -> ')
      x1, y1 = start.split(',')
      x2, y2 = end.split(',')
      vents.append({"x1": int(x1), "y1": int(y1), "x2": int(x2), "y2": int(y2)})
  return vents

def axial_overlap_board ( vents, debug = False ) :
  x_max = max([max(v["x1"], v["x2"]) for v in vents])
  y_max = max([max(v["y1"], v["y2"]) for v in vents])
  board = [[0 for x in range(x_max+1)] for y in range(y_max+1)]

  for vent in vents :

    if vent["x1"] == vent["x2"] :
      direction = 1 if vent["y1"] < vent["y2"] else -1
      ys = range(vent["y1"], vent["y2"] + direction, direction)
      for y in ys :
        board[y][vent["x1"]] += 1
    
    elif vent["y1"] == vent["y2"] :
      direction = 1 if vent["x1"] < vent["x2"] else -1
      xs = range(vent["x1"], vent["x2"] + direction, direction)
      for x in xs :
        board[vent["y1"]][x] += 1

  return board

def overlap_board ( vents ) :
  x_max = max([max(v["x1"], v["x2"]) for v in vents])
  y_max = max([max(v["y1"], v["y2"]) for v in vents])
  board = [[0 for x in range(x_max+1)] for y in range(y_max+1)]

  for vent in vents :
    dx = 1 if vent["x1"] <= vent["x2"] else -1
    xs = range(vent["x1"], vent["x2"] + dx, dx)
    dy = 1 if vent["y1"] <= vent["y2"] else -1
    ys = range(vent["y1"], vent["y2"] + dy, dy)
 
    if len(xs) == 1 :
      xs = [xs[0]] * len(ys)
    if len(ys) == 1 :
      ys = [ys[0]] * len(xs)
    
    for x, y in zip(xs, ys) :
      board[y][x] += 1
  
  return board

def count_overlaps ( board ) :
  return sum([sum([1 for x in row if x > 1]) for row in board])

if __name__ == "__main__":
  vents = parse_input(input_file)
  board = axial_overlap_board(vents)
  print(f"Part 1: {count_overlaps(board)}")
  board = overlap_board(vents)
  print(f"Part 2: {count_overlaps(board)}")
