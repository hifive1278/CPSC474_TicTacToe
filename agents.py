# agents.py

import random

class RandomAgent:
    def __init__(self):
        pass

    def select_move(self, game):
        moves = [(x, y, z) for x in range(4) for y in range(4) for z in range(4) if game.board[x][y][z] == 0]
        return random.choice(moves) if moves else None

class GreedyAgent:
    def __init__(self):
        pass

    def select_move(self, game):
        # Simple heuristic: choose the first available move that completes a line
        for line in game.generate_lines():
            player_count = sum(1 for x, y, z in line if game.board[x][y][z] == game.current_player)
            empty_count = sum(1 for x, y, z in line if game.board[x][y][z] == 0)
            if player_count == 3 and empty_count == 1:
                for x, y, z in line:
                    if game.board[x][y][z] == 0:
                        return (x, y, z)
        
        # If no winning move, choose the first empty space
        for x in range(4):
            for y in range(4):
                for z in range(4):
                    if game.board[x][y][z] == 0:
                        return (x, y, z)
        return None
