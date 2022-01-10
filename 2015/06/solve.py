from PIL import Image

from pathlib import Path
input_file = Path(__file__).parent / "input"

def on_off_lights ( instructions, debug = False ) :
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

def true_lights ( instructions, debug = False ) :
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
          grid[x][y] += 1
        elif action == "turn off" :
          grid[x][y] = max(0, grid[x][y] - 1)
        elif action == "toggle" :
          grid[x][y] += 2
  return grid

def grid_brightness ( grid ) :
  return sum(sum(row) for row in grid)

def render_grid ( grid, debug = False ) :
  im = Image.new("RGB", (1000, 1000))
  max_value = max(max(row) for row in grid)
  if debug :
    print(f"max_value: {max_value}")
  for x in range(1000) :
    for y in range(1000) :
      if debug :
        print(f"({x},{y}): {grid[x][y] * 255 // max_value}")
      im.putpixel((x, y), (grid[x][y] * 255 // max_value, grid[x][y] * 255 // max_value, grid[x][y] * 255 // max_value))
  im.save(Path(__file__).parent / "grid.png")

if __name__ == "__main__":
  with open(input_file, "r") as f:
    instructions = f.readlines()

  on_off_grid = on_off_lights(instructions)
  true_grid = true_lights(instructions)
  render_grid(true_grid)
  print(f"Part 1: {grid_brightness(on_off_grid)} lights are on.")
  print(f"Part 2: The brightness is {grid_brightness(true_grid)}.")
