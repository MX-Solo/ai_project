class Board:
    def __init__(self, size=8):
        self.size = size
        self.board = [[None for _ in range(size)] for _ in range(size)]
        self._initialize_board()

    def is_terminal(self):
        return not self.get_valid_moves('B') and not self.get_valid_moves('W')

    def _initialize_board(self):
        # Set up the initial four discs in the center
        mid = self.size // 2
        self.board[mid-1][mid-1] = 'W'
        self.board[mid][mid] = 'W'
        self.board[mid-1][mid] = 'B'
        self.board[mid][mid-1] = 'B'

    def display(self):
        # Print the board state
        for row in self.board:
            print(' '.join([disc if disc else '.' for disc in row]))
        print()

    def get_valid_moves(self, player_color):
        # Return a list of valid moves (row, col) for the player
        valid_moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.is_valid_move(row, col, player_color):
                    valid_moves.append((row, col))
        return valid_moves

    def is_valid_move(self, row, col, player_color):
        # Check if placing a disc on (row, col) is valid
        if self.board[row][col] is not None:
            return False

        opponent_color = 'W' if player_color == 'B' else 'B'
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            found_opponent = False
            while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == opponent_color:
                r += dr
                c += dc
                found_opponent = True

            if found_opponent and 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == player_color:
                return True
        return False

    def place_disc(self, row, col, player_color):
        # Place a disc and flip opponent's discs
        if not self.is_valid_move(row, col, player_color):
            return False

        self.board[row][col] = player_color
        self.flip_discs(row, col, player_color)
        return True

    def flip_discs(self, row, col, player_color):
        # Flip the opponent's discs
        opponent_color = 'W' if player_color == 'B' else 'B'
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            flip_positions = []
            while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == opponent_color:
                flip_positions.append((r, c))
                r += dr
                c += dc

            if 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == player_color:
                for rr, cc in flip_positions:
                    self.board[rr][cc] = player_color

    def is_full(self):
        # Check if the board is full
        return all(all(cell is not None for cell in row) for row in self.board)

    def get_score(self):
        # Return the score as a tuple (B_score, W_score)
        B_score = sum(row.count('B') for row in self.board)
        W_score = sum(row.count('W') for row in self.board)
        return B_score, W_score
    
    def copy(self):
        """Create a copy of the current board state."""
        new_board = Board(self.size)
        new_board.board = [row[:] for row in self.board]  # Deep copy of the board
        return new_board
