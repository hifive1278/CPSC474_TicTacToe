import time
from math import sqrt, log
from random import choice, random

class MCTSAgent:
    def __init__(self, exploration_constant=1.414):
        self.exploration_constant = exploration_constant
        self.tree = {}  # transposition table

    def select_move(self, game, time_limit=3.5):
        start_time = time.perf_counter()
        game_state = self._get_state_key(game)
        
        if game_state not in self.tree:
            self.tree[game_state] = {
                'visits': 0,
                'wins': 0,
                'children': {},
                'moves': game.get_legal_moves()
            }

        root_node = self.tree[game_state]
        
        while time.perf_counter() - start_time < time_limit:
            node = root_node
            state_key = game_state
            sim_game = game.clone()
            
            # Selection and Expansion
            path = [(state_key, None)]
            while node['moves'] == [] and node['children'] and not sim_game.is_terminal():
                best_move = self._select_uct(node, sim_game.current_player)
                sim_game.make_move(*best_move)
                sim_game.switch_player()
                state_key = self._get_state_key(sim_game)
                
                if state_key not in self.tree:
                    self.tree[state_key] = {
                        'visits': 0,
                        'wins': 0,
                        'children': {},
                        'moves': sim_game.get_legal_moves()
                    }
                
                node = self.tree[state_key]
                path.append((state_key, best_move))
            
            # Expand if not terminal
            if not sim_game.is_terminal() and node['moves']:
                move = node['moves'].pop()
                sim_game.make_move(*move)
                sim_game.switch_player()
                next_state_key = self._get_state_key(sim_game)
                
                if next_state_key not in self.tree:
                    self.tree[next_state_key] = {
                        'visits': 0,
                        'wins': 0,
                        'children': {},
                        'moves': sim_game.get_legal_moves()
                    }
                
                node['children'][move] = next_state_key
                path.append((next_state_key, move))
            
            # Simulation
            while not sim_game.is_terminal():
                legal_moves = sim_game.get_legal_moves()
                if not legal_moves:
                    break
                move = choice(legal_moves)
                sim_game.make_move(*move)
                sim_game.switch_player()
            
            # Backpropagation
            winner = sim_game.get_winner()
            for state_key, _ in path:
                node = self.tree[state_key]
                node['visits'] += 1
                if winner == game.current_player:
                    node['wins'] += 1
                elif winner == 0:  # Draw
                    node['wins'] += 0.5
        
        # Select best move
        best_move = None
        best_visits = -float('inf')
        for move in root_node['children']:
            child_key = root_node['children'][move]
            child_visits = self.tree[child_key]['visits']
            if child_visits > best_visits:
                best_visits = child_visits
                best_move = move
                
        return best_move

    def _get_state_key(self, game):
        # Convert board state to immutable tuple for hashing
        return (tuple(tuple(tuple(plane) for plane in board) 
                for board in game.board), game.current_player)

    def _select_uct(self, node, player):
        total_visits = node['visits']
        best_score = float('-inf')
        best_move = None

        for move, child_key in node['children'].items():
            child = self.tree[child_key]
            if child['visits'] == 0:
                score = float('inf')
            else:
                exploitation = child['wins'] / child['visits']
                if player != 1:  # if minimizing player
                    exploitation = 1 - exploitation
                exploration = self.exploration_constant * sqrt(log(total_visits) / child['visits'])
                score = exploitation + exploration

            if score > best_score:
                best_score = score
                best_move = move

        return best_move


