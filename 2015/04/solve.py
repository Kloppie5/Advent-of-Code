import hashlib

from pathlib import Path
input_file = Path(__file__).parent / "input"

def mine_adventcoin ( key, debug = False ) :
  for i in range(0, 1000000):
    digest = hashlib.md5(key.encode('utf-8') + str(i).encode('utf-8')).hexdigest()
    if debug:
      print(f"{i}: {digest}")
    if digest.startswith("00000"):
      return i

if __name__ == "__main__":
  with input_file.open() as f:
    key = f.read().strip()
  print(f"Part 1: Mined AdventCoin with PoW: {mine_adventcoin(key)}")
