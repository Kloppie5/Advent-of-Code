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

if __name__ == "__main__":
  nice = 0
  with input_file.open() as f:
    data = f.read().strip()
    for line in data.split("\n"):
      if is_nice(line):
        nice += 1

  print(f"Part 1: {nice} nice words")
