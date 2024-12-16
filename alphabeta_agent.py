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
        time_limit = 6 # seconds
        best_move = None
        best_score = float('-inf')

        while True:
            curr_best_move = None
            curr_best_score = float('-inf')

            for move in self.get_legal_moves(game):
                if time.time() > start_time+time_limit or depth > 20:
                    break
                # if depth > 4:
                #     break
                game.make_move(*move)
                score = self.minimax(game, depth - 1, True, float('-inf'), float('inf'))
                game.board[move[0]][move[1]][move[2]] = 0  # Undo move
                #game.switch_player()  # Switch back player
                if score > curr_best_score:
                    curr_best_score = score
                    curr_best_move = move

            if time.time() > start_time+time_limit or depth > 20:
                break
            # if depth > 4:
            #     break
            
            if curr_best_score > best_score:
                best_score = curr_best_score
                best_move = curr_best_move

            print("Passed depth of " + str(depth))
            depth += 1
        
        print(best_move)
        return best_move

    def minimax(self, game, depth, is_maximizing, alpha, beta):
        winner = game.check_winner()
        if winner != 0:
            return float('inf') if winner == game.current_player else float('-inf')
        if game.is_full() or depth == 0:
            return static_evaluator_eval1(game.board, game.current_player)

        if is_maximizing:
            max_eval = float('-inf')
            for move in self.get_legal_moves(game):
                game.make_move(*move)
                # game.switch_player() # maybe??
                eval = self.minimax(game, depth - 1, False, alpha, beta)
                game.board[move[0]][move[1]][move[2]] = 0  # Undo move
                #game.switch_player()  # Switch back player
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_legal_moves(game):
                game.make_move(*move)
                # game.switch_player() # maybe??
                eval = self.minimax(game, depth - 1, True, alpha, beta)
                game.board[move[0]][move[1]][move[2]] = 0  # Undo move
                #game.switch_player()  # Switch back player
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_legal_moves(self, game):
        return [(x, y, z) for x in range(4) for y in range(4) for z in range(4) if game.board[x][y][z] == 0]
