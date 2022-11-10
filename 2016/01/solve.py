
# read input
with open("input", "r") as f :
  input = f.read()
  # remove trailing newline
  input = input[:-1]
  
# split input into list of instructions
instructions = input.split(", ")
print(instructions)

# starting position
x = 0
y = 0
direction = 0
visited = set()

# loop through instructions
for instruction in instructions :
  # get direction
  if instruction[0] == "L" :
    direction = (direction - 1) % 4
  else :
    direction = (direction + 1) % 4
    
  # get distance
  distance = int(instruction[1:])
  
  # loop through distance
  for i in range(distance) :
    # move
    if direction == 0 :
      y += 1
    elif direction == 1 :
      x += 1
    elif direction == 2 :
      y -= 1
    else :
      x -= 1
      
    # check if visited
    if (x, y) in visited :
      print(f"Visited twice at ({x}, {y}), distance = {abs(x) + abs(y)}")
    visited.add((x, y))

# calculate distance
distance = abs(x) + abs(y)
print(f"Final distance: {distance}")
