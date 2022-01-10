from pathlib import Path
input_file = Path(__file__).parent / "input"

def is_nice ( word, debug = False ) :
  vowels = 0
  for c in word:
    if c in "aeiou":
      vowels += 1
  if vowels < 3:
    if debug:
      print(f"{word} NOT NICE, {vowels} vowels")
    return False

  doubles = 0
  for i in range(0, len(word) - 1):
    if word[i] == word[i + 1]:
      doubles += 1
  if doubles == 0:
    if debug:
      print(f"{word} NOT NICE, no doubles")
    return False

  for substring in ["ab", "cd", "pq", "xy"]:
    if substring in word:
      if debug:
        print(f"{word} NOT NICE, detected {substring}")
      return False

  if debug:
    print(f"{word} NICE")
  return True

def is_nicer ( word, debug = False ):
  pairs = {}
  pair_index = -1
  for i in range(0, len(word) - 1):
    pair = word[i:i+2]
    if pair not in pairs:
      pairs[pair] = i
    else:
      if i - pairs[pair] != 1:
        pair_index = i
        break
  if pair_index == -1:
    if debug:
      print(f"{word} NOT NICE, no pairs; {pairs}")
    return False

  for i in range(0, len(word) - 2):
    if word[i] == word[i + 2]:
      if debug:
        print(f"{word} NICE, pair at {pair_index}")
      return True
  if debug:
    print(f"{word} NOT NICE, no letters that repeat with one letter between them")
  return False


if __name__ == "__main__":
  nice = 0
  nicer = 0
  with input_file.open() as f:
    data = f.read().strip()
    for line in data.split("\n"):
      if is_nice(line):
        nice += 1
      if is_nicer(line):
        nicer += 1

  print(f"Part 1: {nice} nice words")
  print(f"Part 2: {nicer} nicer words")
