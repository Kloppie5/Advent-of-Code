from pathlib import Path
input_file = Path(__file__).parent / "input"

def parse_input ( debug = False ) :
    with open(input_file, "r") as f:
        data = f.read().splitlines()
    return data

score_lut_1 = {
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
def score_game_1 ( game ) :
    return score_lut_1[game]

score_lut_2 = {
    'A X' : 3 + 0, # 3 points for C, 0 points for loss
    'B X' : 1 + 0, # 1 point for A, 0 points for loss
    'C X' : 2 + 0, # 2 points for B, 0 points for loss
    'A Y' : 1 + 3, # 1 point for A, 3 points for draw
    'B Y' : 2 + 3, # 2 points for B, 3 points for draw
    'C Y' : 3 + 3, # 3 points for C, 3 points for draw
    'A Z' : 2 + 6, # 2 points for B, 6 points for win
    'B Z' : 3 + 6, # 3 points for C, 6 points for win
    'C Z' : 1 + 6, # 1 point for A, 6 points for win
}
def score_game_2 ( game ) :
    return score_lut_2[game]

if __name__ == "__main__":
    games = parse_input()
    
    scores_1 = [ score_game_1(game) for game in games ]
    total_score_1 = sum(scores_1)
    print(f"Part 1: {total_score_1}")

    scores_2 = [ score_game_2(game) for game in games ]
    total_score_2 = sum(scores_2)
    print(f"Part 2: {total_score_2}")
