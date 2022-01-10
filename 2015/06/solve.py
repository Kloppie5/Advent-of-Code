from pathlib import Path
input_file = Path(__file__).parent / "input"

def lights ( instructions, debug = False ) :
  grid = []
  for i in range(1000) :
    grid.append([0]*1000)
  for instruction in instructions :
    action = " ".join(instruction.split()[:-3])
    start_x = int(instruction.split()[-3].split(",")[0])
    start_y = int(instruction.split()[-3].split(",")[1])
    end_x = int(instruction.split()[-1].split(",")[0])
    end_y = int(instruction.split()[-1].split(",")[1])
    if debug :
      print(f"{action} | {start_x} {start_y} | {end_x} {end_y}")
    for x in range(start_x, end_x+1) :
      for y in range(start_y, end_y+1) :
        if action == "turn on" :
          grid[x][y] = 1
        elif action == "turn off" :
          grid[x][y] = 0
        elif action == "toggle" :
          grid[x][y] = 1 - grid[x][y]

  return grid

def print_grid ( grid ) :
  for row in grid :
    print("".join(["#" if x else "." for x in row]))

if __name__ == "__main__":
  with open(input_file, "r") as f:
    grid = lights(f.readlines())
    print_grid(grid)
    print(f"Part 1: {sum(sum(row) for row in grid)} lights are on.")
