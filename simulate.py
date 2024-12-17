'''
simulate.py
the code to run all the simulations. accepts two command line args.
'''

import sys
from qubic import Qubic
from baseline_agents import RandomAgent, SimpleGreedyAgent, AdvancedGreedyAgent
from mcts_agents import AMAF_MCTSAgent, MAST_MCTSAgent, MCTSAgent
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

def run_simulations(num_games, time_limit):
    random_agent = RandomAgent()
    simple_greedy_agent = SimpleGreedyAgent()
    advanced_greedy_agent = AdvancedGreedyAgent()
    amaf_agent = AMAF_MCTSAgent(time_limit=time_limit)
    mast_agent = MAST_MCTSAgent(time_limit=time_limit)
    mcts_agent = MCTSAgent(time_limit=time_limit)
    alphabeta_agent = AlphaBetaAgent()

    print(f"Running simulations with {num_games} games each...")

    # BASIC RUNS
    print("\nRandom Agent vs Simple Greedy Agent (10,000 games):")
    agent1_wins, agent2_wins, draws = simulate_game(random_agent, simple_greedy_agent, 10_000)
    print(f"Random Agent wins: {agent1_wins} ({agent1_wins/10_000*100:.2f}%)")
    print(f"Simple Greedy Agent wins: {agent2_wins} ({agent2_wins/10_000*100:.2f}%)")
    print(f"Draws: {draws} ({draws/10_000*100:.2f}%)")

    print("\nRandom Agent vs Advanced Greedy Agent (10,000 games):")
    agent1_wins, agent2_wins, draws = simulate_game(random_agent, advanced_greedy_agent, 10_000)
    print(f"Random Agent wins: {agent1_wins} ({agent1_wins/10_000*100:.2f}%)")
    print(f"Advanced Greedy Agent wins: {agent2_wins} ({agent2_wins/10_000*100:.2f}%)")
    print(f"Draws: {draws} ({draws/10_000*100:.2f}%)")
    
    print("\nSimple Greedy Agent vs Advanced Greedy Agent (10,000 games):")
    agent1_wins, agent2_wins, draws = simulate_game(simple_greedy_agent, advanced_greedy_agent, 10_000)
    print(f"Simple Greedy Agent wins: {agent1_wins} ({agent1_wins/10_000*100:.2f}%)")
    print(f"Advanced Greedy Agent wins: {agent2_wins} ({agent2_wins/10_000*100:.2f}%)")
    print(f"Draws: {draws} ({draws/10_000*100:.2f}%)")
    
    # BASELINES against adv. greedy
    
    print(f"\nAlpha Beta Agent vs Advanced Greedy Agent ({num_games} games):")
    agent1_wins, agent2_wins, draws = simulate_game(alphabeta_agent, advanced_greedy_agent, num_games)
    print(f"Alpha Beta Agent wins: {agent1_wins} ({agent1_wins/num_games*100:.2f}%)")
    print(f"Advanced Greedy Agent wins: {agent2_wins} ({agent2_wins/num_games*100:.2f}%)")
    print(f"Draws: {draws} ({draws/num_games*100:.2f}%)")
    
    print(f"\nMCTS Agent vs Advanced Greedy Agent ({num_games} games):")
    agent1_wins, agent2_wins, draws = simulate_game(mcts_agent, advanced_greedy_agent, num_games)
    print(f"MCTS wins: {agent1_wins} ({agent1_wins/num_games*100:.2f}%)")
    print(f"Advanced Greedy Agent wins: {agent2_wins} ({agent2_wins/num_games*100:.2f}%)")
    print(f"Draws: {draws} ({draws/num_games*100:.2f}%)")
    
    # HEAD TO HEADS... 
    
    print(f"\nAlpha Beta Agent vs MCTS Agent ({num_games} games):")
    agent1_wins, agent2_wins, draws = simulate_game(alphabeta_agent, mcts_agent, num_games)
    print(f"Alpha Beta Agent wins: {agent1_wins} ({agent1_wins/num_games*100:.2f}%)")
    print(f"MCTS Agent wins: {agent2_wins} ({agent2_wins/num_games*100:.2f}%)")
    print(f"Draws: {draws} ({draws/num_games*100:.2f}%)")
    
    print(f"\nAlpha Beta Agent vs MAST Agent ({num_games} games):")
    agent1_wins, agent2_wins, draws = simulate_game(alphabeta_agent, mast_agent, num_games)
    print(f"Alpha Beta Agent wins: {agent1_wins} ({agent1_wins/num_games*100:.2f}%)")
    print(f"MAST Agent wins: {agent2_wins} ({agent2_wins/num_games*100:.2f}%)")
    print(f"Draws: {draws} ({draws/num_games*100:.2f}%)")
    
    print(f"\nAlpha Beta Agent vs AMAF Agent ({num_games} games):")
    agent1_wins, agent2_wins, draws = simulate_game(alphabeta_agent, amaf_agent, num_games)
    print(f"Alpha Beta Agent wins: {agent1_wins} ({agent1_wins/num_games*100:.2f}%)")
    print(f"AMAF Agent wins: {agent2_wins} ({agent2_wins/num_games*100:.2f}%)")
    print(f"Draws: {draws} ({draws/num_games*100:.2f}%)")
    
    # investigation of why MCTS sucked...
    
    print(f"\nMAST Agent vs Advanced Greedy Agent ({num_games} games):")
    agent1_wins, agent2_wins, draws = simulate_game(mast_agent, advanced_greedy_agent, num_games)
    print(f"MAST wins: {agent1_wins} ({agent1_wins/num_games*100:.2f}%)")
    print(f"Advanced Greedy Agent wins: {agent2_wins} ({agent2_wins/num_games*100:.2f}%)")
    print(f"Draws: {draws} ({draws/num_games*100:.2f}%)")
    
    print(f"\nAMAF Agent vs Advanced Greedy Agent ({num_games} games):")
    agent1_wins, agent2_wins, draws = simulate_game(amaf_agent, advanced_greedy_agent, num_games)
    print(f"AMAF wins: {agent1_wins} ({agent1_wins/num_games*100:.2f}%)")
    print(f"Advanced Greedy Agent wins: {agent2_wins} ({agent2_wins/num_games*100:.2f}%)")
    print(f"Draws: {draws} ({draws/num_games*100:.2f}%)")

if __name__ == "__main__":
    # default values
    num_games = 5
    time_limit = 1.0

    # Parse command line arguments
    if len(sys.argv) > 2:
        try:
            num_games = int(sys.argv[1])
            time_limit = float(sys.argv[2])
        except ValueError:
            print("Invalid arguments. Usage: python script.py <num_games> <time_limit>")
            print("Example: python script.py 10 2.5")
            sys.exit(1)
    elif len(sys.argv) > 1:
        try:
            num_games = int(sys.argv[1])
        except ValueError:
            print("Invalid argument. Please provide a valid integer for the number of games.")
            sys.exit(1)

    run_simulations(num_games, time_limit)