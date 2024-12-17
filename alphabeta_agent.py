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
            if time.time() > time_limit + start_time or depth > 3: # Can change this depth max to whatever we want
                break

            # print(game.display_board())

            score, move = self.minimax(game, depth, True, float('-inf'), float('inf'))
            # print()

            # print(f"Depth {depth}: Best Score: {score}, Best Move: {move}")
            deepest_score = score
            deepest_move = move

            # print(f"Passed depth of {depth}\n")
            depth += 1

        # print(f"Selected Move: {deepest_move}\n")
        return deepest_move


    def minimax(self, game, depth, is_maximizing, alpha, beta):
        winner = game.get_winner()
        if winner is not None:
            if winner == 0:
                return (0, None)
            else:
                return (float('inf') if winner == 1 else float('-inf'), None)
        if depth == 0:
            return (static_evaluator_eval1(game.board, 1), None)

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
        return [(x, y, z) for x in range(4) for y in range(4) for z in range(4) if game.board[x][y][z] == 0]
