
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

print(f"Code: {code}")
