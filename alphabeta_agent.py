# alphabeta_agent.py

# import random
import time
from heuristics import static_evaluator_eval1

class AlphaBetaAgent:
    def __init__(self):
        pass

    def select_move(self, game):
        start_time = time.time()
        depth = 1
        time_limit = 6  # seconds
        deepest_move = None
        deepest_score = float('-inf')

        while True:
            if depth > 3:
                break

            print(game.display_board())

            score, move = self.minimax(game, depth, True)
            print()

            print(f"Depth {depth}: Best Score: {score}, Best Move: {move}")
            deepest_score = score
            deepest_move = move

            print(f"Passed depth of {depth}\n")
            depth += 1

        print(f"Selected Move: {deepest_move}\n")
        return deepest_move


    def minimax(self, game, depth, is_maximizing):
        winner = game.check_winner()
        if winner != 0:
            return (float('inf') if winner == game.current_player else float('-inf'), None)
        if game.is_full() or depth == 0:
            return (static_evaluator_eval1(game.board, 1), None)

        if is_maximizing:
            max_eval = float('-inf')
            best_move = None
            for move in self.get_legal_moves(game):
                game.board[move[0]][move[1]][move[2]] = game.current_player
                game.switch_player()
                eval, _ = self.minimax(game, depth - 1, False)
                game.board[move[0]][move[1]][move[2]] = 0  # Undo move
                game.switch_player()  # Switch back player
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return (max_eval, best_move)
        else:
            min_eval = float('inf')
            best_move = None
            for move in self.get_legal_moves(game):
                game.board[move[0]][move[1]][move[2]] = game.current_player
                game.switch_player()
                eval, _ = self.minimax(game, depth - 1, True)
                game.board[move[0]][move[1]][move[2]] = 0  # Undo move
                game.switch_player()  # Switch back player
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return (min_eval, best_move)

    def get_legal_moves(self, game):
        return [(x, y, z) for x in range(4) for y in range(4) for z in range(4) if game.board[x][y][z] == 0]
