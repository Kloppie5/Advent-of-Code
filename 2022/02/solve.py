from pathlib import Path
input_file = Path(__file__).parent / "input"

def parse_input ( debug = False ) :
    with open(input_file, "r") as f:
        data = f.read().splitlines()
    return data

score_lut = {
    'A X' : 1 + 3, # 1 point for X, 3 points for draw
    'B X' : 1 + 0, # 1 point for X, 0 points for loss
    'C X' : 1 + 6, # 1 point for X, 6 points for win
    'A Y' : 2 + 6, # 2 points for Y, 6 points for win
    'B Y' : 2 + 3, # 2 points for Y, 3 points for draw
    'C Y' : 2 + 0, # 2 points for Y, 0 points for loss
    'A Z' : 3 + 0, # 3 points for Z, 0 points for loss
    'B Z' : 3 + 6, # 3 points for Z, 6 points for win
    'C Z' : 3 + 3, # 3 points for Z, 3 points for draw
}
def score_game ( game ) :
    return score_lut[game]

if __name__ == "__main__":
    games = parse_input()
    scores = [ score_game(game) for game in games ]
    total_score = sum(scores)
    print(f"Part 1: {total_score}")
