
# read input
with open("input", "r") as f :
  input = f.read()
  # split into lines
  input = input.splitlines()

# starting position
x = 1
y = 1
code = ""

# loop through instructions
for line in input :
  # loop through characters
  for c in line :
    # move
    if c == "U" :
      y = max(0, y - 1)
    elif c == "D" :
      y = min(2, y + 1)
    elif c == "L" :
      x = max(0, x - 1)
    else :
      x = min(2, x + 1)
  
  # print number
  print(f"({x}, {y}) = {x + y * 3 + 1}")
  code += str(x + y * 3 + 1)

print(f"Simple code: {code}")

# reset position
x = 2
y = 2
keypad = [
  [" ", " ", "1", " ", " "],
  [" ", "2", "3", "4", " "],
  ["5", "6", "7", "8", "9"],
  [" ", "A", "B", "C", " "],
  [" ", " ", "D", " ", " "]
]
complicated_code = ""

# loop through instructions
for line in input :
  # loop through characters
  for c in line :
    # move
    if c == "U" and y > 0 and keypad[y - 1][x] != " " :
      y -= 1
    elif c == "D" and y < 4 and keypad[y + 1][x] != " " :
      y += 1
    elif c == "L" and x > 0 and keypad[y][x - 1] != " " :
      x -= 1
    elif c == "R" and x < 4 and keypad[y][x + 1] != " " :
      x += 1
  
  # print button
  print(f"({x}, {y}) = {keypad[y][x]}")
  complicated_code += keypad[y][x]

print(f"Complicated code: {complicated_code}")
