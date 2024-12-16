# # qubic.py

# class Qubic:
#     def __init__(self):
#         # Initialize a 4x4x4 board
#         self.board = [[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)]
#         self.current_player = 1

#     def make_move(self, x, y, z):
#         # Place a move on the board
#         if self.board[x][y][z] == 0:
#             self.board[x][y][z] = self.current_player
#             return True
#         return False

#     def switch_player(self):
#         # Switch the current player, since 3-2=1 and 3-1=2
#         self.current_player = 3 - self.current_player

#     def is_valid_move(self, x, y, z):
#         return 0 <= x < 4 and 0 <= y < 4 and 0 <= z < 4 and self.board[x][y][z] == 0
    
#     def get_legal_moves(self):
#         moves = []
#         for x in range(4):
#             for y in range(4):
#                 for z in range(4):
#                     if self.board[x][y][z] == 0:
#                         moves.append((x, y, z))
#         return moves
    
#     def get_winner(self):
#         # Check all possible winning lines
#         lines = self.generate_lines()
#         for line in lines:
#             first = self.board[line[0][0]][line[0][1]][line[0][2]]
#             if first != 0 and all(self.board[x][y][z] == first for x, y, z in line):
#                 return first
#         if self.is_full():
#             return 0  # Draw
#         return None  # Game not finished
    
#     def generate_lines(self):
#         # Generate all possible winning lines
#         lines = []
#         # Add lines for rows, columns, and diagonals in each dimension
#         for i in range(4):
#             for j in range(4):
#                 lines.append([(i, j, k) for k in range(4)])  # x-y plane
#                 lines.append([(i, k, j) for k in range(4)])  # x-z plane
#                 lines.append([(k, i, j) for k in range(4)])  # y-z plane
#         # Add diagonals
#         for i in range(4):
#             lines.append([(i, i, k) for k in range(4)])
#             lines.append([(i, k, i) for k in range(4)])
#             lines.append([(k, i, i) for k in range(4)])
#         # Add space diagonals
#         lines.append([(i, i, i) for i in range(4)])
#         lines.append([(i, i, 3-i) for i in range(4)])
#         lines.append([(i, 3-i, i) for i in range(4)])
#         lines.append([(3-i, i, i) for i in range(4)])
#         return lines

#     def is_full(self):
#         # Check if the board is full
#         return all(self.board[x][y][z] != 0 for x in range(4) for y in range(4) for z in range(4))
    
#     def is_terminal(self):
#         """Check if the game is in a terminal state (won or drawn)"""
#         return self.get_winner() is not None or not self.get_legal_moves()
    
#     def clone(self):
#         new_game = Qubic()
#         new_game.board = [[[cell for cell in plane] for plane in board] 
#                          for board in self.board]
#         new_game.current_player = self.current_player
#         return new_game


class Qubic:
    def __init__(self):
        # Initialize a 3x3x3 board
        self.board = [[[0 for _ in range(3)] for _ in range(3)] for _ in range(3)]
        self.current_player = 1
    
    def dimensions(self):
        return len(self.board[0])

    def make_move(self, x, y, z):
        # Place a move on the board
        if self.board[x][y][z] == 0:
            self.board[x][y][z] = self.current_player
            return True
        return False

    def switch_player(self):
        # Switch the current player, since 3-2=1 and 3-1=2
        self.current_player = 3 - self.current_player

    def is_valid_move(self, x, y, z):
        return 0 <= x < 3 and 0 <= y < 3 and 0 <= z < 3 and self.board[x][y][z] == 0
    
    def get_legal_moves(self):
        moves = []
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    if self.board[x][y][z] == 0:
                        moves.append((x, y, z))
        return moves
    
    def get_winner(self):
        # Check all possible winning lines
        lines = self.generate_lines()
        for line in lines:
            first = self.board[line[0][0]][line[0][1]][line[0][2]]
            if first != 0 and all(self.board[x][y][z] == first for x, y, z in line):
                return first
        if self.is_full():
            return 0  # Draw
        return None  # Game not finished
    
    def generate_lines(self):
        # Generate all possible winning lines
        lines = []
        # Add lines for rows, columns, and diagonals in each dimension
        for i in range(3):
            for j in range(3):
                lines.append([(i, j, k) for k in range(3)])  # x-y plane
                lines.append([(i, k, j) for k in range(3)])  # x-z plane
                lines.append([(k, i, j) for k in range(3)])  # y-z plane
        # Add diagonals
        for i in range(3):
            lines.append([(i, i, k) for k in range(3)])
            lines.append([(i, k, i) for k in range(3)])
            lines.append([(k, i, i) for k in range(3)])
        # Add space diagonals
        lines.append([(i, i, i) for i in range(3)])
        lines.append([(i, i, 2-i) for i in range(3)])
        lines.append([(i, 2-i, i) for i in range(3)])
        lines.append([(2-i, i, i) for i in range(3)])
        return lines

    def is_full(self):
        # Check if the board is full
        return all(self.board[x][y][z] != 0 
                  for x in range(3) for y in range(3) for z in range(3))
    
    def is_terminal(self):
        """Check if the game is in a terminal state (won or drawn)"""
        return self.get_winner() is not None or not self.get_legal_moves()
    
    def clone(self):
        new_game = Qubic()
        new_game.board = [[[cell for cell in plane] for plane in board] 
                         for board in self.board]
        new_game.current_player = self.current_player
        return new_game
