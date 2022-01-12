from pathlib import Path
input_file = Path(__file__).parent / "input"

def increment_password ( password ) :
  password = list(password)
  for i in range(len(password)-1, -1, -1) :
    if password[i] == 'z' :
      password[i] = 'a'
    else :
      password[i] = chr(ord(password[i])+1)
      if password[i] == 'i' or password[i] == 'o' or password[i] == 'l' :
        password[i] = chr(ord(password[i])+1)
      break
  return ''.join(password)

def validate_password ( password, debug = False ) :
  # Check for 'i', 'o', 'l'
  if 'i' in password or 'o' in password or 'l' in password :
    if debug :
      print(f"{password} has a bad letter")
    return False

  # Check for 2 non-overlapping pairs
  pair_index = -1
  for i in range(len(password)-1) :
    if password[i] == password[i+1] :
      if pair_index == -1 :
        pair_index = i
      else :
        if pair_index != i-1 :
          pair_index = -2
          break
  if pair_index != -2 :
    if debug :
      print(f"{password} has too few pairs")
    return False

  # Check for 2 increasing letters
  increasing = False
  for i in range(len(password)-2) :
    if ord(password[i])+1 == ord(password[i+1]) and ord(password[i])+2 == ord(password[i+2]) :
      return True
  if debug :
    print(f"{password} has no increasing letters")

  return False

if __name__ == "__main__":
  with open(input_file, "r") as f:
    previous_password = f.readline().strip()

  password = increment_password(previous_password)
  while ( not validate_password(password) ) :
    password = increment_password(password)
  print(f"Part 1: The next valid password: {password}")

  password = increment_password(password)
  while ( not validate_password(password) ) :
    password = increment_password(password)
  print(f"Part 2: The next valid password: {password}")
