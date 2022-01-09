from pathlib import Path
input_file = Path(__file__).parent / "input"

def wrapping_paper_required ( l, w, h, debug = False ):
  lw = l * w
  lh = l * h
  wh = w * h
  slack = min(lw, lh, wh)
  wrapping_paper = 2*lw + 2*lh + 2*wh + slack
  if debug:
    print(f"{l}x{w}x{h} requires {wrapping_paper} square feet of wrapping paper.")
  return wrapping_paper

if __name__ == "__main__":
  with input_file.open() as f:
    data = f.read().strip()
    data = data.split("\n")
    total = 0
    for line in data:
      l, w, h = [int(x) for x in line.split("x")]
      total += wrapping_paper_required(l, w, h)
    print(f"Part 1: The total wrapping paper required is {total} square feet.")
