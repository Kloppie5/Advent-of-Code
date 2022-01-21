import copy

from pathlib import Path
input_file = Path(__file__).parent / "input"

def parse_input ( input_file, debug = False ) :
  with open(input_file, "r") as f:
    data = f.read().splitlines()
    numbers = map(int,data[0].split(','))
    boards = []
    current_board = []
    for line in data[2:]:
      if line == '':
        boards.append(current_board)
        current_board = []
        continue

      current_board.append([
        int(line[0:2]),
        int(line[3:5]),
        int(line[6:8]),
        int(line[9:11]),
        int(line[12:14])
      ])
    boards.append(current_board)
  return numbers, boards

def mark_boards ( boards, number ) :
  for board in boards :
    for row in board :
      for i in range(0, len(row)) :
        if row[i] == number :
          row[i] = -1
def mark_boards_new ( boards, number ) :
  return [ [ [ \
          0 if board[y][x] == number else board[y][x] \
        for x in range(5) ] \
      for y in range(5) ] \
    for board in boards ]

def check_win ( boards ) :
  winners = []
  for board in boards :
    for i in range(0, len(board)) :
      if sum(board[i]) == -5 :
        winners.append(board)
        break
      if sum([row[i] for row in board]) == -5 :
        winners.append(board)
        break
  return winners
def remove_winners ( boards, winners ) :
  boards_new = []
  for board in boards :
    if board not in winners :
      boards_new.append(board)
  return boards_new

def calculate_score ( board ) :
  return sum([sum([x for x in row if x != -1]) for row in board])

if __name__ == "__main__":
  numbers, boards = parse_input(input_file)
  win_scores = []
  for number in numbers :
    mark_boards(boards, number)
    winners = check_win(boards)
    if winners != [] :
      win_scores.append(number * calculate_score(winners[0]))
      boards = remove_winners(boards, winners)

  print(f"Part 1: {win_scores[0]}")
  print(f"Part 2: {win_scores[-1]}")
