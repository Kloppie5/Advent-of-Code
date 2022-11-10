
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

# loop through instructions
for instruction in instructions :
  # get direction
  if instruction[0] == "L" :
    direction = (direction - 1) % 4
  else :
    direction = (direction + 1) % 4
    
  # get distance
  distance = int(instruction[1:])
  
  # move
  if direction == 0 :
    y += distance
  elif direction == 1 :
    x += distance
  elif direction == 2 :
    y -= distance
  elif direction == 3 :
    x -= distance

# calculate distance
distance = abs(x) + abs(y)
print(f"Distance: {distance}")
