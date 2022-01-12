from pathlib import Path
input_file = Path(__file__).parent / "input"

def look_and_say ( word, rounds, debug = False ) :
  for i in range(rounds) :
    if debug :
      print(f"Round {i+1}; {word} -> ", end="")

    word = word.replace("1", "a")
    word = word.replace("2", "b")
    word = word.replace("3", "c")

    word = word.replace("aaa", "31")
    word = word.replace("bbb", "32")
    # ccc is impossible
    word = word.replace("aa", "21")
    word = word.replace("bb", "22")
    word = word.replace("cc", "23")
    word = word.replace("a", "11")
    word = word.replace("b", "12")
    word = word.replace("c", "13")

    if debug :
      print(word)

  return word

if __name__ == "__main__":
  with open(input_file, "r") as f:
    start = f.readline().strip()
  word = look_and_say(start, 40)
  print(f"Part 1: After 40 rounds, the input as length {len(word)}; {word}")
