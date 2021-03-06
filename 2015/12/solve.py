import json

from pathlib import Path
input_file = Path(__file__).parent / "input"

def recursive_count ( obj, debug = False ) :
  if isinstance(obj, dict) :
    count = 0
    for k, v in obj.items() :
      if k.isdigit() :
        if debug :
          print(f"Found dict key {k}")
        count += int(k)
      count += recursive_count(v, debug)
    return count

  if isinstance(obj, list) :
    count = 0
    for v in obj :
      count += recursive_count(v, debug)
    return count

  if isinstance(obj, int) :
    if debug :
      print(f"Found value {obj}")
    return obj

  return 0

def recursive_count_ignore_red ( obj, debug = False ) :
  if isinstance(obj, dict) :
    if "red" in obj.values() :
      if debug :
        print(f"Found red in {obj}")
      return 0
    count = 0
    for k, v in obj.items() :
      if k.isdigit() :
        if debug :
          print(f"Found dict key {k}")
        count += int(k)
      count += recursive_count_ignore_red(v, debug)
    return count

  if isinstance(obj, list) :
    count = 0
    for v in obj :
      count += recursive_count_ignore_red(v, debug)
    return count

  if isinstance(obj, int) :
    if debug :
      print(f"Found value {obj}")
    return obj

  return 0

if __name__ == "__main__":
  with open(input_file, "r") as f:
    data = json.load(f)
  print(f"Part 1: {recursive_count(data)}")
  print(f"Part 2: {recursive_count_ignore_red(data, True)}")
