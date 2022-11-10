
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