class AMAF_MCTSAgent:
    def __init__(self, exploration_constant=1.414, amaf_constant=0.5):
        self.exploration_constant = exploration_constant
        self.amaf_constant = amaf_constant
        self.tree = {}  # transposition table

    def select_move(self, game, time_limit=3.5):
        start_time = time.perf_counter()
        game_state = self._get_state_key(game)
        
        if game_state not in self.tree:
            self.tree[game_state] = {
                'visits': 0,
                'wins': 0,
                'children': {},
                'moves': game.get_legal_moves(),
                'amaf_visits': {},
                'amaf_wins': {}
            }

        root_node = self.tree[game_state]
        
        while time.perf_counter() - start_time < time_limit:
            node = root_node
            state_key = game_state
            sim_game = game.clone()
            
            # Selection and Expansion
            path = [(state_key, None)]
            moves_made = set()
            while node['moves'] == [] and node['children'] and not sim_game.is_terminal():
                best_move = self._select_uct_amaf(node, sim_game.current_player)
                sim_game.make_move(*best_move)
                sim_game.switch_player()
                state_key = self._get_state_key(sim_game)
                moves_made.add(best_move)
                
                if state_key not in self.tree:
                    self.tree[state_key] = {
                        'visits': 0,
                        'wins': 0,
                        'children': {},
                        'moves': sim_game.get_legal_moves(),
                        'amaf_visits': {},
                        'amaf_wins': {}
                    }
                
                node = self.tree[state_key]
                path.append((state_key, best_move))
            
            # Expand if not terminal
            if not sim_game.is_terminal() and node['moves']:
                move = node['moves'].pop()
                sim_game.make_move(*move)
                sim_game.switch_player()
                next_state_key = self._get_state_key(sim_game)
                moves_made.add(move)
                
                if next_state_key not in self.tree:
                    self.tree[next_state_key] = {
                        'visits': 0,
                        'wins': 0,
                        'children': {},
                        'moves': sim_game.get_legal_moves(),
                        'amaf_visits': {},
                        'amaf_wins': {}
                    }
                
                node['children'][move] = next_state_key
                path.append((next_state_key, move))
            
            # Simulation
            while not sim_game.is_terminal():
                legal_moves = sim_game.get_legal_moves()
                if not legal_moves:
                    break
                move = choice(legal_moves)
                sim_game.make_move(*move)
                sim_game.switch_player()
                moves_made.add(move)
            
            # Backpropagation
            winner = sim_game.get_winner()
            for state_key, _ in path:
                node = self.tree[state_key]
                node['visits'] += 1
                if winner == game.current_player:
                    node['wins'] += 1
                elif winner == 0:  # Draw
                    node['wins'] += 0.5
                
                # Update AMAF statistics
                for move in moves_made:
                    if move not in node['amaf_visits']:
                        node['amaf_visits'][move] = 0
                        node['amaf_wins'][move] = 0
                    node['amaf_visits'][move] += 1
                    if winner == game.current_player:
                        node['amaf_wins'][move] += 1
                    elif winner == 0:  # Draw
                        node['amaf_wins'][move] += 0.5
        
        # Select best move
        best_move = None
        best_visits = -float('inf')
        for move in root_node['children']:
            child_key = root_node['children'][move]
            child_visits = self.tree[child_key]['visits']
            if child_visits > best_visits:
                best_visits = child_visits
                best_move = move
                
        return best_move

    def _get_state_key(self, game):
        # Convert board state to immutable tuple for hashing
        return (tuple(tuple(tuple(plane) for plane in board) 
                for board in game.board), game.current_player)

    def _select_uct_amaf(self, node, player):
        total_visits = node['visits']
        best_score = float('-inf')
        best_move = None

        for move, child_key in node['children'].items():
            child = self.tree[child_key]
            if child['visits'] == 0:
                score = float('inf')
            else:
                mc_score = child['wins'] / child['visits']
                amaf_score = node['amaf_wins'].get(move, 0) / max(node['amaf_visits'].get(move, 1), 1)
                
                beta = node['amaf_visits'].get(move, 0) / (node['amaf_visits'].get(move, 0) + child['visits'] + 1e-5 * node['amaf_visits'].get(move, 0) * child['visits'])
                exploitation = (1 - beta) * mc_score + beta * amaf_score
                
                if player != 1:  # if minimizing player
                    exploitation = 1 - exploitation
                exploration = self.exploration_constant * sqrt(log(total_visits) / child['visits'])
                score = exploitation + exploration

            if score > best_score:
                best_score = score
                best_move = move

        return best_move


