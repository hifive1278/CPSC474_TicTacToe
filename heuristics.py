# heuristics.py

from qubic import Qubic

game = Qubic()

def simple_heuristic(game):
    # Simple heuristic: choose the first available move that completes a line
    for line in game.generate_lines():
        player_count = sum(1 for x, y, z in line if game.board[x][y][z] == game.current_player)
        empty_count = sum(1 for x, y, z in line if game.board[x][y][z] == 0)
        if player_count == 3 and empty_count == 1:
            for x, y, z in line:
                if game.board[x][y][z] == 0:
                    return (x, y, z)
    
    # If no winning move, choose the first empty space
    for x in range(game.dimensions()):
        for y in range(game.dimensions()):
            for z in range(game.dimensions()):
                if game.board[x][y][z] == 0:
                    return (x, y, z)
    return None

def static_evaluator_eval1(board, player):
    opponent = 3 - player
    player_score = 0
    opponent_score = 0
    
    # Define the value of n-in-a-rows
    values = {1: 1, 2: 10, 3: 100, 4: 1000}
    opponent_multiplier = 1.1  # Opponent's rows are slightly more valuable

    # Generate all possible lines
    lines = game.generate_lines()

    # Count n-in-a-rows for each player
    player_counts = {1: 0, 2: 0, 3: 0, 4: 0}
    opponent_counts = {1: 0, 2: 0, 3: 0, 4: 0}

    for line in lines:
        player_pieces = sum(1 for x, y, z in line if board[x][y][z] == player)
        opponent_pieces = sum(1 for x, y, z in line if board[x][y][z] == opponent)

        if player_pieces > 0 and opponent_pieces == 0:
            player_counts[player_pieces] += 1
        elif opponent_pieces > 0 and player_pieces == 0:
            opponent_counts[opponent_pieces] += 1

    # Calculate scores
    for n in range(1, game.dimensions()+1):
        player_score += player_counts[n] * values[n]
        opponent_score += opponent_counts[n] * values[n] * opponent_multiplier

    if player_counts[4] != 0:
        return float('inf')
    if opponent_counts[4] != 0:
        return float('-inf')

    return player_score - opponent_score
