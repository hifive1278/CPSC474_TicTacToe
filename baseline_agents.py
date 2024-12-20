'''
baseline_agents.py
the random, simple greedy, and adv. greedy agents.
'''

import random
from heuristics import simple_heuristic, static_evaluator

class RandomAgent:
    def __init__(self):
        pass

    def select_move(self, game):
        moves = [(x, y, z) for x in range(game.dimensions()) for y in range(game.dimensions()) for z in range(game.dimensions()) if game.board[x][y][z] == 0]
        return random.choice(moves) if moves else None

class SimpleGreedyAgent:
    def __init__(self):
        pass

    def select_move(self, game):
        return simple_heuristic(game)

class AdvancedGreedyAgent:
    def __init__(self):
        pass

    def select_move(self, game):
        best_move = None
        best_score = float('-inf')

        for x in range(game.dimensions()):
            for y in range(game.dimensions()):
                for z in range(game.dimensions()):
                    if game.board[x][y][z] == 0:
                        game.board[x][y][z] = game.current_player
                        score = static_evaluator(game.board, game.current_player)
                        game.board[x][y][z] = 0

                        if score > best_score:
                            best_score = score
                            best_move = (x, y, z)

        return best_move