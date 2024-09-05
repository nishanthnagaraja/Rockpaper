import random
from collections import defaultdict

# Moves and winning logic
MOVES = ['rock', 'paper', 'scissors']
WINNING_MOVES = {'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}

class RockPaperScissorsPlayer:
    def __init__(self):
        # Dictionary to store the history of opponent's moves
        self.opponent_history = []
        # Dictionary to count the occurrences of move pairs for Markov prediction
        self.transition_matrix = defaultdict(lambda: defaultdict(int))

    def update_opponent_move(self, opponent_move):
        if self.opponent_history:
            # Update the transition matrix based on the last opponent move
            last_move = self.opponent_history[-1]
            self.transition_matrix[last_move][opponent_move] += 1
        # Append the move to the opponent's history
        self.opponent_history.append(opponent_move)

    def predict_opponent_move(self):
        if not self.opponent_history:
            return random.choice(MOVES)
        
        last_move = self.opponent_history[-1]
        # Get the most frequent move that follows the last move from the transition matrix
        predicted_move = max(self.transition_matrix[last_move], key=self.transition_matrix[last_move].get, default=random.choice(MOVES))
        return predicted_move

    def make_move(self):
        predicted_opponent_move = self.predict_opponent_move()
        # Return the winning move against the predicted move
        return WINNING_MOVES[predicted_opponent_move]

def play_round(player, bot_move):
    player_move = player.make_move()
    print(f"Player move: {player_move}, Bot move: {bot_move}")
    
    # Determine winner
    if player_move == bot_move:
        return "draw"
    elif WINNING_MOVES[bot_move] == player_move:
        return "player"
    else:
        return "bot"

# Example bot that plays randomly
def random_bot():
    return random.choice(MOVES)

# Game simulation
def play_match(player, bot, rounds=100):
    player_wins = 0
    bot_wins = 0
    draws = 0
    
    for _ in range(rounds):
        bot_move = bot()
        result = play_round(player, bot_move)
        if result == "player":
            player_wins += 1
        elif result == "bot":
            bot_wins += 1
        else:
            draws += 1
        
        # Update the player with the bot's move
        player.update_opponent_move(bot_move)

    return player_wins, bot_wins, draws

if __name__ == "__main__":
    player = RockPaperScissorsPlayer()
    
    # Play against a random bot
    player_wins, bot_wins, draws = play_match(player, random_bot, rounds=100)
    
    print(f"Player wins: {player_wins}, Bot wins: {bot_wins}, Draws: {draws}")
    win_rate = (player_wins / (player_wins + bot_wins + draws)) * 100
    print(f"Player win rate: {win_rate:.2f}%")
