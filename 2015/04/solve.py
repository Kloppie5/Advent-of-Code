import hashlib

from pathlib import Path
input_file = Path(__file__).parent / "input"

def mine_adventcoin ( key, difficulty, debug = False ) :
  target = '0' * difficulty
  for i in range(0, 10000000):
    digest = hashlib.md5(key.encode('utf-8') + str(i).encode('utf-8')).hexdigest()
    if debug:
      print(f"{i}: {digest}")
    if digest.startswith(target):
      return i

if __name__ == "__main__":
  with input_file.open() as f:
    key = f.read().strip()
  print(f"Part 1: Mined AdventCoin with PoW: {mine_adventcoin(key, 5)}")
  print(f"Part 2: Mined AdventCoin with PoW: {mine_adventcoin(key, 6)}")