class MAST_MCTSAgent:
    def __init__(self, exploration_constant=1.414, mast_constant=0.15):
        self.exploration_constant = exploration_constant
        self.mast_constant = mast_constant
        self.tree = {}  # transposition table
        self.move_stats = {}  # MAST statistics

    def _init_move_stats(self, move):
        if move not in self.move_stats:
            self.move_stats[move] = {
                'reward': 0,
                'count': 0
            }

    def _update_move_stats(self, move, reward):
        self._init_move_stats(move)
        self.move_stats[move]['reward'] += reward
        self.move_stats[move]['count'] += 1

    def _get_move_value(self, move):
        if move in self.move_stats and self.move_stats[move]['count'] > 0:
            return self.move_stats[move]['reward'] / self.move_stats[move]['count']
        return 0.5

    def select_move(self, game, time_limit=5):
        start_time = time.perf_counter()
        game_state = self._get_state_key(game)
        
        if game_state not in self.tree:
            self.tree[game_state] = {
                'visits': 0,
                'wins': 0,
                'children': {},
                'moves': game.get_legal_moves()
            }

        root_node = self.tree[game_state]
        
        while time.perf_counter() - start_time < time_limit:
            moves_in_simulation = []
            node = root_node
            state_key = game_state
            sim_game = game.clone()
            
            # Selection
            path = [(state_key, None)]
            while node['moves'] == [] and node['children'] and not sim_game.is_terminal():
                move = self._select_uct(node, sim_game.current_player)
                moves_in_simulation.append(move)
                sim_game.make_move(*move)
                sim_game.switch_player()
                state_key = self._get_state_key(sim_game)
                
                if state_key not in self.tree:
                    self.tree[state_key] = {
                        'visits': 0,
                        'wins': 0,
                        'children': {},
                        'moves': sim_game.get_legal_moves()
                    }
                
                node = self.tree[state_key]
                path.append((state_key, move))

             # Expand if not terminal
            if not sim_game.is_terminal() and node['moves']:
                move = node['moves'].pop()
                sim_game.make_move(*move)
                sim_game.switch_player()
                next_state_key = self._get_state_key(sim_game)
                
                if next_state_key not in self.tree:
                    self.tree[next_state_key] = {
                        'visits': 0,
                        'wins': 0,
                        'children': {},
                        'moves': sim_game.get_legal_moves()
                    }
                
                node['children'][move] = next_state_key
                path.append((next_state_key, move))
                
            # MAST-guided simulation
            while not sim_game.is_terminal():
                legal_moves = sim_game.get_legal_moves()
                if not legal_moves:
                    break
                
                # Use MAST values to select moves
                if random() < self.mast_constant:
                    move = max(legal_moves, 
                             key=lambda m: self._get_move_value(m))
                else:
                    move = choice(legal_moves)
                
                moves_in_simulation.append(move)
                sim_game.make_move(*move)
                sim_game.switch_player()

            # Backpropagation with MAST updates
            winner = sim_game.get_winner()
            reward = 1 if winner == game.current_player else (0.5 if winner == 0 else 0)
            
            # Update MAST statistics
            for move in moves_in_simulation:
                self._update_move_stats(move, reward)
            
            # Update MCTS nodes
            for state_key, _ in path:
                node = self.tree[state_key]
                node['visits'] += 1
                node['wins'] += reward

        # Select best move combining MCTS and MAST
        best_move = None
        best_value = float('-inf')
        for move, child_key in root_node['children'].items():
            child = self.tree[child_key]
            if child['visits'] == 0:
                continue
            
            mcts_value = child['wins'] / child['visits']
            mast_value = self._get_move_value(move)
            combined_value = ((1 - self.mast_constant) * mcts_value + 
                            self.mast_constant * mast_value)
            
            if combined_value > best_value:
                best_value = combined_value
                best_move = move
        
        return best_move

    def _get_state_key(self, game):
        return (tuple(tuple(tuple(plane) for plane in board) 
                for board in game.board), game.current_player)

    def _select_uct(self, node, player):
        total_visits = node['visits']
        best_score = float('-inf')
        best_move = None

        for move, child_key in node['children'].items():
            child = self.tree[child_key]
            if child['visits'] == 0:
                score = float('inf')
            else:
                exploitation = child['wins'] / child['visits']
                if player != 1:
                    exploitation = 1 - exploitation
                exploration = (self.exploration_constant * 
                             sqrt(log(total_visits) / child['visits']))
                mast_score = self._get_move_value(move)
                score = ((1 - self.mast_constant) * (exploitation + exploration) + 
                        self.mast_constant * mast_score)

            if score > best_score:
                best_score = score
                best_move = move

        return best_move
