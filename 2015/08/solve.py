from pathlib import Path
input_file = Path(__file__).parent / "input"

def small_step_number_of_characters_in_string ( string ):
  string = string[1:-1] # remove surrounding quotes
  characters_in_string = 0

  i = 0
  while i < len(string): # python, why dont you have a proper for loop?
    characters_in_string += 1
    if string[i] != '\\':
      i += 1
      continue

    # indexing i+1 is technically unsafe for improper input
    if string[i+1] == 'x':
      i += 4
    elif string[i+1] == '\\':
      i += 2
    elif string[i+1] == '"':
      i += 2
    else:
      print("Error: unknown escape sequence: " + string[i:])
      exit(1)

  return characters_in_string

def number_of_characters_in_encoded_string ( string ) :
  return \
    len(string) \
    + string.count('\\') \
    + string.count('\"') \
    + 2

if __name__ == "__main__":
  debug = False

  total_characters_in_string = 0
  total_characters_in_memory = 0
  total_characters_in_encoded_string = 0
  with open(input_file, "r") as f:
    for line in f:
      line = line.strip()
      characters_in_string = len(line)
      characters_in_memory = small_step_number_of_characters_in_string(line)
      characters_in_encoded_string = number_of_characters_in_encoded_string(line)
      total_characters_in_string += characters_in_string
      total_characters_in_memory += characters_in_memory
      total_characters_in_encoded_string += characters_in_encoded_string
      if debug :
        print(f"{line} - {characters_in_string} characters in string, {characters_in_memory} characters in memory, {characters_in_encoded_string} characters in encoded string")
  if debug :
    print(f"Total characters in string: {total_characters_in_string}")
    print(f"Total characters in memory: {total_characters_in_memory}")
  print(f"Part 1: Difference: {total_characters_in_string - total_characters_in_memory}")
  if debug :
    print(f"Total characters in encoded string: {total_characters_in_encoded_string}")
  print(f"Part 2: Difference: {total_characters_in_encoded_string - total_characters_in_string}")
