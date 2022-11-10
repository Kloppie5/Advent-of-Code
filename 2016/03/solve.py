
# read input
with open("input", "r") as f :
  input = f.read()
  # split into lines
  input = input.splitlines()
  # split into words
  input = [line.split() for line in input]
  # convert to integers
  input = [[int(x) for x in line] for line in input]

# count valid triangles
count = 0
for line in input :
  if line[0] + line[1] > line[2] and line[0] + line[2] > line[1] and line[1] + line[2] > line[0] :
    count += 1
  else :
    print(f"Invalid triangle: {line}")

print(f"Valid triangles: {count}")

# count valid triangles vertically
count = 0
for i in range(0, len(input), 3) :
  for j in range(3) :
    if input[i][j] + input[i + 1][j] > input[i + 2][j] and input[i][j] + input[i + 2][j] > input[i + 1][j] and input[i + 1][j] + input[i + 2][j] > input[i][j] :
      count += 1
    else :
      print(f"Invalid vertical triangle: {input[i][j]}, {input[i + 1][j]}, {input[i + 2][j]}")

print(f"Valid vertical triangles: {count}")
