# simulate.py

from qubic import Qubic
from agents import RandomAgent, SimpleGreedyAgent, AdvancedGreedyAgent

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
    simple_greedy_agent = SimpleGreedyAgent()
    advanced_greedy_agent = AdvancedGreedyAgent()

    num_games = 100

    print("Random Agent vs Simple Greedy Agent:")
    agent1_wins, agent2_wins, draws = simulate_game(random_agent, simple_greedy_agent, num_games)
    print(f"Random Agent wins: {agent1_wins} ({agent1_wins/num_games*100:.2f}%)")
    print(f"Simple Greedy Agent wins: {agent2_wins} ({agent2_wins/num_games*100:.2f}%)")
    print(f"Draws: {draws} ({draws/num_games*100:.2f}%)")

    print("\nRandom Agent vs Advanced Greedy Agent:")
    agent1_wins, agent2_wins, draws = simulate_game(random_agent, advanced_greedy_agent, num_games)
    print(f"Random Agent wins: {agent1_wins} ({agent1_wins/num_games*100:.2f}%)")
    print(f"Advanced Greedy Agent wins: {agent2_wins} ({agent2_wins/num_games*100:.2f}%)")
    print(f"Draws: {draws} ({draws/num_games*100:.2f}%)")

    print("\nSimple Greedy Agent vs Advanced Greedy Agent:")
    agent1_wins, agent2_wins, draws = simulate_game(simple_greedy_agent, advanced_greedy_agent, num_games)
    print(f"Simple Greedy Agent wins: {agent1_wins} ({agent1_wins/num_games*100:.2f}%)")
    print(f"Advanced Greedy Agent wins: {agent2_wins} ({agent2_wins/num_games*100:.2f}%)")
    print(f"Draws: {draws} ({draws/num_games*100:.2f}%)")