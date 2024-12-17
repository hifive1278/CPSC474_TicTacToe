# simulate.py

import sys
from qubic import Qubic
from baseline_agents import RandomAgent, SimpleGreedyAgent, AdvancedGreedyAgent
from mcgs_agent import AMAF_MCTSAgent, MAST_MCTSAgent, MCTSAgent
from alphabeta_agent import AlphaBetaAgent

def simulate_game(agent1, agent2, num_games=100):
    agent1_wins = 0
    agent2_wins = 0
    draws = 0

    for _ in range(num_games):
        game = Qubic()
        while not game.is_full() and game.get_winner() == None:
            if game.current_player == 1:
                move = agent1.select_move(game)
            else:
                move = agent2.select_move(game)

            if move:
                game.make_move(*move)
                if game.get_winner() == 1:
                    agent1_wins += 1
                    break
                elif game.get_winner() == 2:
                    agent2_wins += 1
                    break
            game.switch_player()

        if game.get_winner() == 0:
            draws += 1

    return agent1_wins, agent2_wins, draws

def run_simulations(num_games):
    random_agent = RandomAgent()
    simple_greedy_agent = SimpleGreedyAgent()
    advanced_greedy_agent = AdvancedGreedyAgent()
    amaf_agent = AMAF_MCTSAgent()
    mast_agent = MAST_MCTSAgent()
    mcts_agent = MCTSAgent()
    alphabeta_agent = AlphaBetaAgent()

    print(f"Running simulations with {num_games} games each...")

    print("\nRandom Agent vs Simple Greedy Agent:")
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
    
    print("\nMCTS Agent vs Advanced Greedy Agent:")
    agent1_wins, agent2_wins, draws = simulate_game(mcts_agent, advanced_greedy_agent, num_games)
    print(f"MCTS wins: {agent1_wins} ({agent1_wins/num_games*100:.2f}%)")
    print(f"Advanced Greedy Agent wins: {agent2_wins} ({agent2_wins/num_games*100:.2f}%)")
    print(f"Draws: {draws} ({draws/num_games*100:.2f}%)")
    
    print("\nMAST Agent vs Advanced Greedy Agent:")
    agent1_wins, agent2_wins, draws = simulate_game(mast_agent, advanced_greedy_agent, num_games)
    print(f"MAST wins: {agent1_wins} ({agent1_wins/num_games*100:.2f}%)")
    print(f"Advanced Greedy Agent wins: {agent2_wins} ({agent2_wins/num_games*100:.2f}%)")
    print(f"Draws: {draws} ({draws/num_games*100:.2f}%)")
    
    print("\nAMAF Agent vs Advanced Greedy Agent:")
    agent1_wins, agent2_wins, draws = simulate_game(amaf_agent, advanced_greedy_agent, num_games)
    print(f"AMAF wins: {agent1_wins} ({agent1_wins/num_games*100:.2f}%)")
    print(f"Advanced Greedy Agent wins: {agent2_wins} ({agent2_wins/num_games*100:.2f}%)")
    print(f"Draws: {draws} ({draws/num_games*100:.2f}%)")

    # print("\nAlpha Beta Agent vs Random Agent:")
    # agent1_wins, agent2_wins, draws = simulate_game(alphabeta_agent, random_agent, num_games)
    # print(f"Alpha Beta Agent wins: {agent1_wins} ({agent1_wins/num_games*100:.2f}%)")
    # print(f"Random Agent wins: {agent2_wins} ({agent2_wins/num_games*100:.2f}%)")
    # print(f"Draws: {draws} ({draws/num_games*100:.2f}%)")

    # print("\nAlpha Beta Agent vs Simple Greedy Agent:")
    # agent1_wins, agent2_wins, draws = simulate_game(alphabeta_agent, simple_greedy_agent, num_games)
    # print(f"Alpha Beta Agent wins: {agent1_wins} ({agent1_wins/num_games*100:.2f}%)")
    # print(f"Simple Greedy Agent wins: {agent2_wins} ({agent2_wins/num_games*100:.2f}%)")
    # print(f"Draws: {draws} ({draws/num_games*100:.2f}%)")

    print("\nAlpha Beta Agent vs Advanced Greedy Agent:")
    agent1_wins, agent2_wins, draws = simulate_game(alphabeta_agent, advanced_greedy_agent, num_games)
    print(f"Alpha Beta Agent wins: {agent1_wins} ({agent1_wins/num_games*100:.2f}%)")
    print(f"Advanced Greedy Agent wins: {agent2_wins} ({agent2_wins/num_games*100:.2f}%)")
    print(f"Draws: {draws} ({draws/num_games*100:.2f}%)")

    # print("\nAlpha Beta Agent vs Random Agent:")
    # agent1_wins, agent2_wins, draws = simulate_game(alphabeta_agent, random_agent, num_games)
    # print(f"Alpha Beta Agent wins: {agent1_wins} ({agent1_wins/num_games*100:.2f}%)")
    # print(f"Random Agent wins: {agent2_wins} ({agent2_wins/num_games*100:.2f}%)")
    # print(f"Draws: {draws} ({draws/num_games*100:.2f}%)")

    # print("\nAlpha Beta Agent vs Simple Greedy Agent:")
    # agent1_wins, agent2_wins, draws = simulate_game(alphabeta_agent, simple_greedy_agent, num_games)
    # print(f"Alpha Beta Agent wins: {agent1_wins} ({agent1_wins/num_games*100:.2f}%)")
    # print(f"Simple Greedy Agent wins: {agent2_wins} ({agent2_wins/num_games*100:.2f}%)")
    # print(f"Draws: {draws} ({draws/num_games*100:.2f}%)")

    print("\nAlpha Beta Agent vs Advanced Greedy Agent:")
    agent1_wins, agent2_wins, draws = simulate_game(alphabeta_agent, advanced_greedy_agent, num_games)
    print(f"Alpha Beta Agent wins: {agent1_wins} ({agent1_wins/num_games*100:.2f}%)")
    print(f"Advanced Greedy Agent wins: {agent2_wins} ({agent2_wins/num_games*100:.2f}%)")
    print(f"Draws: {draws} ({draws/num_games*100:.2f}%)")

if __name__ == "__main__":
    # Default number of games
    num_games = 10

    # Check if a command-line argument is provided
    if len(sys.argv) > 1:
        try:
            num_games = int(sys.argv[1])
        except ValueError:
            print("Invalid argument. Please provide a valid integer for the number of games.")
            sys.exit(1)

    run_simulations(num_games)