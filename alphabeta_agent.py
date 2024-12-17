'''
alphabeta_agent.py
the alpha-beta pruning minimax agent
'''

import time
import random
from heuristics import static_evaluator, simple_heuristic

class AlphaBetaAgent:
    def __init__(self, max_depth=3, random_move_prob=0.05):
        self.max_depth = max_depth
        self.random_move_prob = random_move_prob

    def select_move(self, game):
        start_time = time.time()
        depth = 1
        score = float('-inf')
        move = None

        while True:
            if depth > self.max_depth:
                break
            
            if random.random() < self.random_move_prob:
                move = simple_heuristic(game)
            else:
                score, move = self.minimax(game, depth, True, float('-inf'), float('inf'))
                depth += 1

        return move

    def minimax(self, game, depth, is_maximizing, alpha, beta):
        winner = game.get_winner()
        if winner is not None:
            if winner == 0:
                return (0, None)
            else:
                return (float('inf') if winner == 1 else float('-inf'), None)
        if depth == 0:
            return (static_evaluator(game.board, 1), None)

        if is_maximizing:
            max_eval = float('-inf')
            best_move = None
            for move in self.get_legal_moves(game):
                game.board[move[0]][move[1]][move[2]] = game.current_player
                game.switch_player()
                eval, _ = self.minimax(game, depth - 1, False, alpha, beta)
                game.board[move[0]][move[1]][move[2]] = 0
                game.switch_player()
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return (max_eval, best_move)
        else:
            min_eval = float('inf')
            best_move = None
            for move in self.get_legal_moves(game):
                game.board[move[0]][move[1]][move[2]] = game.current_player
                game.switch_player()
                eval, _ = self.minimax(game, depth - 1, True, alpha, beta)
                game.board[move[0]][move[1]][move[2]] = 0
                game.switch_player()
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return (min_eval, best_move)

    def get_legal_moves(self, game):
        return [(x, y, z) for x in range(game.dimensions()) for y in range(game.dimensions()) for z in range(game.dimensions()) if game.board[x][y][z] == 0]
