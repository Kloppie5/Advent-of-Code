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

def ribbon_required ( l, w, h, debug = False ):
  base_length = 2*(l + w + h - max(l, w, h))
  bow = l * w * h
  if debug:
    print(f"{l}x{w}x{h} requires {base_length} + {bow} feet of ribbon.")
  return base_length + bow

if __name__ == "__main__":
  with input_file.open() as f:
    data = f.read().strip()
    data = data.split("\n")
    total_wrapping_paper = 0
    total_ribbon = 0
    for line in data:
      l, w, h = [int(x) for x in line.split("x")]
      total_wrapping_paper += wrapping_paper_required(l, w, h)
      total_ribbon += ribbon_required(l, w, h)

    print(f"Part 1: The total wrapping paper required is {total_wrapping_paper} square feet.")
    print(f"Part 2: The total ribbon required is {total_ribbon} feet.")
