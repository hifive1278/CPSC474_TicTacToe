# simulate.py

from qubic import Qubic
from agents import RandomAgent, GreedyAgent

def simulate_game(agent1, agent2, num_games=100):
    agent1_wins = 0
    agent2_wins = 0
    draws = 0

    for _ in range(num_games):
        game = Qubic()
        while not game.is_full() and game.check_winner() == 0:
            if game.current_player == 1:
                move = agent1.select_move(game)
            else:
                move = agent2.select_move(game)

            if move:
                game.make_move(*move)
                if game.check_winner() == 1:
                    agent1_wins += 1
                    break
                elif game.check_winner() == 2:
                    agent2_wins += 1
                    break
            game.switch_player()

        if game.check_winner() == 0:
            draws += 1

    return agent1_wins, agent2_wins, draws

if __name__ == "__main__":
    random_agent = RandomAgent()
    greedy_agent = RandomAgent()

    num_games = 1000
    agent1_wins, agent2_wins, draws = simulate_game(random_agent, greedy_agent, num_games)

    print(f"Results after {num_games} games:")
    print(f"Random Agent wins: {agent1_wins} ({agent1_wins/num_games*100:.2f}%)")
    print(f"Greedy Agent wins: {agent2_wins} ({agent2_wins/num_games*100:.2f}%)")
    print(f"Draws: {draws} ({draws/num_games*100:.2f}%)")
