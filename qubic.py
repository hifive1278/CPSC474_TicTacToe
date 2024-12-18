'''
qubic.py
contains the game logic for Qubic.
'''

class Qubic:
    def __init__(self):
        # Initialize the qubic board
        self.dimension = 3  # to shorten the time to run our trials... not enough comp. power :(
        self.board = [[[0 for _ in range(self.dimension)] for _ in range(self.dimension)] for _ in range(self.dimension)]
        self.current_player = 1

    def display_board(self):
        print("Curr Player: " + str(self.current_player))
        
        for y in range(self.dimension):
            row_strings = []
            for z in range(self.dimension):
                row = []
                for x in range(self.dimension):
                    value = self.board[z][y][x]
                    if value == 0:
                        row.append('.')
                    elif value == 1:
                        row.append('1')
                    elif value == 2:
                        row.append('2')
                row_strings.append(" ".join(row))
            
            print("   ".join(row_strings))
        print("\n" + "-" * 30 + "\n")

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
        return 0 <= x < self.dimension and 0 <= y < self.dimension and 0 <= z < self.dimension and self.board[x][y][z] == 0
    
    def get_legal_moves(self):
        moves = []
        for x in range(self.dimension):
            for y in range(self.dimension):
                for z in range(self.dimension):
                    if self.board[x][y][z] == 0:
                        moves.append((x, y, z))
        return moves
    
    def is_full(self):
        return all(self.board[x][y][z] != 0 for x in range(self.dimension) for y in range(self.dimension) for z in range(self.dimension))
    
    def is_terminal(self):
        # Check if the game is in a terminal state (won or drawn)
        return self.get_winner() is not None or not self.get_legal_moves()
    
    def get_winner(self):
        # check all possible winning lines
        lines = self.generate_lines()
        for line in lines:
            first = self.board[line[0][0]][line[0][1]][line[0][2]]
            if first != 0 and all(self.board[x][y][z] == first for x, y, z in line):
                return first
        if self.is_full():
            return 0  # draw
        return None  # game not finished
    
    def generate_lines(self):
        # Generate all possible winning lines
        lines = []
        # Add lines for rows, columns, and diagonals in each dimension
        for i in range(self.dimension):
            for j in range(self.dimension):
                lines.append([(i, j, k) for k in range(self.dimension)])  # x-y plane
                lines.append([(i, k, j) for k in range(self.dimension)])  # x-z plane
                lines.append([(k, i, j) for k in range(self.dimension)])  # y-z plane
        # Add diagonals within each plane
        for i in range(self.dimension):
            # Diagonals in x-y planes (z fixed)
            lines.append([(i, i, k) for k in range(self.dimension)])
            lines.append([(i, (self.dimension-1)-i, k) for k in range(self.dimension)])
            # Diagonals in x-z planes (y fixed)
            lines.append([(i, k, i) for k in range(self.dimension)])
            lines.append([(i, k, (self.dimension-1)-i) for k in range(self.dimension)])
            # Diagonals in y-z planes (x fixed)
            lines.append([(k, i, i) for k in range(self.dimension)])
            lines.append([(k, i, (self.dimension-1)-i) for k in range(self.dimension)])
        # Add space diagonals
        lines.append([(i, i, i) for i in range(self.dimension)])
        lines.append([(i, i, (self.dimension-1)-i) for i in range(self.dimension)])
        lines.append([(i, (self.dimension-1)-i, i) for i in range(self.dimension)])
        lines.append([((self.dimension-1)-i, i, i) for i in range(self.dimension)])
        return lines

    def dimensions(self):
        return self.dimension
    
    def clone(self):
        new_game = Qubic()
        new_game.board = [[[cell for cell in plane] for plane in board] 
                         for board in self.board]
        new_game.current_player = self.current_player
        return new_game
