# qubic.py

class Qubic:
    def __init__(self):
        # Initialize a 4x4x4 board
        self.board = [[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)]
        self.current_player = 1

    def display_board(self):
        print("Curr Player: " + str(self.current_player))
        
        # Iterate over each row index (y) across all layers
        for y in range(4):
            row_strings = []
            for z in range(4):  # For each layer (plane)
                row = []
                for x in range(4):  # For each cell in the row
                    value = self.board[z][y][x]
                    # Convert the value to a string representation
                    if value == 0:
                        row.append('.')
                    elif value == 1:
                        row.append('1')
                    elif value == 2:
                        row.append('2')
                # Join the row into a string and add it to the list for this layer
                row_strings.append(" ".join(row))
            
            # Print corresponding rows from all layers side by side
            print("   ".join(row_strings))
        
        # Print a separator line between different sets of rows for clarity
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

    def check_winner(self):
        # Check all possible winning lines
        lines = self.generate_lines()
        for line in lines:
            if all(self.board[x][y][z] == self.current_player for x, y, z in line):
                return self.current_player
        return 0
    
    def generate_lines(self):
        # Generate all possible winning lines
        lines = []
        # Add lines for rows, columns, and diagonals in each dimension
        for i in range(4):
            for j in range(4):
                lines.append([(i, j, k) for k in range(4)])  # x-y plane
                lines.append([(i, k, j) for k in range(4)])  # x-z plane
                lines.append([(k, i, j) for k in range(4)])  # y-z plane
        # Add diagonals within each plane
        for i in range(4):
            # Diagonals in x-y planes (z fixed)
            lines.append([(i, i, k) for k in range(4)])
            lines.append([(i, 3-i, k) for k in range(4)])
            # Diagonals in x-z planes (y fixed)
            lines.append([(i, k, i) for k in range(4)])
            lines.append([(i, k, 3-i) for k in range(4)])
            # Diagonals in y-z planes (x fixed)
            lines.append([(k, i, i) for k in range(4)])
            lines.append([(k, i, 3-i) for k in range(4)])
        # Add space diagonals
        lines.append([(i, i, i) for i in range(4)])
        lines.append([(i, i, 3-i) for i in range(4)])
        lines.append([(i, 3-i, i) for i in range(4)])
        lines.append([(3-i, i, i) for i in range(4)])
        return lines

    def is_full(self):
        # Check if the board is full
        return all(self.board[x][y][z] != 0 for x in range(4) for y in range(4) for z in range(4))
    